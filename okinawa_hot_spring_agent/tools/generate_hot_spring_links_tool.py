from google.adk.tools.function_tool import FunctionTool

def generate_hot_spring_links(facility_name: str) -> dict:
    """沖縄の温泉施設名から、Googleマップ（検索・ルート）とじゃらんの検索URLを生成します。
    
    Args:
        facility_name: 温泉施設名（例: 龍神の湯、シギラ黄金温泉）
        
    Returns:
        Googleマップ検索、ルート検索、じゃらん検索のURLを含む辞書
    """
    from urllib.parse import quote
    
    encoded_name = quote(facility_name)
    origin = quote("那覇空港")
    
    links = {
        "google_maps_search": f"https://www.google.com/maps/search/?api=1&query={encoded_name}",
        "google_maps_route": f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={encoded_name}&travelmode=driving",
        "jalan_search": f"https://www.jalan.net/uw/uwp2011/uww2011search.do?keyword={encoded_name}"
    }
    
    return links


# FunctionToolとして登録
generate_hot_spring_links_tool = FunctionTool(func=generate_hot_spring_links)
