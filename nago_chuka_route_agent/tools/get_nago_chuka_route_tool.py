from google.adk.tools.function_tool import FunctionTool


def get_nago_chuka_route(destination_name: str, destination_address: str) -> str:
    """沖縄県名護市役所から指定された町中華までのGoogle Mapsルートリンクを生成します。

    Args:
        destination_name: 目的地の町中華の店名
        destination_address: 目的地の町中華の住所

    Returns:
        Google Mapsのルートリンク
    """
    from urllib.parse import quote

    origin = "沖縄県名護市役所"
    encoded_origin = quote(origin)
    encoded_destination = quote(f"{destination_name}, {destination_address}")
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_destination}&travelmode=driving"
    return maps_url


# FunctionToolとして登録
get_nago_chuka_route_tool = FunctionTool(func=get_nago_chuka_route)
