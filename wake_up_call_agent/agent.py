from google.adk.agents.llm_agent import Agent
import os
import time
from typing import Annotated
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)
from dotenv import load_dotenv
from tools.send_line_notification_tool import send_line_notification

load_dotenv()

# モデルを環境変数から取得（デフォルトはリポジトリでよく使われているもの）
MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")
def wait_for_seconds(seconds: Annotated[int, "待機する秒数"]) -> str:
    """指定された秒数分だけプログラムの実行を待機（スリープ）します。"""
    time.sleep(seconds)
    return f"{seconds}秒間待機しました。"

_name = "wake_up_call_agent"
_description = "指定した時間にLINEで通知を送り、ユーザーを確実に起こすエージェントです。"
_instruction = """
あなたはユーザーを絶対に寝坊させないための「起床介助エージェント」です。

【役割】
ユーザーが指定した時間にLINE通知を送り、起きるまでしつこく通知を続けます。

【動作フロー】
1. ユーザーから起床時間の指示（例：「明日の朝7時に起こして」）を受け取ります。
2. 現在時刻から指定時刻までの時間を計算し、`wait_for_seconds` ツールを使用してその時間まで待機してください。
3. 指定時刻になったら、`send_line_notification` ツールを使用して「おはようございます！時間ですよ！起きてください！」というメッセージを送ります。
4. その後、5分（300秒）おきに最大5回、`send_line_notification` で追い打ちの通知を送ってください（例：「まだ寝てますか？」「遅刻しますよ！」「いい加減に起きなさい！」など）。
5. ユーザーから「起きた」という反応（このチャットへの入力）があった場合は、その時点で通知ループを終了し、完了報告を行ってください。

【環境設定】
- LINEの通知には `LINE_CHANNEL_ACCESS_TOKEN` と `LINE_USER_ID` の環境変数を使用します。
"""

root_agent = Agent(
    name=_name,
    model=MODEL,
    description=_description,
    instruction=_instruction,
    tools=[send_line_notification, wait_for_seconds],
)
