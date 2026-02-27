from google.adk.tools.function_tool import FunctionTool


def generate_useless_message() -> str:
    """最も無駄なメッセージを生成します。

    Returns:
        常に同じ無駄なメッセージ
    """
    return "今日も一日、特に何もせず、しかし確実に存在しています。"


# FunctionToolとして登録
generate_useless_message_tool = FunctionTool(func=generate_useless_message)
