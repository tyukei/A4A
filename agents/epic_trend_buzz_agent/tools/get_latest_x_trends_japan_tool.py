from google.adk.tools.function_tool import FunctionTool

def get_latest_x_trends_japan() -> str:
    """日本のX（旧Twitter）で現在トレンド入りのワードを取得します。
    
    Returns:
        トレンドワードのリスト（文字列形式）
    """
    import urllib.request
    import re

    url = "https://twittrend.jp/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
            
            # twittrend.jp の構造に基づき、リンクテキスト部分を抽出
            pattern = r'<a href="/trend/[^"]+">([^<]+)</a>'
            trends = re.findall(pattern, html)
            
            unique_trends = []
            for t in trends:
                if t not in unique_trends:
                    unique_trends.append(t)
            
            if not unique_trends:
                return "トレンドワードを取得できませんでした。"
                
            return "現在のトレンドワード: " + ", ".join(unique_trends[:20])

    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


# FunctionToolとして登録
get_latest_x_trends_japan_tool = FunctionTool(func=get_latest_x_trends_japan)
