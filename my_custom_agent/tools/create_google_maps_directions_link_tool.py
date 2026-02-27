from google.adk.tools.function_tool import FunctionTool


def create_google_maps_directions_link(
    origin: str,
    destination: str,
    travelmode: str = "driving",
) -> str:
    """Google Mapsの経路リンク（Directions URL）を生成します。

    Args:
        origin: 出発地（例: "沖縄県名護市役所"）
        destination: 目的地（例: "中華料理 美味, 沖縄県名護市大北1丁目13-13"）
        travelmode: 移動手段。driving / walking / bicycling / transit のいずれか。

    Returns:
        Google Mapsの経路リンクURL
    """
    from urllib.parse import quote

    allowed = {"driving", "walking", "bicycling", "transit"}
    mode = travelmode if travelmode in allowed else "driving"

    encoded_origin = quote(origin)
    encoded_destination = quote(destination)
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={encoded_origin}"
        f"&destination={encoded_destination}"
        f"&travelmode={mode}"
    )


create_google_maps_directions_link_tool = FunctionTool(func=create_google_maps_directions_link)

