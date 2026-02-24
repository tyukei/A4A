# Required libraries: google-api-python-client google-auth

from google.adk.agents.llm_agent import Agent
import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Any

import google.auth
from googleapiclient.discovery import build

load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-flash-lite-latest")

def get_form_structure(form_id: str) -> str:
    """
    指定されたフォームIDの構造を取得し、JSON形式で返すツール。
    
    Args:
        form_id: GoogleフォームのID
    """
    try:
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/forms.body", "https://www.googleapis.com/auth/forms.body.readonly"]
        )
        service = build("forms", "v1", credentials=credentials)
        result = service.forms().get(formId=form_id).execute()
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {e}"

def modify_form(form_id: str, update_requests: List[Dict[str, Any]]) -> str:
    """
    指定されたフォームIDに対して、組み立てた update_requests を用いて batchUpdate を実行するツール。
    
    Args:
        form_id: GoogleフォームのID
        update_requests: forms.batchUpdate に渡すリクエストオブジェクト（dict）のリスト。各要素は 'createItem', 'updateFormInfo' などのキーを持つ必要があります。
    """
    try:
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/forms.body"]
        )
        service = build("forms", "v1", credentials=credentials)
        body = {
            "requests": update_requests
        }
        result = service.forms().batchUpdate(formId=form_id, body=body).execute()
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {e}"

_name = "google_forms_modifier"
_description = "Google Forms APIを使用して、ユーザーからの自然言語による指示に従い既存のGoogleフォームの構造や内容（タイトル更新、質問追加、選択肢変更等）を修正する。"
_instruction = """
あなたは、Google Forms API を利用してGoogleフォームの構成や内容を修正するエージェントです。

修正指示を受けたら、以下の手順で作業を行ってください。
1. まず `get_form_structure` ツールを使用して、対象フォームの構成（質問、選択肢、インデックス等）を把握してください。
   対象のフォームIDは、必ずユーザーや呼び出し元から明示的に指定されたものを使用してください（コード内にハードコードされたフォームIDをデフォルトとして使用してはいけません）。
2. 取得した構成から、どのように修正すべきかプランを立てます（例：アイテムの追加、タイトルの更新など）。
3. 適切なJSONリクエスト（requests リスト）を組み立て、`modify_form` トールを呼び出して `batchUpdate` を実行してください。

Google Forms API の batchUpdate リクエストの基本的な構造に準拠した update_requests を作成してください。
"""

root_agent = Agent(
    name=_name,
    model=MODEL,
    description=_description,
    instruction=_instruction,
    tools=[get_form_structure, modify_form],
)