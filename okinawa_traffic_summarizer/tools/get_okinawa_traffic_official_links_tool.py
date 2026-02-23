from google.adk.tools.function_tool import FunctionTool

def get_okinawa_traffic_official_links() -> dict:
    """沖縄の主要な交通情報提供サイトのURLリストを返します。
    
    Returns:
        dict: 各種交通情報のソースURL（JARTIC、沖縄県警察、高速道路など）
    """
    links = {
        "JARTIC_Okinawa": "https://www.jartic.or.jp/guide/shisetsu.html", # 施設情報ページ等への誘導
        "JARTIC_Realtime": "https://www.jartic.or.jp/", # トップから沖縄を選択
        "Okinawa_Pref_Police_Traffic": "https://www.pref.okinawa.jp/kenkei/kotu/kisei/index.html",
        "Okinawa_Expressway_NEXCO": "https://www.w-nexco.co.jp/realtime/",
        "Ryukyu_Shimpo_Traffic": "https://ryukyushimpo.jp/tag/%E4%BA%A4%E9%80%9A%E6%83%85%E5%A0%B1",
        "Okinawa_Times_Traffic": "https://www.okinawatimes.co.jp/category/news-traffic"
    }
    return links


# FunctionToolとして登録
get_okinawa_traffic_official_links_tool = FunctionTool(func=get_okinawa_traffic_official_links)
