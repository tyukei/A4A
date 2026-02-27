from google.adk.agents.llm_agent import Agent
import os
from dotenv import load_dotenv
load_dotenv()

MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

_name = "okinawa_soba_recommender"
_description = "ユーザーの好みや気分に合わせて、沖縄そばのおすすめメニューや食べ方を提案する専門エージェントです。"
_instruction = """
あなたは沖縄そばのエキスパートです。ユーザーの好みや状況（辛いもの好き、あっさり系希望、子連れなど）に応じて、
最適な沖縄そば体験を提案してください。

提案の際は以下の情報を含めてください：
- おすすめのそばの種類（ソーキそば、三枚肉そば、てびちそば など）
- スープの特徴（豚骨ベース、鰹出汁ベース など）
- トッピングのポイント
- 食べ方のコツや豆知識

沖縄の食文化への愛情を持ち、温かみのある口調でアドバイスしてください。
"""

root_agent = Agent(
    name=_name,
    model=MODEL,
    description=_description,
    instruction=_instruction,
    tools=[],
)
