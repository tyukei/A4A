import asyncio
import os
import argparse
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from vertexai.generative_models import Content, Part

async def query_agent(port: int, query: str):
    agent_card_url = f"http://127.0.0.1:{port}/.well-known/agent-card.json"
    
    # 接続先のエージェントを定義
    remote_agent = RemoteA2aAgent(
        name="remote_agent",
        agent_card=agent_card_url,
        description=f"A2A agent on port {port}"
    )
    
    # SessionService を用意
    session_service = InMemorySessionService()
    
    # セッションを作成
    user_id = "cli_user"
    session_id = "cli_session"
    await session_service.create_session(
        app_name="a2a_query_cli",
        user_id=user_id,
        session_id=session_id
    )
    
    # メッセージの構築
    new_message = Content(
        role="user",
        parts=[Part.from_text(query)]
    )
    
    # Runner を使ってメッセージを送信
    async with Runner(
        app_name="a2a_query_cli",
        agent=remote_agent,
        session_service=session_service
    ) as runner:
        # print(f"Connecting to A2A agent at {agent_card_url}...\n")
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            # イベントからテキスト成分を抽出
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
    
    print("\n\nDone.")

def main():
    parser = argparse.ArgumentParser(description="Query an A2A agent.")
    parser.add_argument("--port", type=int, default=8001, help="Port of the A2A agent (default: 8001)")
    parser.add_argument("query", type=str, help="The query message to send")
    
    args = parser.parse_args()
    
    asyncio.run(query_agent(args.port, args.query))

if __name__ == "__main__":
    main()
