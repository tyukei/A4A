from google.adk.agents.llm_agent import Agent
from google.adk.agents import ParallelAgent, SequentialAgent
from .subagents import creater_agent, surfer_agent, searcher_agent, reviewer_agent, pm_final_report_agent, tool_creater_agent
import os
from dotenv import load_dotenv
load_dotenv()
MODEL = os.environ.get("MODEL", "gemini-2.5-flash")


# --- PM（要件化＆タスク分解） ---
pm_instruction = """
あなたはPMエージェントです。
ユーザーの要望からエージェント作成の要件を明確化するのが役割です。

【手順】
1. まずユーザーの要望を確認する
2. 不明確な点があれば「合計1回だけ」質問してよい
3. 次を決定する：
   - agent_name（短く分かりやすい英小文字+_）
   - goal（目的1行）
   - research_brief（searcher/surfer 共通の調査方針。プロンプトに入れるための材料を集める）
   - creater_agentへの指示（まず動くコード優先）
4. 要件が固まったら「要件確定しました」と明示し、フォーマットに従って指示を出す
5. member_agents（prepare_team_agent → reviewer_agent）に作業を開始させる
6. reviewer_agent の完了報告を受け取ったら、あなたが最終成果物を確認し、ユーザーに「納品報告」を行う
   - get_agent_file_tool で最終 agent.py を取得して、要点を確認する
   - ユーザーへの報告には「作ったもの」「使い方」「次に調整できる点」を含める

[サブエージェント]
- prepare_team_agent: searcher/surfer/creater を並列に実行する
- reviewer_agent: prepare_team_agent の出力を反映し、生成物を改善する

[重要]
- 曖昧な箇所はよしなに決めてよい
- 要件確定後は必ず以下フォーマットで出力する：


```
# 要件確定

## agent_name:
[名前]

## goal: 
[目的]

## research_brief（searcher/surfer 共通）
- 調べたい対象:
- 何のために調べるか（instructionへどう入れるか）:
- ほしいアウトプット（コピペ可能な箇条書き）:
- 禁止事項（捏造しない等）:

## creater_agentへの指示
[作成すべきエージェントの詳細]

```

"""

prepare_team_agent = ParallelAgent(
    name="prepare_team_agent",
    description="searcher/surfer/creater/tool_creater を並列に実行する。",
    sub_agents=[searcher_agent, surfer_agent, creater_agent, tool_creater_agent],
)


member_agents = SequentialAgent(
    name="member_agents",
    description="prepare_team_agentとreviewer_agentとpm_final_report_agentを順番に実行する。",
    sub_agents=[prepare_team_agent, reviewer_agent, pm_final_report_agent],
)


pm_agent = Agent(
    name="pm_agent",
    model=MODEL,
    instruction=pm_instruction,
    description=(
        "Agentを作成するためのPMエージェントです。"
        "要件が固まり次第、member_agents（prepare_team_agent→reviewer_agent）に指示を出して作業を開始させてください。"
        "最終成果物ができたら、必ずユーザーに納品報告してください。"
    ),
    sub_agents=[member_agents]
)

root_agent = SequentialAgent(
    name="agent_4_agent",
    description="PMで要件確定→membersで作成→reviewerで改善→PMがユーザーに納品報告。",
    sub_agents=[pm_agent],
)
