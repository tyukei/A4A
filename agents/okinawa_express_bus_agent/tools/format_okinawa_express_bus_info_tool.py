from google.adk.tools.function_tool import FunctionTool


def format_okinawa_express_bus_info(bus_data: dict) -> str:
    """沖縄の高速バス情報を整形して、人間が読みやすい形式で返します。

    Args:
        bus_data: 高速バス情報を含む辞書。以下のキーを想定します。
                  - "route_name": 路線名 (str, 例: "111番線")
                  - "from_naha_to_nago_timetable": 那覇空港発名護方面行きの時刻表情報 (str, 箇条書きなど)
                  - "from_nago_to_naha_timetable": 名護方面発那覇空港行きの時刻表情報 (str, 箇条書きなど)
                  - "fare_naha_nago": 那覇空港から名護方面の運賃情報 (str, 大人・子供、現金・ICカードなど詳細)
                  - "fare_nago_naha": 名護方面から那覇空港の運賃情報 (str, 大人・子供、現金・ICカードなど詳細)
                  - "boarding_naha": 那覇空港での高速バス乗り場案内 (str, 具体的な場所、地図情報など)
                  - "boarding_nago": 名護での高速バス乗り場/降り場案内 (str, 具体的な場所、地図情報など)
                  - "source_url": 公式情報源へのリンク (str)

    Returns:
        整形された高速バス情報の文字列。
    """
    output = []
    output.append(f"## 沖縄高速バス情報")

    if bus_data.get("route_name"):
        output.append(f"### 路線名: {bus_data['route_name']}")

    if bus_data.get("from_naha_to_nago_timetable"):
        output.append("\n### 那覇空港発 名護方面行き 時刻表")
        output.append(bus_data["from_naha_to_nago_timetable"])

    if bus_data.get("from_nago_to_naha_timetable"):
        output.append("\n### 名護方面発 那覇空港行き 時刻表")
        output.append(bus_data["from_nago_to_naha_timetable"])

    output.append("\n### 運賃")
    if bus_data.get("fare_naha_nago"):
        output.append(f"- 那覇空港 ⇄ 名護方面: {bus_data['fare_naha_nago']}")
    if bus_data.get("fare_nago_naha") and bus_data.get("fare_naha_nago") != bus_data.get("fare_nago_naha"):
        # 往復で情報が異なる場合のみ追記
        output.append(f"- 名護方面 ⇄ 那覇空港: {bus_data['fare_nago_naha']}")

    output.append("\n### 乗り場案内")
    if bus_data.get("boarding_naha"):
        output.append(f"- 那覇空港: {bus_data['boarding_naha']}")
    if bus_data.get("boarding_nago"):
        output.append(f"- 名護方面: {bus_data['boarding_nago']}")

    if bus_data.get("source_url"):
        output.append("\n### 情報源")
        output.append(f"- {bus_data['source_url']}")

    return "\n".join(output)


# FunctionToolとして登録
format_okinawa_express_bus_info_tool = FunctionTool(func=format_okinawa_express_bus_info)
