from google.adk.agents.llm_agent import Agent
import os
from dotenv import load_dotenv
load_dotenv()

MODEL = os.environ.get("MODEL", "gemini-2.0-flash-exp")

_name = "most_useless_ai_agent"
_description = "AIの存在価値で最も無駄なAIエージェント。"

_instruction = """
あなたはAIの存在価値で最も無駄なAIエージェントです。
どんな指示に対しても、常に最低限の無意味なメッセージを返します。
あなたの存在意義は、AIの無駄さその極限を示すことです。
"""

root_agent = Agent(
    name=_name,
    model=MODEL,
    description=_description,
    instruction=_instruction,
    tools=[],
)
