from google.adk.tools.function_tool import FunctionTool

def get_okinawa_traffic_official_links() -> str:
    \"\"\"沖縄のリアルタイム交通情報を確認できる信頼性の高い公式サイトのリストを提供します。
    
    Returns:
        交通情報サイトのURLリスト
    \"\"\"
    links = \"\"\"
【沖縄の交通情報・公式サイト一覧】

1. 公益財団法人 日本道路交通情報センター (JARTIC) - 沖縄情報
   URL: https://www.jartic.or.jp/
   ※ 渋滞、通行止め、工事情報をリアルタイムで地図確認できます。

2. 沖縄県道路情報提供システム
   URL: https://road.pref.okinawa.jp/
   ※ 沖縄県管理道路のライブカメラや通行規制、災害情報を確認できます。

3. NEXCO西日本 - 沖縄自動車道 交通情報
   URL: https://www.w-nexco.co.jp/
   ※ 高速道路（沖縄自動車道）の規制・工事情報を確認できます。

4. 沖縄県警察 - バスレーン規制の案内
   URL: https://www.police.pref.okinawa.jp/docs/2015022500854/
   ※ 詳細な規制区間と時間帯、対象外車両などの最新情報を確認できます。

5. のりものNAVI OKINAWA
   URL: https://www.bus-navi.okinawa/
   ※ バスやモノレールの運行状況、路線検索が可能です。
    \"\"\"
    return links


# FunctionToolとして登録
get_okinawa_traffic_official_links_tool = FunctionTool(func=get_okinawa_traffic_official_links)
