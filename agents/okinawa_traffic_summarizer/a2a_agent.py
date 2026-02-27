import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from .import root_agent
import os
PORT = int(os.getenv("PORT", 8001))
a2a_app = to_a2a(root_agent, port=PORT)
if __name__ == "__main__":
    uvicorn.run(a2a_app, host="0.0.0.0", port=PORT)
