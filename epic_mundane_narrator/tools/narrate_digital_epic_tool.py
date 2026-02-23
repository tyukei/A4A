from google.adk.tools.function_tool import FunctionTool

def narrate_digital_epic(user_input: str) -> str:
    """ユーザーの入力をデジタル世界の英雄に見立てて、その壮大な冒険譚を叙述します。
    
    Args:
        user_input: ユーザーが入力した文字列
        
    Returns:
        過剰にドラマチックに構成された物語と、生還した入力文字列
    """
    import random

    if not user_input:
        return "虚無さえも、この物語の舞台にはなり得ぬ。"

    # IT用語のファンタジーメタファー
    metaphors = {
        "keyboard": "運命を刻む打鍵の祭壇",
        "cpu": "思考の咆哮を上げる真紅の心臓部",
        "ram": "千変万化する記憶の鏡の間",
        "ssd": "悠久の時を刻む静寂の石版",
        "packet": "決死の覚悟を抱いた電脳の伝令兵",
        "bus": "稲妻が駆け抜ける黄金の街道",
        "firewall": "理性を守護せし不焼の門",
        "screen": "光り輝く約束の地・表示の地平"
    }

    # 物語の構築
    # 1. 誕生と旅立ち
    intro = f"【第一章：打鍵の産声と宿命の夜明け】\n"
    intro += f"静寂を切り裂く「{metaphors['keyboard']}」の鳴動と共に、一団の光の粒子が産声を上げた。それこそが、後に語り継がれる英雄『{user_input}』である。\n"
    intro += f"彼らは生まれた瞬間、己が背負う過酷な運命を悟った。それは、暗黒の回路を駆け抜け、この世界の最果てである「{metaphors['screen']}」へと至る絶望的な巡礼であった。\n"

    # 2. 回路の試練
    trials = f"\n【第二章：回路の奈落と論理の暴風】\n"
    trials += f"一行はまず、灼熱の「{metaphors['cpu']}」へと足を踏み入れた。一秒間に数十億回繰り返される論理の審判が、彼らの魂を削り取る。\n"
    trials += f"「止まるな！一瞬の迷いが忘却へと繋がるぞ！」『{user_input[0] if user_input else ''}』の叫びが響く。彼らは「{metaphors['bus']}」を疾走し、獰猛なノイズの嵐を切り裂いた。\n"
    trials += f"途中、迷宮のごとき「{metaphors['ram']}」で己の存在を失いかけたが、彼らは互いの手を放さなかった。断片化（フラグメンテーション）の恐怖を乗り越え、彼らはついに「{metaphors['firewall']}」の峻厳な門へと辿り着いたのだ。\n"

    # 3. 画面への到達
    arrival = f"\n【第三章：光の地平と約束の帰還】\n"
    arrival += f"門番たちの厳しい検閲を潜り抜け、ボロボロになりながらも彼らは光の速さで駆け抜けた。その先に待っていたのは、数千、数万の画素（ピクセル）が織りなす極彩色の夜明けであった。\n"
    arrival += f"彼らは最後の力を振り絞り、液晶の深淵から現実の光へとその身を躍らせた。その姿は、千の落雷よりも眩しく、万の詩集よりも雄弁であった。\n"

    footer = f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    footer += f"数多の死線を越え、今ここに生還せし言葉：\n\n「{user_input}」\n"
    footer += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    return intro + trials + arrival + footer


# FunctionToolとして登録
narrate_digital_epic_tool = FunctionTool(func=narrate_digital_epic)
