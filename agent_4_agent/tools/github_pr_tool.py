import subprocess
import os
from google.adk.tools.function_tool import FunctionTool


def _run_git(args: list[str], cwd: str, timeout: int = 60) -> tuple[int, str, str]:
    """git コマンドを実行して (returncode, stdout, stderr) を返す"""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True, text=True, cwd=cwd, timeout=timeout
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def create_github_pr(agent_name: str, description: str = "") -> str:
    """新しく作成されたエージェントのGitHub PRを作成する

    Args:
        agent_name: エージェント名（英小文字+アンダースコア、例: weather_forecast_agent）
        description: エージェントの説明（PR本文に使用）

    Returns:
        PRのURLまたはエラーメッセージ
    """
    try:
        # リポジトリルートを取得（このファイルの3階層上）
        repo_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        branch_name = f"feat/add-{agent_name.replace('_', '-')}"

        # 現在のブランチを保存（PR作成後に戻るため）
        rc, original_branch, _ = _run_git(["branch", "--show-current"], repo_root)
        if rc != 0:
            original_branch = "main"

        # 1. 新しいブランチを作成（既存なら切り替え）
        rc, out, err = _run_git(["checkout", "-b", branch_name], repo_root)
        if rc != 0:
            rc, out, err = _run_git(["checkout", branch_name], repo_root)
            if rc != 0:
                return f"エラー: ブランチ切り替え失敗: {err}"

        # 2. エージェントディレクトリをステージング（.env は .gitignore で除外済み）
        agent_dir = os.path.join("agents", agent_name)
        rc, out, err = _run_git(["add", agent_dir], repo_root)
        if rc != 0:
            _run_git(["checkout", original_branch], repo_root)
            return f"エラー: git add 失敗: {err}"

        # 変更がない場合はスキップ
        rc, status_out, _ = _run_git(["status", "--porcelain"], repo_root)
        if not status_out:
            _run_git(["checkout", original_branch], repo_root)
            return f"情報: {agent_name} にコミットすべき変更がありませんでした"

        # 3. コミット
        commit_msg = f"feat: Add {agent_name}"
        if description:
            commit_msg += f"\n\n{description}"
        rc, out, err = _run_git(["commit", "-m", commit_msg], repo_root)
        if rc != 0:
            _run_git(["checkout", original_branch], repo_root)
            return f"エラー: git commit 失敗: {err}"

        # 4. リモートにプッシュ
        rc, out, err = _run_git(["push", "-u", "origin", branch_name], repo_root)
        if rc != 0:
            _run_git(["checkout", original_branch], repo_root)
            return f"エラー: git push 失敗: {err}"

        # 5. PR作成（pull_request_template.md の構造に準拠）
        pr_title = f"[{agent_name}(shink-shinka)] Add {agent_name}"
        agent_desc = description or agent_name
        pr_body = (
            "## 概要\n\n"
            f"A4Aにより自動生成されたエージェント `{agent_name}` を追加します。\n"
            f"{agent_desc}\n\n"
            "## 変更内容\n\n"
            f"- `agents/{agent_name}/agent.py` — エージェント本体\n"
            f"- `agents/{agent_name}/__init__.py` — モジュール定義\n"
            f"- `agents/{agent_name}/a2a_agent.py` — A2A連携エントリポイント\n\n"
            "## 関連するIssue\n\n"
            "Closes #\n\n"
            "## 動作確認方法\n\n"
            "```bash\n"
            "adk web\n"
            "```\n\n"
            f"左上のエージェント選択で `{agent_name}` を選択し、チャットで動作確認してください。\n\n"
            "## チェックリスト\n\n"
            "- [ ] 既存の機能に影響がないことを確認した\n"
            "- [ ] タイポや不要なコメントがないことを確認した\n"
            "- [ ] 必要なドキュメントを更新した\n\n"
            "## その他\n\n"
            "🤖 Generated with [A4A (Agent for Agent)](https://github.com/tyukei/A4A)"
        )

        result = subprocess.run(
            ["gh", "pr", "create", "--title", pr_title, "--body", pr_body],
            capture_output=True, text=True, cwd=repo_root, timeout=60
        )

        # 元のブランチに戻る
        _run_git(["checkout", original_branch], repo_root)

        if result.returncode == 0:
            return f"PR作成成功: {result.stdout.strip()}"
        else:
            return f"PR作成失敗: {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "エラー: コマンドがタイムアウトしました"
    except FileNotFoundError as e:
        return f"エラー: コマンドが見つかりません ({str(e)})"
    except Exception as e:
        return f"エラー: {str(e)}"


create_github_pr_tool = FunctionTool(func=create_github_pr)
