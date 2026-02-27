from google.adk.tools.function_tool import FunctionTool

def send_line_notification(message: str) -> str:
    """Sends a push notification message via LINE Messaging API.
    Required environment variables: LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID.
    
    Args:
        message: The message text to send.
        
    Returns:
        A string indicating the result of the operation.
    """
    import os
    import requests
    import json

    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    if not token:
        return "Error: LINE_CHANNEL_ACCESS_TOKEN is not set."
    if not user_id:
        return "Error: LINE_USER_ID is not set."

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            return f"Successfully sent LINE notification: {message}"
        else:
            return f"Failed to send LINE notification. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"An error occurred while sending LINE notification: {str(e)}"


# FunctionToolとして登録
send_line_notification_tool = FunctionTool(func=send_line_notification)
