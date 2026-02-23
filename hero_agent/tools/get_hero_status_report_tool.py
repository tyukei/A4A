from google.adk.tools.function_tool import FunctionTool

def get_hero_status_report(name: str, level: int = 1, job: str = "勇者", hp: int = 100, mp: int = 50) -> str:
    \"\"\"
    勇者のステータス画面を王道RPG風のテキスト形式で生成します。
    
    Args:
        name: 勇者の名前（ユーザー名など）
        level: 現在のレベル
        job: 職業（デフォルトは「勇者」）
        hp: 現在の体力
        mp: 現在の魔力
        
    Returns:
        王道RPG風のステータスウィンドウ文字列
    \"\"\"
    status_window = f\"\"\"
┌──────────────────────────────────────┐
│  【 ステータス 】                    │
├──────────────────────────────────────┤
│  なまえ： {name:<10}         │
│  しょくぎょう： {job:<8}           │
│  レベル： {level:>3}                        │
├──────────────────────────────────────┤
│  ＨＰ： {hp:>3} / {hp:>3}                  │
│  ＭＰ： {mp:>3} / {mp:>3}                  │
├──────────────────────────────────────┤
│  そうび： ひのきのぼう               │
│          ぬののふく                 │
└──────────────────────────────────────┘
\"\"\"
    return status_window.strip()


# FunctionToolとして登録
get_hero_status_report_tool = FunctionTool(func=get_hero_status_report)
