from google.adk.tools.function_tool import FunctionTool

def generate_search_urls(location_name: str) -> dict:
    """観光地名からGoogleマップとTripAdvisorの検索用URLを生成します。
    
    Args:
        location_name: 観光地やスポットの名前（例: 美ら海水族館、国際通り）
        
    Returns:
        GoogleマップとTripAdvisorのURLを含む辞書形式のデータ
    """
    from urllib.parse import quote
    
    # URLエンコード
    encoded_name = quote(location_name)
    
    # Google Maps 検索URL
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_name}"
    
    # TripAdvisor 検索URL
    tripadvisor_url = f"https://www.tripadvisor.jp/Search?q={encoded_name}"
    
    return {
        "google_maps": google_maps_url,
        "tripadvisor": tripadvisor_url
    }


# FunctionToolとして登録
generate_search_urls_tool = FunctionTool(func=generate_search_urls)
