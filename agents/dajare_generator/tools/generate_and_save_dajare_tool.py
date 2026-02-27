from google.adk.tools.function_tool import FunctionTool


def generate_and_save_dajare() -> str:
    """ランダムな寒いダジャレを生成し、「dajare.txt」に保存します。
    ファイルはUTF-8でエンコードされ、文字化けを防ぎます。

    Returns:
        生成されたダジャレがファイルに保存されたことを示すメッセージ。
    """
    import random
    import os

    # 寒いダジャレのリスト
    dajare_list = [
        "アルミ缶の上にあるみかん。",
        "サイダーを飲んだら、そうだー！と叫んだ。",
        "このイクラはいくら？",
        "カレーは辛え！",
        "紅茶を飲んで、もうこーちゃった。",
        "トイレに行っといれ！",
        "ニューヨークで入浴。",
        "チーターが、走るのちーと速い。",
        "おっと、落とし物だよ。オートー！",
        "パンダのパンだ。",
        "蚊がカーッと怒った。",
        "イルカはいるか？",
        "ダジャレを言うのは誰じゃ？",
        "レモンを割ったら、レモンの香り。",
    ]

    # リストからランダムに1つダジャレを選択
    selected_dajare = random.choice(dajare_list)

    # dajare.txtファイルにダジャレをUTF-8で書き込む
    file_path = "dajare.txt"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(selected_dajare)
        return f"寒いダジャレを生成し、'{file_path}'に保存しました: '{selected_dajare}'"
    except IOError as e:
        return f"ファイルの書き込み中にエラーが発生しました: {e}"



# FunctionToolとして登録
generate_and_save_dajare_tool = FunctionTool(func=generate_and_save_dajare)
