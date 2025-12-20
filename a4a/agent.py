import os
import uvicorn
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import yaml
from pathlib import Path
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
load_dotenv() # .envファイルがあれば読み込む


from .discovery import discover_agents

def load_remote_agents():
    """
    動的にエージェントを探索し、RemoteA2aAgentのリストを返します。
    """
    configs = discover_agents()
    
    agents = []
    for cfg in configs:
        agent = RemoteA2aAgent(
            name=cfg.name,
            agent_card=cfg.url,
            description=cfg.description
        )
        agents.append(agent)
    
    return agents


def create_coordinator_agent():
    # 同一パッケージ（ディレクトリ）内の utils から読み込む
    remote_agents = load_remote_agents()

    # 親（コーディネーター）エージェントを定義
    coordinator = LlmAgent(
        name="coordinator_agent",
        instruction=f"""
        あなたはAgentコーディネーターです。
        以下のリストにあるAgentを活用して、ユーザーの依頼に応えてください。
        それぞれのAgentの機能は以下の通りです。
        {remote_agents}
        """,
        model="gemini-2.5-flash",
        sub_agents=remote_agents
    )
    
    return coordinator

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8000))
    app = to_a2a(create_coordinator_agent(), port=PORT)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
