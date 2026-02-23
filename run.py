#!/usr/bin/env python3
"""
agent_4_agent CLI - エージェントを自動作成し、品質レビューしてGitHub issueを起票する

Usage:
    # 直接プロンプトを渡して作成
    python run.py "天気予報エージェントを作って"

    # キーワードだけ渡してLLMにプロンプトを生成させてから作成
    python run.py --idea "天気"
    python run.py --idea "沖縄観光" --review

    # 作成後にコードレビュー → GitHub issue も起票する
    python run.py "天気予報エージェントを作って" --review

    # 既存エージェントのみレビューする（作成はスキップ）
    python run.py --review-only weather_agent
"""
import asyncio
import argparse
import os
import re
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / "agent_4_agent" / ".env")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


def _make_runner(agent, app_name: str) -> tuple[Runner, InMemorySessionService]:
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )
    return runner, session_service


async def _run_one_turn(runner: Runner, session_id: str, message_text: str) -> str:
    """1ターン実行してレスポンステキストを返す"""
    message = types.Content(role="user", parts=[types.Part.from_text(text=message_text)])
    collected: list[str] = []
    async for event in runner.run_async(
        user_id="cli_user",
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                text = getattr(part, "text", None)
                if text:
                    print(text, end="", flush=True)
                    collected.append(text)
    print()
    return "".join(collected)


def _is_question(text: str) -> bool:
    """エージェントが追加情報を求めているかを判定する"""
    signals = ["？", "教えてください", "確認させてください", "いかがでしょうか",
               "ご要望", "ご希望", "どちらを", "どのよう", "でよろしいですか"]
    return any(s in text for s in signals)


def _is_done(text: str) -> bool:
    """エージェントが作業完了したかを判定する"""
    signals = ["---納品---", "納品報告", "納品---", "agent_name:"]
    return any(s in text for s in signals)


async def _auto_answer(question: str, context: str) -> str:
    """PMからの確認質問にLLMで自動回答する"""
    from google import genai

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    system_instruction = """あなたはエージェント開発の依頼者です。
PMエージェントから確認・質問が来たので、簡潔に回答してください。

## 回答方針
- シンプルで実用的な選択をする
- 出発地が必要なら那覇空港をデフォルトにする
- URLは動的生成（urllib.parse.quote）で良い
- 外部APIキーが不要な実装を優先する
- 迷ったら「おまかせします」と答えてよい
- 回答は1〜3文で簡潔に

回答文だけ出力してください。前置き不要。"""

    response = client.models.generate_content(
        model=os.environ.get("MODEL", "gemini-2.0-flash"),
        contents=f"作成アイデア: {context}\n\nPMからの質問:\n{question}",
        config={"system_instruction": system_instruction},
    )
    return response.text.strip()


async def _conversation_loop(
    runner: Runner,
    session_service: InMemorySessionService,
    app_name: str,
    initial_prompt: str,
    context: str,
    max_turns: int = 10,
) -> str:
    """完了まで自動で会話を続けるループ（質問には自動回答）"""
    session = await session_service.create_session(app_name=app_name, user_id="cli_user")
    message_text = initial_prompt
    all_output: list[str] = []

    for turn in range(max_turns):
        response = await _run_one_turn(runner, session.id, message_text)
        all_output.append(response)

        if _is_done(response) or not _is_question(response):
            break

        # 質問を検出 → LLMで自動回答して次のターンへ
        answer = await _auto_answer(response, context)
        print(f"[自動回答] {answer}\n")
        message_text = answer
    else:
        print(f"[警告] {max_turns}ターン到達。会話を終了します。")

    return "\n".join(all_output)


async def _stream(runner: Runner, session_service: InMemorySessionService, app_name: str, prompt: str) -> str:
    """単発実行（review用）"""
    session = await session_service.create_session(app_name=app_name, user_id="cli_user")
    return await _run_one_turn(runner, session.id, prompt)


async def generate_prompt_from_idea(idea: str) -> str:
    """キーワード/アイデアから agent_4_agent 向けの具体的な作成プロンプトをLLMで生成する"""
    from google import genai

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    system_instruction = """あなたはエージェント設計の専門家です。
ユーザーのざっくりしたアイデアやキーワードから、agent_4_agent に渡す具体的なエージェント作成指示を1つ生成してください。

## 出力ルール
- 1〜3文の日本語で書く
- エージェント名（英小文字+アンダースコア）を必ず含める
- 具体的にどんなツール・機能が必要かを述べる
- ダミーデータを使わず、URLを動的生成するツールを活用することを示唆する

## 出力例
- input: "天気"
  output: "weather_forecast_agent を作って。都市名を受け取り、Yahoo天気とGoogle検索へのリンクURLを動的生成して返すツールを持つエージェントにしてください。"

- input: "レシピ"
  output: "recipe_search_agent を作って。料理名からクックパッドとYouTubeの検索URLを動的生成して返すツールを持つエージェントにしてください。"

指示文だけを出力してください。説明や前置きは不要です。"""

    response = client.models.generate_content(
        model=os.environ.get("MODEL", "gemini-2.0-flash"),
        contents=idea,
        config={"system_instruction": system_instruction},
    )
    return response.text.strip()


def _extract_agent_name(output: str) -> str | None:
    """納品レポートから agent_name を抽出する"""
    match = re.search(r'agent_name[:\s]+([a-z][a-z0-9_]+)', output, re.IGNORECASE)
    return match.group(1) if match else None


async def run_create(prompt: str, context: str) -> str:
    """agent_4_agent を実行してエージェントを作成する（質問には自動回答）"""
    from agent_4_agent import root_agent

    runner, session_service = _make_runner(root_agent, "a4a_cli")
    print("=" * 60)
    print("agent_4_agent 実行中...")
    print("=" * 60)
    return await _conversation_loop(runner, session_service, "a4a_cli", prompt, context)


async def run_review(agent_name: str) -> None:
    """quality_reporter_agent を実行して GitHub issue を起票する"""
    from agent_4_agent.subagents.quality_reporter_agent import quality_reporter_agent

    runner, session_service = _make_runner(quality_reporter_agent, "review_cli")
    prompt = f"{agent_name} のコードレビューをして、改善点があれば GitHub issue を作成してください。"
    print("\n" + "=" * 60)
    print(f"品質レビュー中: {agent_name}")
    print("=" * 60)
    await _stream(runner, session_service, "review_cli", prompt)


async def main_async(
    prompt: str | None, idea: str | None, review: bool, review_only: str | None
) -> None:
    if review_only:
        await run_review(review_only)
        return

    # --idea が指定されている場合はLLMでプロンプトを生成する
    if idea:
        print("=" * 60)
        print(f"アイデア → プロンプト生成中: '{idea}'")
        print("=" * 60)
        prompt = await generate_prompt_from_idea(idea)
        print(f"生成されたプロンプト:\n  {prompt}\n")

    output = await run_create(prompt, context=idea or prompt)

    if review:
        agent_name = _extract_agent_name(output)
        if agent_name:
            await run_review(agent_name)
        else:
            print("\nagent_name を出力から特定できませんでした。")
            print("手動でレビューする場合: python run.py --review-only <agent_name>")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="agent_4_agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python run.py "天気予報エージェントを作って"
  python run.py --idea "天気"
  python run.py --idea "沖縄観光" --review
  python run.py --review-only okinawa_gourmet_agent
""",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="エージェント作成の指示（直接渡す場合）",
    )
    parser.add_argument(
        "--idea",
        metavar="KEYWORD",
        help="キーワードだけ渡してLLMに作成プロンプトを自動生成させる（例: --idea '天気'）",
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="作成後にコードレビューして GitHub issue を起票する",
    )
    parser.add_argument(
        "--review-only",
        metavar="AGENT_NAME",
        help="既存エージェントのみレビューする（作成はスキップ）",
    )

    args = parser.parse_args()

    if not args.prompt and not args.idea and not args.review_only:
        parser.print_help()
        sys.exit(1)

    asyncio.run(main_async(args.prompt, args.idea, args.review, args.review_only))


if __name__ == "__main__":
    main()
