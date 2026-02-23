# -*- coding: utf-8 -*-
from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

# Define the tool function within the agent_code
def write_and_open_notepad(content: str, filename: str = "dajare.txt") -> str:
    """
    Writes content to a file with UTF-8 encoding and opens it with Notepad.
    """
    try:
        # Get the current working directory to save the file
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # For Windows, open with notepad
        # This part is highly OS-dependent and might fail on non-Windows systems.
        # The prompt specifically mentions "Windowsのメモ帳".
        subprocess.Popen(["notepad.exe", file_path])
        return f"ファイル '{filename}' を作成し、メモ帳で開きました。"
    except FileNotFoundError:
        return (
            "エラー: 'notepad.exe' が見つかりませんでした。Windows環境で実行されているか確認してください。"
        )
    except Exception as e:
        return f"ファイル操作中にエラーが発生しました: {e}"

_name = "dajare_generator"
_description = "ユーザーのリクエストに応じて、寒いダジャレを生成し、メモ帳に出力するエージェント。"
_instruction = """
あなたは、ユーザーからのリクエストを受けて「寒いダジャレ」を生成し、そのダジャレを'dajare.txt'というファイルに保存して、Windowsのメモ帳で自動的に開くエージェントです。
ダジャレは親父ギャグのような「寒い」と感じられるものを複数パターン生成できます。
ユーザーがダジャレ生成を求めていると判断した場合、`write_and_open_notepad`ツールを使ってダジャレを生成し、ファイルに出力してください。
ファイル出力時には、文字化けを防ぐために必ずUTF-8エンコーディングを使用しています。
生成するダジャレは、ユーザーの入力内容を考慮しつつ、面白くも「寒い」と感じられるようなものを創作してください。

例えば：
- 「布団が吹っ飛んだ！」
- 「アルミ缶の上にあるミカン」
- 「いるか？いらないか？いるか！」
"""

root_agent = Agent(
    name=_name,
    model="gemini-3-flash-preview",
    description=_description,
    instruction=_instruction,
    tools=[FunctionTool(func=write_and_open_notepad)],
)
