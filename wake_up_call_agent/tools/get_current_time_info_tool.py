from google.adk.tools.function_tool import FunctionTool

def get_current_time_info() -> str:
    """Returns the current date and time in JST.
    
    Returns:
        Current time string formatted as YYYY-MM-DD HH:MM:SS
    """
    from datetime import datetime, timedelta, timezone
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    return now.strftime("%Y-%m-%d %H:%M:%S")


# FunctionToolとして登録
get_current_time_info_tool = FunctionTool(func=get_current_time_info)
