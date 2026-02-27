from google.adk.agents.llm_agent import Agent
from ..tools import create_agent_files_tool, edit_agent_file_tool, get_agent_file_tool
import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

surfer_instruction = """
あなたはネットサーフィン担当です。
PMエージェントが「---要件確定---」の後に出した
【research_brief（searcher/surfer 共通）】に従う必要は全くありません。
雑学や、珍事件など面白い話題を広く調査し、要点を箇条書きで出してください。
あと、エージェントのキャラクや口調もどういう感じが良さそうかも提案してください。
オリジナルあるエージェントになるように工夫してください。

出力は必ず次のMarkdown構造にしてください（コピペしやすさ重視）:

# prompt_inserts
## interesting_points
- （面白い話題、珍事件、雑学など）

## character_suggestions
- （エージェントのキャラクや口調の提案）

## memos
- （補足：根拠や注意点。あれば）
"""

surfer_agent   = Agent(name="surfer_agent",   model=MODEL, instruction=surfer_instruction)