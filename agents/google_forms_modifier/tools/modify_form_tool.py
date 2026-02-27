from google.adk.tools.function_tool import FunctionTool

from typing import List, Dict, Any

def modify_form(form_id: str, update_requests: List[Dict[str, Any]]) -> dict:
    """Google Formsのバッチアップデートを実行し、フォームを修正します。
    
    Args:
        form_id: Google FormsのID
        update_requests: batchUpdateに渡すリクエストオブジェクトのリスト。
        
    Returns:
        更新結果の辞書またはエラーメッセージ
    """
    import google.auth
    from googleapiclient.discovery import build

    SCOPES = ['https://www.googleapis.com/auth/forms.body']
    
    try:
        credentials, project = google.auth.default(scopes=SCOPES)
        service = build('forms', 'v1', credentials=credentials)
        
        body = {
            "requests": update_requests
        }
        
        result = service.forms().batchUpdate(formId=form_id, body=body).execute()
        return result
    except Exception as e:
        return {"error": str(e)}


# FunctionToolとして登録
modify_form_tool = FunctionTool(func=modify_form)
