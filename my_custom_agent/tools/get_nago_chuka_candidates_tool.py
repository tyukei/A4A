from google.adk.tools.function_tool import FunctionTool


def get_nago_chuka_candidates() -> list:
    """沖縄県名護市役所周辺の町中華候補を返します（試作用のダミーデータ）。

    Returns:
        候補リスト。各要素は店情報の辞書（name/address/opening_hours/rating）です。
    """
    return [
        {
            "name": "中華料理 美味",
            "address": "沖縄県名護市大北1丁目13-13",
            "opening_hours": "11:00～22:00",
            "rating": "3.8",
        },
        {
            "name": "町中華 龍鳳",
            "address": "沖縄県名護市城1丁目3-3",
            "opening_hours": "11:30～14:30, 17:00～21:00",
            "rating": "4.1",
        },
        {
            "name": "名護飯店",
            "address": "沖縄県名護市宮里1丁目2-5",
            "opening_hours": "10:00～20:00",
            "rating": "3.5",
        },
    ]


get_nago_chuka_candidates_tool = FunctionTool(func=get_nago_chuka_candidates)

