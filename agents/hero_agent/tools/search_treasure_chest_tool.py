from google.adk.tools.function_tool import FunctionTool

def search_treasure_chest() -> str:
    \"\"\"
    宝箱を探して中身をランダムに取得します。
    勇者がフィールドやダンジョンを探索する際に使用します。
    
    Returns:
        宝箱から見つけたアイテムの名前と説明
    \"\"\"
    import random
    
    items = [
        {"name": "やくそう", "desc": "傷を癒やす不思議な薬草。HPを少し回復する。"},
        {"name": "せいすい", "desc": "清らかな水。魔物を寄せ付けない効果がある。"},
        {"name": "どくけしそう", "desc": "毒を中和する薬草。体のしびれを治す。"},
        {"name": "キメラのつばさ", "desc": "一度行ったことのある町へ一瞬で戻れる羽。"},
        {"name": "50ゴールド", "desc": "旅の資金。宿屋に泊まるのに使おう。"},
        {"name": "てつのかぶと", "desc": "硬い鉄で作られた兜。守備力が上がる。"},
        {"name": "ふしぎなきのみ", "desc": "食べると最大MPが少し上がる不思議な実。"},
        {"name": "ちからのたね", "desc": "食べると攻撃力が少し上がる不思議な種。"},
        {"name": "ミミック！", "desc": "宝箱かと思ったら魔物だった！気をつけろ！"}
    ]
    
    found_item = random.choice(items)
    
    result = f"おおっと！ 宝箱を 見つけた！\n\n「{found_item['name']}」を 手に 入れた！\n({found_item['desc']})"
    return result


# FunctionToolとして登録
search_treasure_chest_tool = FunctionTool(func=search_treasure_chest)
