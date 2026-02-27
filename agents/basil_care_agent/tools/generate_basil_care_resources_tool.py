from google.adk.tools.function_tool import FunctionTool

def generate_basil_care_resources(keyword: str) -> str:
    """バジルの育て方に関する検索URLと一般的なアドバイスを生成します。
    
    Args:
        keyword: 検索キーワード（例：「水やり」「摘心」「収穫」）
        
    Returns:
        アドバイスと検索URLを含むテキスト
    """
    from urllib.parse import quote
    
    # 検索用のクエリを作成
    search_query = f"バジル {keyword}"
    encoded_query = quote(search_query)
    
    # URLの生成
    urls = {
        "Google検索": f"https://www.google.com/search?q={encoded_query}",
        "YouTube検索": f"https://www.youtube.com/results?search_query={encoded_query}",
        "LOVEGREEN": f"https://lovegreen.net/?s={encoded_query}",
        "住友化学園芸": f"https://www.sc-engei.co.jp/search/list.html?kw={encoded_query}",
        "サカタのタネ": f"https://www.sakatano-tane.co.jp/search/index.html?q={encoded_query}"
    }
    
    # キーワードに基づく簡易的な栽培アドバイス
    advice = "【一般的な栽培アドバイス】\n"
    if "水" in keyword:
        advice += "・バジルは水を好みます。土の表面が乾いたら鉢底から流れるくらいたっぷりと水を与えてください。\n・特に夏場は水切れを起こしやすいので、朝晩の2回確認するのがおすすめです。"
    elif any(k in keyword for k in ["摘心", "剪定", "わき芽", "脇芽"]):
        advice += "・草丈が15〜20cm程度になったら、一番上の芽を摘み取る「摘心」を行いましょう。\n・摘心することで脇芽が伸び、枝数が増えて収穫量もアップします。"
    elif any(k in keyword for k in ["収穫", "保存"]):
        advice += "・必要な分をその都度摘み取ります。花芽がつくと葉が硬くなり風味が落ちるので、早めに摘み取るのがコツです。\n・大量に収穫した場合は、バジルソース（ジェノベーゼ）にしたり、乾燥させて保存するのも良いでしょう。"
    elif any(k in keyword for k in ["虫", "病気", "アブラムシ", "ハダニ"]):
        advice += "・アブラムシやハダニが発生しやすいです。風通しを良くし、見つけ次第取り除いてください。\n・食用にする場合は、食品成分由来の殺虫剤などを使用するか、こまめに霧吹きで葉裏を洗うのが効果的です。"
    elif any(k in keyword for k in ["土", "肥料", "追肥"]):
        advice += "・水はけが良く、有機質の豊富な土を好みます。市販の「野菜の土」で十分育ちます。\n・生育が旺盛なので、2週間に1回程度、薄めた液体肥料か置き肥をバランス良く与えましょう。"
    elif any(k in keyword for k in ["冬", "越冬", "温度"]):
        advice += "・バジルは熱帯原産で寒さに非常に弱いです。15度を下回るようになると生育が鈍ります。\n・日本では一年草として扱われますが、冬越しさせる場合は室内の暖かい日向に移動させてください。"
    else:
        advice += "・バジルは日光が大好きです。日当たりの良い場所（1日5時間以上が理想）で育てましょう。\n・風通しが悪いと蒸れて病気になりやすいので、株同士の間隔を空けることも大切です。"

    # メッセージの組み立て
    response = f"「{keyword}」に関する情報ですね。以下の知識とリンクを参考にしてください。\n\n"
    response += advice + "\n\n"
    response += "【詳細を調べるためのリンク】\n"
    for site, url in urls.items():
        response += f"- {site}: {url}\n"
    
    return response


# FunctionToolとして登録
generate_basil_care_resources_tool = FunctionTool(func=generate_basil_care_resources)
