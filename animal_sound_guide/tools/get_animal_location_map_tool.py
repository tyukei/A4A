from google.adk.tools.function_tool import FunctionTool


def get_animal_location_map(animal_name: str, location_name: str) -> str:
    """那覇空港から指定された場所までのGoogle Mapsルートリンクを生成します。

    Args:
        animal_name: 動物の名前（例: イリオモテヤマネコ、ヤンバルクイナ、ジンベエザメ）
        location_name: 目的地の名前（例: 美ら海水族館、ヤンバルクイナ生態展示学習施設）

    Returns:
        Google Mapsのルートリンク
    """
    from urllib.parse import quote

    origin = "那覇空港"
    encoded_origin = quote(origin)
    encoded_destination = quote(location_name)
    maps_url = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={encoded_origin}"
        f"&destination={encoded_destination}"
        f"&travelmode=driving"
    )

    return f"【{animal_name}が見られる場所へのルート】\n那覇空港 → {location_name}\n {maps_url}"


# FunctionToolとして登録
get_animal_location_map_tool = FunctionTool(func=get_animal_location_map)
