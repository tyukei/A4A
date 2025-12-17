# A4A
![alt text](assets/a4a.png)
エージェントを作るためのエージェント(agent for agent)です。
略してA4Aと呼びます。


## コントリビュータの募集
自分のオリジナルのエージェントを作ってぜひ、PR作成して、共有してください。

1. GitHubでこのリポジトリをFork
2. Forkしたリポジトリをclone
3. 以下セットアップ手順でエージェント作成する


## セットアップ手順
以下ターミナルより実行します。
```bash
git clone https://github.com/tyukei/A4A.git
uv sync
source .venv/bin/activate
cp agent_4_agent/.env.example agent_4_agent/.env
```

.envファイルにGEMINI_API_KEYを設定してください

GEMINI_API_KEYは、以下から取得できます。

https://aistudio.google.com/api-keys

## 実行手順
以下ターミナルより実行します。
```bash
adk web
```
open http://127.0.0.1:8000

チャットで作りたいエージェントを入力します

例：沖縄そばエージェントを作成したい。

![alt text](assets/image.png)

質問に答えていきます

![alt text](assets/image-1.png)

最終報告がされること確認します

![alt text](assets/image-2.png)

ブラウザをリフレッシュして、左上のエージェントを切り替えます。
作成成功していれば、新しいエージェントが選択できるようになっています。

![alt text](assets/image-3.png)

新しく作成したエージェントに質問をします。
例：おすすめのお店を教えて

![alt text](assets/image-4.png)

# Appendix
以下は、このA4Aを構築した時に用いたコマンドです

```bash
uv init -p=3.12
uv sync
source .venv/bin/activate
uv add google-adk python-dotenv
adk create agent_4_agent
echo "GOOGLE_API_KEY=your_google_api_key" >> agent_4_agent/.env
```

## adkエージェントの作り方

以下はadkエージェントの作り方のメモです。

参考：
- repository: https://github.com/google/adk-python　
- tutorial: https://codelabs.developers.google.com/your-first-agent-with-adk#0
- adk web: https://docs.cloud.google.com/agent-builder/agent-engine/sessions/manage-sessions-adk
- tool: https://google.github.io/adk-docs/tools/built-in-tools/
- adk web: https://github.com/google/adk-web
- adk examples: https://github.com/google/adk-samples

### uv のインストール
pythonのライブラリ管理ツールuvをインストールをします。
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

### uv の仮想環境作成
プロジェクトのルートディレクトリで以下のコマンドを実行します。
```bash
uv init -p 3.12
source .venv/bin/activate
uv add python-dotenv google-adk
```

uv initで仮想環境とproject.tomlが作成されます。

仮想環境のフォルダはデフォルトで.venvになります。

またオプションでpythonのバージョンを指定できます。

agent engineにディプロイする場合、pythonは3.12以下が推奨だったので、pythonのバージョンを3.12に指定しています。

### エージェント作成

adk webを使ってエージェントを作成するため、ルートディレクトリの配下に{agent_name}というフォルダを作成します。

その中にagent.pyを作成し、エージェントのコードを書きます。

> Run this command from the parent directory that contains your my_agent/ folder. For example, if your agent is inside agents/my_agent/, run adk web from the agents/ directory.
https://google.github.io/adk-docs/get-started/python/#run-with-web-interface


#### エージェント作成ファイルのフォルダ構成例
adkを使ったエージェントのフォルダ構成例は以下の通り。

サブエージェントは必要に応じて追加します。

```
{project_name}/
 ├── {agent_name}/
 │    ├── sub_agents/
 │    │    ├── {sub_agent1}.py　# サブエージェントがある場合
 │    │    └── ...
 │    ├── .env　# 環境変数ファイル
 │    ├──  agent.py　# エージェント定義ファイル
 │    └── tools/　# ツール定義ファイル
 │         ├── {tool1}.py
 │         └── ...
 ├── project.toml　# uvのプロジェクト設定ファイル
 └── .venv/　# uvの仮想環境フォルダ
```

#### agent.py
agent.pyにはエージェントの定義を書きます。

LlmAgentクラスをインスタンス化し、root_agentに代入することでエージェントが作成されます。

ここを`root_agent`にしないと` No root_agent found`というエラーになりました。
```python
from google.adk.agents import LlmAgent
root_agent = LlmAgent(
        model=LLM_MODEL_ID, # gemini-2.5-flash etc
        name=AGENT_NAME, # 任意のエージェント名
        description=AGENT_DESCRIPTION, # 簡単なエージェントの説明
        instruction=AGENT_INSTRUCTION, # エージェントの詳細な指示
        tools=[TOOLS],　# 使用するツールのリスト
    )
```

ドキュメントには`Agent`や`LlmAgent`とクラス名が出てくるが、AgentはLlmAgentのエイリアスで、どちらもで良いみたいです。

> The LlmAgent (often aliased simply as Agent) 
https://google.github.io/adk-docs/agents/llm-agents/

並列に実行したいエージェントは、ParallelAgentクラスをインスタンス化したり、
順番に実行したいエージェントは、SequentialAgentクラスをインスタンス化したりします。


#### tools.py
tools.pyにはエージェントが使用するtoolを定義します。
toolとは、エージェントが外部の情報を取得したり、アクションを実行したりするための機能です。

toolの書き方として、２つの方法があります。
1. 既に用意されれている、Built-in toolsを使う(例：Search tool)
2. 自分で関数を定義した、Custom toolsを作成する

https://google.github.io/adk-docs/tools/

カスタムtoolの場合は、FunctionToolを用いて、関数を定義します。
そのまま、pythonで定義して、エージェントに渡すこともできましたが、お作法として使用しています。

### エージェントの実行

adkの場合、UIはadk webコマンドで起動します。

```bash
adk web
```