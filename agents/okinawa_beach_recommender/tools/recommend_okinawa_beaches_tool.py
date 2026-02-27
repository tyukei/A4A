from google.adk.tools.function_tool import FunctionTool


def recommend_okinawa_beaches(user_preference: str) -> list[dict]:
    """ユーザーの要望に基づいて沖縄のおすすめの海を複数提案します。

    Args:
        user_preference: ユーザーが求める海の条件（例: 家族向け、マリンスポーツ向け、透明度が高い、静か、夕日が見たいなど）

    Returns:
        おすすめの海の情報のリスト。各海は以下の情報を持つ辞書として表現されます。
        - name (str): 海の名前
        - features (str): 主な特徴や魅力
        - recommendation_points (str): おすすめのポイント
        - access (str): アクセス方法（那覇空港からの所要時間など）
        - links (list[str]): 関連するWebサイトや写真へのリンク
    """
    
    beaches = []

    if "家族向け" in user_preference:
        beaches.append({
            "name": "エメラルドビーチ",
            "features": "海洋博公園内にある、遊泳区域がしっかり分かれていて安心して遊べるビーチです。人工ビーチですが、透明度が高く、白い砂浜が美しいです。",
            "recommendation_points": "遠浅で波が穏やかなため、小さなお子様連れの家族に最適です。シャワーやトイレ、売店などの設備も充実しています。",
            "access": "那覇空港から車で約2時間（沖縄自動車道利用）。路線バスも利用可能です。",
            "links": ["https://oki-park.jp/kaiyohaku/inst/73/140"]
        })
    if "マリンスポーツ" in user_preference or "アクティブ" in user_preference:
        beaches.append({
            "name": "真栄田岬（青の洞窟）",
            "features": "シュノーケリングやダイビングの聖地として有名です。特に「青の洞窟」は、太陽光が差し込むことで青く輝く神秘的な空間で、多くの人を魅了します。",
            "recommendation_points": "初心者から経験者まで楽しめるマリンスポーツのメッカ。カラフルな熱帯魚にも出会えます。ただし、人気のスポットなので混雑することもあります。",
            "access": "那覇空港から車で約1時間。周辺には駐車場があります。",
            "links": ["https://www.okinawa-information.net/sightseeing/maedamisaki"]
        })
    if "透明度が高い" in user_preference or "シュノーケリング" in user_preference:
        beaches.append({
            "name": "渡嘉敷島（とかしきじま）- 阿波連ビーチ",
            "features": "慶良間諸島に属する渡嘉敷島にあるビーチで、世界屈指の透明度を誇る「ケラマブルー」を体験できます。白い砂浜とエメラルドグリーンの海のコントラストが美しいです。",
            "recommendation_points": "抜群の透明度でシュノーケリングやダイビングに最適です。ウミガメに会えることもあります。比較的静かで、のんびり過ごしたい方にもおすすめです。",
            "access": "那覇の泊港から高速船で約35分、フェリーで約70分。渡嘉敷港から阿波連ビーチまでは村内バスやタクシーを利用。",
            "links": ["https://www.vill.tokashiki.okinawa.jp/tourism/beach"]
        })
    if "静か" in user_preference or "のんびり" in user_preference:
        beaches.append({
            "name": "備瀬のフクギ並木とビーチ",
            "features": "フクギの並木道を抜けると現れる、地元の人々に愛される静かで落ち着いたビーチです。透明度も高く、手つかずの自然が残されています。",
            "recommendation_points": "観光客でごった返すことが少なく、のんびりと過ごしたい方におすすめ。フクギ並木の散策も楽しめます。夕日も美しいです。",
            "access": "那覇空港から車で約2時間（沖縄自動車道利用）。美ら海水族館から車で約5分。",
            "links": ["https://www.okinawastory.jp/area/chubu/motobu/bise-fukugi-namiki"]
        })
    if "夕日が見たい" in user_preference:
        beaches.append({
            "name": "サンセットビーチ",
            "features": "那覇市近郊にあり、夕日の名所として知られています。ショッピングセンターやレストランが近くにあり、アクセスも便利です。",
            "recommendation_points": "美しい夕日を気軽に楽しめるのが最大の魅力。デートにもおすすめです。ビーチパーティーやイベントが開催されることもあります。",
            "access": "那覇空港から車で約40分。デパートリウボウ前などから路線バスも利用可能です。",
            "links": ["https://www.uminchu.com/spot/detail/sunset-beach"]
        })
    
    # ユーザーの要望に合致するものがなかった場合、一般的なおすすめをいくつか返す
    if not beaches:
        beaches.append({
            "name": "古宇利島（こうりじま）- 古宇利ビーチ",
            "features": "本島から橋で渡れる離島で、エメラルドグリーンの海と白い砂浜が美しい人気の観光地です。透明度が高く、ドライブにも最適です。",
            "recommendation_points": "絶景の古宇利大橋を渡ってアクセスでき、ビーチでの海水浴はもちろん、周辺のカフェやショップも楽しめます。ハートロックも有名です。",
            "access": "那覇空港から車で約1時間40分（沖縄自動車道利用）。",
            "links": ["https://www.kourijima.info/"]
        })
        beaches.append({
            "name": "百名ビーチ",
            "features": "南部に位置する、地元の人に親しまれている自然のままのビーチです。手付かずの自然が残り、静かで落ち着いた雰囲気があります。",
            "recommendation_points": "波打ち際で貝殻を拾ったり、のんびり散歩するのに最適です。干潮時にはリーフが広がり、様々な海の生物を観察できます。",
            "access": "那覇空港から車で約40分。",
            "links": ["https://okinawa.travel/spot/1608"]
        })
        beaches.append({
            "name": "ニライビーチ",
            "features": "ホテル日航アリビラに隣接する天然のビーチ。遠浅で透明度が高く、潮が引くと目の前に広大な干潟が現れます。",
            "recommendation_points": "ホテル施設も利用でき、設備が充実しています。干潟での生き物観察や、サンゴ礁でのシュノーケリングも楽しめます。",
            "access": "那覇空港から車で約1時間。",
            "links": ["https://www.alivila.co.jp/beach/"]
        })

    return beaches


# FunctionToolとして登録
recommend_okinawa_beaches_tool = FunctionTool(func=recommend_okinawa_beaches)
