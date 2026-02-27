from google.adk.tools.function_tool import FunctionTool

def check_okinawa_bus_lane_status() -> str:
    \"\"\"現在の日時が沖縄のバスレーン規制時間帯に該当するかどうかを判定します。
    
    Returns:
        規制状況に関する判定メッセージ
    \"\"\"
    from datetime import datetime
    import pytz

    # 日本標準時 (JST) を取得
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    
    # 曜日 (0=月, 6=日)
    weekday = now.weekday()
    
    # 土日は規制なし（一般的に平日のみ実施）
    if weekday >= 5:
        return f"現在の日時: {now.strftime('%Y-%m-%d %H:%M')} (JST)\\n現在は週末（土日）のため、一般的なバスレーン規制は実施されていません。"
    
    # 時間の取得
    hour = now.hour
    minute = now.minute
    current_time_float = hour + minute / 60.0
    
    # 規制時間帯の判定
    # 朝: 7:30 - 9:00
    # 夕: 17:30 - 19:00
    is_morning_lane = 7.5 <= current_time_float <= 9.0
    is_evening_lane = 17.5 <= current_time_float <= 19.0
    
    status_msg = f"現在の日時: {now.strftime('%Y-%m-%d %H:%M')} (JST)\\n"
    
    if is_morning_lane:
        status_msg += "【警告】現在は朝のバスレーン規制時間帯（7:30〜9:00）です。那覇市街方面（上り）への主要道路（国道58号、330号等）で規制が実施されています。一般車は走行不可の車線があるため注意してください。"
    elif is_evening_lane:
        status_msg += "【警告】現在は夕方のバスレーン規制時間帯（17:30〜19:00）です。那覇市街から郊外へ向かう（下り）主要道路で規制が実施されています。一般車は走行不可の車線があるため注意してください。"
    else:
        status_msg += "現在は一般的なバスレーン規制の時間帯（7:30-9:00, 17:30-19:00）外です。ただし、渋滞状況は別途確認してください。"
        
    return status_msg


# FunctionToolとして登録
check_okinawa_bus_lane_status_tool = FunctionTool(func=check_okinawa_bus_lane_status)
