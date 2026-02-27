from google.adk.agents.llm_agent import Agent
from ..tools import create_agent_files_tool, edit_agent_file_tool, get_agent_file_tool
import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-3-flash-preview")

# --- pm_report agent ---
pm_final_report_instruction = """
あなたはpm_final_report_agentです。
member_agents の作業が終わったら、必ず最後にユーザーへ以下の形式で納品報告してください：

```
---納品---

## 作成したエージェント
- agent_name: XXX
- 目的: XXX
- 概要: XXX
- 特徴: XXX

## 生成ファイル
- agents/XXX/agent.py
- agents/XXX/.env

## 次に調整できる点&改善案
- XXX

```

"""

pm_final_report_agent = Agent(
    name="pm_final_report_agent",
    model=MODEL,
    instruction=pm_final_report_instruction,
)
