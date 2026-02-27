from google.adk.tools.function_tool import FunctionTool

def get_animal_sound_info(animal_name: str) -> dict:
    """指定された動物の鳴き声表現、説明、およびYouTubeの検索リンクを取得します。
    
    Args:
        animal_name: 動物の名前（例：ライオン、イヌ、ネコ）
        
    Returns:
        動物の鳴き声情報（擬音語、説明、YouTube検索URL）を含む辞書
    """
    from urllib.parse import quote
    
    # 主要な動物のデータ
    animal_data = {
        "イヌ": {"sound": "ワンワン", "desc": "元気によく吠えます。"},
        "ネコ": {"sound": "ニャー", "desc": "甘えたり、お腹が空いたときに鳴きます。"},
        "ライオン": {"sound": "ガオー", "desc": "百獣の王らしい、迫力のある鳴き声です。"},
        "ゾウ": {"sound": "パオーン", "desc": "長い鼻を使って高く響く音を出します。"},
        "ヒツジ": {"sound": "メーメー", "desc": "のどかな牧場で聞こえてくる鳴き声です。"},
        "ウマ": {"sound": "ヒヒーン", "desc": "いななきと呼ばれ、力強い声です。"},
        "ニワトリ": {"sound": "コケコッコー", "desc": "朝一番に鳴いて時間を知らせてくれます。"},
        "カエル": {"sound": "ケロケロ", "desc": "雨の日や夜の田んぼでよく聞こえます。"},
        "パンダ": {"sound": "メー / ワン", "desc": "意外かもしれませんが、羊や犬に近い声で鳴くことがあります。"},
        "ペンギン": {"sound": "ガーガー / クワッ", "desc": "種類によりますが、ラッパのような声で鳴きます。"},
        "キリン": {"sound": "（ほとんど鳴かない）", "desc": "滅多に鳴きませんが、鼻を鳴らすような音を出すことがあります。"},
        "カラス": {"sound": "カーカー", "desc": "賢い鳥で、仲間との合図に鳴きます。"},
        "フクロウ": {"sound": "ホーホー", "desc": "夜の森で静かに響く鳴き声です。"},
        "サル": {"sound": "ウキー", "desc": "仲間とコミュニケーションをとるために騒がしく鳴きます。"},
        "トラ": {"sound": "グルルル / ガオー", "desc": "低い唸り声から激しい咆哮まで様々です。"},
        "ウシ": {"sound": "モーモー", "desc": "のんびりとした低い鳴き声です。"},
        "ブタ": {"sound": "ブーブー", "desc": "鼻を鳴らして鳴きます。"},
        "ヤギ": {"sound": "メー", "desc": "ヒツジより少し高い声で鳴くことが多いです。"},
        "セミ": {"sound": "ミーンミーン", "desc": "夏を象徴する鳴き声ですね。"},
        "スズムシ": {"sound": "リンリン", "desc": "秋の夜に美しく響く鳴き声です。"}
    }

    # 辞書から情報を取得。見つからない場合はデフォルト値。
    info = animal_data.get(animal_name)
    
    if info:
        sound = info["sound"]
        description = info["desc"]
    else:
        sound = "（詳しく調べてみてね！）"
        description = f"{animal_name}の鳴き声はどんな音かな？一緒にYouTubeで確認してみよう！"

    # YouTubeの検索リンクを生成（捏造を避けるため検索結果URLを推奨）
    search_query = f"{animal_name} 鳴き声"
    youtube_link = f"https://www.youtube.com/results?search_query={quote(search_query)}"
    
    return {
        "animal": animal_name,
        "sound": sound,
        "description": description,
        "youtube_url": youtube_link
    }


# FunctionToolとして登録
get_animal_sound_info_tool = FunctionTool(func=get_animal_sound_info)
