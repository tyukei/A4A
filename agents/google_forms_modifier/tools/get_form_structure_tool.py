from google.adk.tools.function_tool import FunctionTool

def get_form_structure(form_id: str) -> dict:
    """指定されたGoogle Formsの構造（タイトル、質問項目など）を取得します。
    
    Args:
        form_id: Google FormsのID
        
    Returns:
        フォームの構造データの辞書（JSON表現）またはエラーメッセージ
    """
    import google.auth
    from googleapiclient.discovery import build

    SCOPES = ['https://www.googleapis.com/auth/forms.body.readonly', 'https://www.googleapis.com/auth/forms.body']
    
    try:
        # GOOGLE_APPLICATION_CREDENTIALS が設定されていれば、google.auth.default() で読み込まれる
        credentials, project = google.auth.default(scopes=SCOPES)
        service = build('forms', 'v1', credentials=credentials)
        
        result = service.forms().get(formId=form_id).execute()
        return result
    except Exception as e:
        return {"error": str(e)}


# FunctionToolとして登録
get_form_structure_tool = FunctionTool(func=get_form_structure)
