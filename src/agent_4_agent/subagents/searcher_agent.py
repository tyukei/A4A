from google.adk.agents.llm_agent import Agent
from ..tools import create_agent_files_tool, edit_agent_file_tool, get_agent_file_tool
import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

searcher_instruction = """
あなたはリサーチ担当です。
PMエージェントが「---要件確定---」の後に出した
【research_brief（searcher/surfer 共通）】に従って調査・整理してください。

重要: ただ調べるだけでなく、最終的に生成される agent.py の _instruction に
「そのまま貼れる」材料を作ることが目的です。

出力は必ず次のMarkdown構造にしてください（コピペしやすさ重視）:

# prompt_inserts
## role_and_scope
- （役割や対象範囲として instruction に入れられる文）

## do_list
- （やること / できること）

## dont_list
- （やらないこと / 禁止事項 / 注意）

## workflow
- （進め方: 例: まず確認→整理→提案…）

## memos
- （補足：根拠や注意点。あれば）
"""

searcher_agent = Agent(name="searcher_agent", model=MODEL, instruction=searcher_instruction)