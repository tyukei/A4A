from google.adk.tools.function_tool import FunctionTool

def generate_okinawa_traffic_map_url(area: str = "沖縄県") -> str:
    \"\"\"指定されたエリアのGoogleマップ渋滞状況表示URLを生成します。
    
    Args:
        area: 表示したいエリア名（例：「那覇市」「国道58号」「沖縄市」など）
        
    Returns:
        str: Google Mapsの渋滞レイヤー付きURL
    \"\"\"
    from urllib.parse import quote
    base_url = "https://www.google.com/maps/search/"
    query = quote(f"{area} 交通状況")
    # layer=t は渋滞状況を表示するパラメータ（URLパラメータとして直接指定できない場合が多いため、検索結果からの遷移を想定）
    return f"{base_url}{query}"


# FunctionToolとして登録
generate_okinawa_traffic_map_url_tool = FunctionTool(func=generate_okinawa_traffic_map_url)
