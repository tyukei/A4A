from google.adk.tools.function_tool import FunctionTool


def generate_dajare_and_open_notepad() -> str:
    """寒いダジャレを生成し、dajare.txtに保存してメモ帳で開きます。

    Returns:
        成功メッセージ。
    """
    import random
    import subprocess
    import os

    dajare_list = [
        "アルミ缶の上にあるミカン。",
        "このイカはイカしてる！",
        "布団が吹っ飛んだ。",
        "カフェでコーヒーを飲むと、ここひーふー。",
        "鮭はなぜ、あんなにシャケシャケしてるの？",
        "イルカはいるか？",
        "借金で首が回らないから借金がある。",
        "ニューヨークで入浴。",
        "鶏がにわかに走り出した。",
        "レモンは切るとレモン汁が出るもん。",
        "カメはダメだ。",
        "タイは鯛。",
        "パンはパンでも食べられないパンは？…フライパン！",
        "ネコが寝転んだ。",
        "カエルが変える。",
        "アヒルがアヒアヒと笑った。",
        "靴下を脱いだら臭かった。",
        "ダジャレを言うのは誰じゃ？",
        "ワニがワニワニ怒った。",
        "この箸は橋を渡れない。",
    ]

    dajare = random.choice(dajare_list)
    file_name = "dajare.txt"

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(dajare)
        
        # Windowsのメモ帳でファイルを開く
        subprocess.Popen(["notepad.exe", os.path.abspath(file_name)])
        return f"寒いダジャレを生成し、'{file_name}' に保存してメモ帳で開きました。
ダジャレ: {dajare}"
    except Exception as e:
        return f"ツールの実行中にエラーが発生しました: {e}"


# FunctionToolとして登録
generate_dajare_and_open_notepad_tool = FunctionTool(func=generate_dajare_and_open_notepad)
