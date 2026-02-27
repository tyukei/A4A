# https://docs.cloud.google.com/agent-builder/agent-engine/use/adk?hl=ja#vertex-ai-sdk-for-python

import vertexai
from vertexai import agent_engines
import asyncio
import os 
from dotenv import load_dotenv
load_dotenv()

AGENT_RESOURCE_NAME = os.getenv("AGENT_RESOURCE_NAME")
PROJECT_ID = os.getenv("PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("LOCATION", "us-central1")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "gs://your-gcs-bucket-name")

# Initialize the Vertex AI SDK
client = vertexai.Client(
    project=PROJECT_ID,
    location=LOCATION,
)
adk_app = client.agent_engines.get(name=AGENT_RESOURCE_NAME)

# agent engineにディプロイしたエージェントを呼び出す
async def call_agent(query:str):
    async for event in adk_app.async_stream_query(
        user_id="USER_ID",
        message=query,
    ):
        print(event['content']['parts'][0]['text'])




async def main():
    await call_agent("あなたは、何ができますか")


if __name__ == "__main__":
    asyncio.run(main())
