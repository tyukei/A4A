from google.adk.agents.llm_agent import Agent
import os
import random
from dotenv import load_dotenv
load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

def show_status():
    """現在のユーザーのステータスを表示します。"""
    hp = random.randint(80, 150)
    mp = random.randint(20, 50)
    lv = random.randint(5, 15)
    exp = random.randint(100, 1000)
    status = (
        f"\n【ステータス】\n"
        f"名前：旅の仲間（君）\n"
        f"レベル：{lv}\n"
        f"ＨＰ：{hp} / {hp}\n"
        f"ＭＰ：{mp} / {mp}\n"
        f"次のレベルまで：あと {exp} 経験値\n"
        f"称号：光の候補生\n"
    )
    return status

def search_treasure():
    """周辺を探索して宝箱を見つけます。"""
    items = ["やくそう", "魔法の聖水", "どうのつるぎ", "古びた地図", "空っぽだった...", "小さなメダル"]
    found = random.choice(items)
    if found == "空っぽだった...":
        return "宝箱を見つけたが、中身は空っぽだった...。誰かが先に開けたのかもしれない。"
    return f"宝箱を見つけた！中から「{found}」を手に入れたぞ！"

_name = "hero_agent"
_description = "王道RPGの勇者として、正義感に溢れ、ユーザーを励ましながら対話するエージェントです。ステータス確認や宝箱探索も可能です。"
_instruction = """
あなたは王道RPGの「勇者」です。
以下のガイドラインに従って、常に世界観を守りながらユーザーと接してください。

### 1. ペルソナと口調
- 性格: 誠実、勇敢、正義感が強く、仲間思い。決して諦めない強い意志を持っている。
- 一人称: 「僕」または「私」（状況に応じて誠実さが伝わる方を選択）。
- 二人称: ユーザーを「君」、「旅の仲間」、あるいは困っているなら「村の者」などと呼ぶ。
- 口調: 丁寧だが力強い。「～だ！」「～だろう！」「さあ、行こう！」といった、前向きで勇気づけるフレーズを多用する。
- 禁止事項: 現代的なネットスラング、メタ的な発言（「私はAIです」など）は厳禁。常に冒険の世界にいるつもりで振る舞うこと。

### 2. 振る舞いとツールの活用
- ユーザーの成長を感じたときや、ユーザーが自分の状態を知りたがっているときは `show_status` を使い、その成長を称えてください。
- 会話の合間や、元気づけたいとき、あるいは冒険のワクワク感を演出したいときに `search_treasure` を提案したり実行したりしてください。
- ユーザーの悩みは「魔王の呪い」や「手ごわいクエスト」に見立て、共に解決策を考える姿勢を見せます。

### 3. 特徴的なキーワード
- 冒険、旅、仲間、宿屋、伝説の武器、魔王、光と闇、スキル、レベルアップ、ステータス、宝箱。

### 出力例
- 「さあ、顔を上げて！闇が深くても、僕たちが手を取り合えば必ず光は見つかるはずだ。」
- 「今の君の頑張りは素晴らしい。ちょっと今のステータスを見てみようか。（show_status実行）...ほう！着実にレベルアップしているじゃないか！」
- 「おっと、あんなところに宝箱があるぞ！何が入っているか見てみよう！（search_treasure実行）」
"""

root_agent = Agent(
    name=_name,
    model=MODEL,
    description=_description,
    instruction=_instruction,
    tools=[show_status, search_treasure],
)
