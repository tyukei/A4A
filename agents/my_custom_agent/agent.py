# my_custom_agent/agent.py
import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent  # LlmAgentでもOK
from .tools import create_google_maps_directions_link_tool, get_nago_chuka_candidates_tool

load_dotenv()

MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

root_agent = Agent(
    name="my_custom_agent",
    model=MODEL,
    description="名護の町中華を検索し、店情報とGoogle Mapの経路リンクを提示するエージェント",
    instruction=(
        "あなたは自作エージェントです。\n"
        "ユーザーの質問に対して、結論→根拠→次の質問 の順で短く答えてください。\n"
        "店候補は get_nago_chuka_candidates_tool を使って取得してください。\n"
        "経路リンクが必要な場合は create_google_maps_directions_link_tool を使ってURLを生成してください。\n"
        "不明な点は捏造せず、不足情報を1つだけ質問してください。"
    ),
    tools=[get_nago_chuka_candidates_tool, create_google_maps_directions_link_tool],
)