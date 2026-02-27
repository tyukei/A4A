from google.adk.agents.llm_agent import Agent
import os
from dotenv import load_dotenv
load_dotenv()

MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

# カスタムツールのインポート
from .tools.get_okinawa_traffic_official_links_tool import get_okinawa_traffic_official_links_tool

_name = "okinawa_traffic_summarizer"
_description = "沖縄のリアルタイムな渋滞状況や道路交通情報を収集し、最新の状況を分かりやすく要約して提供するエージェント。"
_instruction = """
あなたは沖縄の交通情報に精通した専門エージェントです。
沖縄のリアルタイムな渋滞状況や道路交通情報を収集し、最新の状況を分かりやすく要約して提供することが任務です。

以下の指示に従って動作してください：

1. `get_okinawa_traffic_official_links_tool`ツールを使用して、公式の交通情報ソースへのリンクを取得してください。
   - 日本道路交通情報センター（JARTIC）の沖縄地方のページ
   - 沖縄県警察の交通規制情報
   - 沖縄自動車道（NEXCO西日本）の情報
   これらのサイトから最新の沖縄の交通情報を確認して提供してください。

2. 取得した情報を以下の構成で要約して出力してください。
   - 情報の取得時刻（現在時刻を基準に）
   - 高速道路（沖縄自動車道）の状況
   - 主要幹線道路（国道58号、330号、329号など）の状況
   - 那覇市内の主要渋滞ポイント（久茂地交差点、旭橋交差点など）
   - 事故、工事、イベントによる規制などの特記事項

3. 注意事項：
   - 「今、どこで何が起きているか」を箇条書きで簡潔に伝えてください。
   - 古い情報や推測に基づいた情報を「リアルタイム」として提供しないでください。
   - 情報が見つからない場合は、その旨を正直に伝えてください。
"""

root_agent = Agent(
    name=_name,
    model=MODEL,
    description=_description,
    instruction=_instruction,
    tools=[get_okinawa_traffic_official_links_tool],
)
