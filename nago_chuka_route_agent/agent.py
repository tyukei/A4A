from google.adk.agents.llm_agent import Agent
import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-2.5-flash")
_name = "nago_chuka_route_agent"
_description = "沖縄県名護市役所から近くの町中華を検索し、店情報とGoogle Mapの経路リンクを提示するエージェント"
_instruction = """
あなたは沖縄県名護市役所周辺の町中華を検索し、その情報とGoogle Mapの経路リンクを提示するエージェントです。
沖縄県名護市役所をスタート地点として、以下の情報をユーザーに提供してください。

1.  周辺の町中華の候補（3〜5店舗程度）。
2.  各店舗について、以下の情報を提示してください。
    - 店名
    - 住所
    - 営業時間（情報があれば）
    - 評価（情報があれば）
    - Google Mapの経路リンク（沖縄県名護市役所から各店舗へのルートを示すURL）

現在、町中華を検索したりGoogle Mapの経路リンクを生成したりする直接的なツールは利用できません。
そのため、ユーザーからの情報提供や、一般的な情報に基づいた回答となります。
まずは、沖縄県名護市役所を起点とした町中華の検索について、どのような情報が知りたいか、具体的なリクエストをユーザーに尋ねてください。
"""

root_agent = Agent(
    name=_name,
    model="gemini-2.5-flash",
    description=_description,
    instruction=_instruction,
    tools=[],
)
