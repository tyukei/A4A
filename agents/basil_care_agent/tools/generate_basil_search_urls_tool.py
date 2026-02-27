from google.adk.tools.function_tool import FunctionTool

def generate_basil_search_urls(keyword: str) -> str:
    \"\"\"バジルの育て方に関する検索URLを生成します。
    
    Args:
        keyword: 検索したいキーワード（例: バジル 摘心, バジル 虫）
        
    Returns:
        Google, YouTube, および主要な園芸サイトの検索結果URL
    \"\"\"
    from urllib.parse import quote
    
    encoded_keyword = quote(keyword)
    
    google_url = f"https://www.google.com/search?q={encoded_keyword}"
    youtube_url = f"https://www.youtube.com/results?search_query={encoded_keyword}"
    lovegreen_url = f"https://lovegreen.net/?s={encoded_keyword}"
    sc_engei_url = f"https://www.sc-engei.co.jp/search/search.php?key={encoded_keyword}"
    
    result = (
        f"「{keyword}」の検索結果へのリンクを作成しました：\n\n"
        f"- [Google 検索]({google_url})\n"
        f"- [YouTube 検索]({youtube_url})\n"
        f"- [園芸情報サイト LOVEGREEN]({lovegreen_url})\n"
        f"- [住友化学園芸（害虫・病気など）]({sc_engei_url})"
    )
    return result


# FunctionToolとして登録
generate_basil_search_urls_tool = FunctionTool(func=generate_basil_search_urls)
