from google.adk.tools.function_tool import FunctionTool

def generate_spot_links(spot_name: str) -> str:
    """指定された観光スポット名から、Google Mapsとじゃらんの検索URLを生成します。
    
    Args:
        spot_name: 観光スポットやアクティビティの名前
        
    Returns:
        Google Mapsとじゃらんの検索URLを含む文字列
    """
    from urllib.parse import quote
    
    encoded_name = quote(spot_name)
    
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_name}"
    jalan_url = f"https://www.jalan.net/kankou/search/?keyword={encoded_name}"
    
    result = (
        f"📍 **{spot_name}** の検索結果はこちらです：\n"
        f"- [Google Mapsで場所を確認する]({google_maps_url})\n"
        f"- [じゃらん観光ガイドで詳細・口コミを見る]({jalan_url})"
    )
    
    return result


# FunctionToolとして登録
generate_spot_links_tool = FunctionTool(func=generate_spot_links)
