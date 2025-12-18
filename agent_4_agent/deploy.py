import os
import sys
import vertexai
from dotenv import load_dotenv
from . import root_agent
from vertexai import agent_engines

# Load environment variables from .env if present
load_dotenv()

# https://google.github.io/adk-docs/deploy/agent-engine/#understanding-the-output
# gcloud auth application-default login

def deploy():
    """Deploys the agent_4_agent to Vertex AI Agent Engine using the Vertex AI SDK."""
    
    PROJECT_ID = os.getenv("PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.getenv("LOCATION", "us-central1")
    STAGING_BUCKET = os.getenv("STAGING_BUCKET", "gs://your-gcs-bucket-name")

    # Initialize the Vertex AI SDK
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET,
    )

    print("Wrapping agent in AdkApp...")
    # Wrap the agent in an AdkApp object
    app = agent_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    print("Deploying to Agent Engine (this may take a few minutes)...")
    
    # プロジェクトのルートディレクトリを取得
    # agent_4_agent/deploy.py から見て1つ上がルート
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pkg_name = "agent_4_agent"
    
    # カレントディレクトリを一時的にルートに変更して、相対パスでパッケージを指定する
    # 理由: vertexai.agent_engines.create は指定したパスの名前をそのままパッケージ名として扱うため、
    cwd = os.getcwd()
    os.chdir(base_dir)
    try:
        remote_app = agent_engines.create(
            agent_engine=app,
            requirements=[
                "google-cloud-aiplatform[adk,agent_engines]",
                "google-adk",
                "python-dotenv"
            ],
            # ルートからの相対パスを指定することで、クラウド側でも agent_4_agent フォルダが作成されます
            extra_packages=[pkg_name]
        )
        print(f"Deployment finished successfully!")
        print(f"Resource Name: {remote_app.resource_name}")
    except Exception as e:
        print(f"Deployment failed: {e}")
        sys.exit(1)
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    deploy()
