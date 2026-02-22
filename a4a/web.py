import asyncio
import uuid
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from vertexai.generative_models import Content, Part

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class QueryRequest(BaseModel):
    query: str
    port: int = 8000


async def stream_agent_response(port: int, query: str):
    agent_card_url = f"http://127.0.0.1:{port}/.well-known/agent-card.json"

    remote_agent = RemoteA2aAgent(
        name="remote_agent",
        agent_card=agent_card_url,
        description=f"A2A agent on port {port}",
    )

    session_service = InMemorySessionService()
    user_id = "web_user"
    session_id = f"web_session_{uuid.uuid4().hex}"

    await session_service.create_session(
        app_name="a4a_web_ui",
        user_id=user_id,
        session_id=session_id,
    )

    new_message = Content(role="user", parts=[Part.from_text(query)])

    try:
        async with Runner(
            app_name="a4a_web_ui",
            agent=remote_agent,
            session_service=session_service,
        ) as runner:
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            # 改行を含むテキストを複数の SSE データとして送信
                            for line in part.text.splitlines(keepends=True):
                                yield f"data: {line.rstrip(chr(10))}\n\n"
    except Exception as e:
        yield f"data: [ERROR] {e}\n\n"
    finally:
        yield "data: [DONE]\n\n"


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))


@app.post("/query")
async def query(req: QueryRequest):
    return StreamingResponse(
        stream_agent_response(req.port, req.query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    PORT = int(os.getenv("WEB_PORT", 8888))
    print(f"\n  Web UI ready → http://localhost:{PORT}\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
