from google.adk.tools.function_tool import FunctionTool

def generate_search_urls(keywords: str) -> dict:
    """ユーザーの質問や文脈から生成されたキーワードをもとに、Google検索とYouTube検索のURLを生成します。
    
    Args:
        keywords: 検索に使用するキーワード（例: 「バジル 摘心 方法」「バジル プランター 追肥」）
        
    Returns:
        Google検索URLとYouTube検索URLを含む辞書
    """
    from urllib.parse import quote
    
    encoded_keywords = quote(keywords)
    google_url = f"https://www.google.com/search?q={encoded_keywords}"
    youtube_url = f"https://www.youtube.com/results?search_query={encoded_keywords}"
    
    return {
        "google_search_url": google_url,
        "youtube_search_url": youtube_url
    }


# FunctionToolとして登録
generate_search_urls_tool = FunctionTool(func=generate_search_urls)
