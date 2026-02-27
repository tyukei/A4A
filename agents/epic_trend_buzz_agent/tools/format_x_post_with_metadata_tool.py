from google.adk.tools.function_tool import FunctionTool

def format_x_post_with_metadata(content: str, trends: list) -> str:
    """作成された物語をXの投稿形式に整え、文字数チェックとトレンドハッシュタグの付与を行います。
    
    Args:
        content: 投稿本文
        trends: 関連付けたいトレンドワードのリスト
        
    Returns:
        整形済み投稿内容
    """
    def count_chars(text):
        count = 0
        for char in text:
            if ord(char) <= 127:
                count += 0.5
            else:
                count += 1
        return count

    formatted_content = content + "\n\n"
    for trend in trends[:2]:
        tag = trend.replace(" ", "").replace("#", "")
        formatted_content += f"#{tag} "
    
    char_count = count_chars(formatted_content)
    
    status = "【OK】" if char_count <= 140 else "【文字数オーバー】"
    return f"--- 投稿案 ---\n{formatted_content}\n--------------\n判定: {status} (約{int(char_count)}文字)"


# FunctionToolとして登録
format_x_post_with_metadata_tool = FunctionTool(func=format_x_post_with_metadata)
