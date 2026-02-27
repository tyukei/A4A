from google.adk.tools.function_tool import FunctionTool

def get_hot_spring_urls(facility_name: str) -> str:
    """沖縄の温泉施設のGoogle Maps検索、ルート検索、じゃらん検索のURLを生成します。
    
    Args:
        facility_name: 温泉施設の名前（例: 龍神の湯、シギラ黄金温泉）
        
    Returns:
        各検索サイトのURLを含む文字列
    """
    from urllib.parse import quote
    
    encoded_name = quote(facility_name)
    google_maps_search = f"https://www.google.com/maps/search/?api=1&query={encoded_name}"
    google_maps_route = f"https://www.google.com/maps/dir/?api=1&origin=Naha+Airport&destination={encoded_name}"
    jalan_search = f"https://www.jalan.net/uw/uwp2011/uww2011search.do?keyword={encoded_name}"
    
    return (
        f"【{facility_name} の関連リンク】\n"
        f"・Google Maps 検索: {google_maps_search}\n"
        f"・Google Maps ルート（那覇空港発）: {google_maps_route}\n"
        f"・じゃらん 検索: {jalan_search}"
    )


# FunctionToolとして登録
get_hot_spring_urls_tool = FunctionTool(func=get_hot_spring_urls)
