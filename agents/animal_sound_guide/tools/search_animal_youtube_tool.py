from google.adk.tools.function_tool import FunctionTool


def search_animal_youtube(animal_name: str) -> str:
    """指定された動物の鳴き声に関するYouTube動画を検索します。

    Args:
        animal_name: 動物の名前（例: 犬、猫、ライオン）

    Returns:
        YouTube検索結果のURL
    """
    from urllib.parse import quote

    search_query = f"{animal_name} 鳴き声"
    encoded_query = quote(search_query)
    youtube_search_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    return f"【{animal_name}の鳴き声】YouTube検索結果: {youtube_search_url}"


# FunctionToolとして登録
search_animal_youtube_tool = FunctionTool(func=search_animal_youtube)
