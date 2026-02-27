import os
import sys
import importlib
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

import google.genai as genai

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from vertexai.generative_models import Content, Part

from .discovery import discover_agents

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

_session_service = InMemorySessionService()
_sub_agents_cache: dict | None = None

APP_NAME = "a4a_web_ui"
USER_ID  = "web_user"
MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")


def _get_sub_agents() -> dict:
    """サブエージェントをローカルにロードしてキャッシュする。"""
    global _sub_agents_cache
    if _sub_agents_cache is not None:
        return _sub_agents_cache

    root_dir = Path.cwd()
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

    configs = discover_agents(root_dir)
    agents = {}
    for cfg in configs:
        try:
            mod = importlib.import_module(cfg.name)
            agent = getattr(mod, "root_agent", None)
            if agent is not None:
                agents[agent.name] = agent
        except Exception as e:
            print(f"Warning: could not load '{cfg.name}': {e}")

    _sub_agents_cache = agents
    return agents


async def _route_query(query: str, sub_agents: dict) -> str:
    """Gemini に直接問い合わせてルーティング先のエージェント名を取得する。"""
    agent_list = "\n".join(
        f"- {name}: {a.description}" for name, a in sub_agents.items()
    )
    prompt = (
        "以下のエージェントリストから、ユーザーの質問に最適なエージェントを一つ選んでください。\n"
        "エージェント名のみを返してください（他のテキスト不要）。\n\n"
        f"エージェント:\n{agent_list}\n\n"
        f"ユーザーの質問: {query}"
    )

    client = genai.Client()
    resp = await client.aio.models.generate_content(model=MODEL, contents=prompt)
    name = resp.text.strip().strip('"').strip("'")

    if name in sub_agents:
        return name
    # fuzzy fallback
    for n in sub_agents:
        if n.lower() in name.lower() or name.lower() in n.lower():
            return n
    return next(iter(sub_agents))


class QueryRequest(BaseModel):
    query: str
    session_id: str = ""  # ブラウザが生成・保持するセッションID


async def stream_agent_response(query: str, session_id: str):
    sub_agents = _get_sub_agents()

    # コーディネーターがルーティング中
    yield f"data: [AGENT:coordinator_agent]\n\n"

    target_name = await _route_query(query, sub_agents)
    yield f"data: [AGENT:{target_name}]\n\n"

    target_agent = sub_agents[target_name]

    # サブエージェントごとに独立したセッションで会話を継続
    agent_session_id = f"{target_name}__{session_id}"
    existing = await _session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=agent_session_id
    )
    if existing is None:
        await _session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=agent_session_id
        )

    new_message = Content(role="user", parts=[Part.from_text(query)])

    try:
        async with Runner(
            app_name=APP_NAME,
            agent=target_agent,
            session_service=_session_service,
        ) as runner:
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=agent_session_id,
                new_message=new_message,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
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
        stream_agent_response(req.query, req.session_id),
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
