# ADKエージェントの作り方

このドキュメントでは、Google ADK（Agent Development Kit）を使ってエージェントを作成する方法を説明します。

## 参考リンク

- Repository: https://github.com/google/adk-python
- Tutorial: https://codelabs.developers.google.com/your-first-agent-with-adk#0
- ADK Web: https://docs.cloud.google.com/agent-builder/agent-engine/sessions/manage-sessions-adk
- Tools: https://google.github.io/adk-docs/tools/built-in-tools/
- ADK Web: https://github.com/google/adk-web
- ADK Examples: https://github.com/google/adk-samples

---

## uvのインストール

Pythonのライブラリ管理ツール`uv`をインストールします。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

### uvとは？

`uv`は高速なPythonパッケージマネージャーで、従来の`pip`や`poetry`よりも高速に動作します。
仮想環境の管理とパッケージのインストールを統合的に行えます。

---

## uvの仮想環境作成

プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
uv init -p 3.12
source .venv/bin/activate
uv add python-dotenv google-adk
```

### 各コマンドの説明

- `uv init -p 3.12`: Python 3.12で仮想環境とproject.tomlを作成
  - 仮想環境のフォルダはデフォルトで`.venv`になります
  - Agent Engineにディプロイする場合、Pythonは3.12以下が推奨されています
- `source .venv/bin/activate`: 仮想環境を有効化
- `uv add python-dotenv google-adk`: 必要なライブラリをインストール

---

## エージェント作成

ADK webを使ってエージェントを作成するため、ルートディレクトリの配下に`{agent_name}`というフォルダを作成します。

その中に`agent.py`を作成し、エージェントのコードを書きます。

> **重要**: Run this command from the parent directory that contains your my_agent/ folder. For example, if your agent is inside agents/my_agent/, run adk web from the agents/ directory.
> 
> 参考: https://google.github.io/adk-docs/get-started/python/#run-with-web-interface

---

## エージェント作成ファイルのフォルダ構成例

ADKを使ったエージェントのフォルダ構成例は以下の通りです。

サブエージェントは必要に応じて追加します。

```
{project_name}/
 ├── {agent_name}/
 │    ├── sub_agents/
 │    │    ├── {sub_agent1}.py　# サブエージェントがある場合
 │    │    └── ...
 │    ├── .env　# 環境変数ファイル
 │    ├── agent.py　# エージェント定義ファイル
 │    └── tools/　# ツール定義ファイル
 │         ├── {tool1}.py
 │         └── ...
 ├── pyproject.toml　# uvのプロジェクト設定ファイル
 └── .venv/　# uvの仮想環境フォルダ
```

### フォルダ構成のポイント

- **agent.py**: エージェントのメイン定義ファイル（必須）
- **tools/**: カスタムツールを配置するディレクトリ
- **sub_agents/**: 複数のエージェントを組み合わせる場合に使用
- **.env**: API キーなどの環境変数を管理

---

## agent.py

`agent.py`にはエージェントの定義を書きます。

`LlmAgent`クラスをインスタンス化し、`root_agent`に代入することでエージェントが作成されます。

> **注意**: ここを`root_agent`にしないと`No root_agent found`というエラーになります。

```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model=LLM_MODEL_ID,  # gemini-2.5-flash etc
    name=AGENT_NAME,  # 任意のエージェント名
    description=AGENT_DESCRIPTION,  # 簡単なエージェントの説明
    instruction=AGENT_INSTRUCTION,  # エージェントの詳細な指示
    tools=[TOOLS],  # 使用するツールのリスト
)
```

### LlmAgentとAgentの違い

ドキュメントには`Agent`や`LlmAgent`とクラス名が出てきますが、`Agent`は`LlmAgent`のエイリアスで、どちらを使っても問題ありません。

> The LlmAgent (often aliased simply as Agent)
> 
> 参考: https://google.github.io/adk-docs/agents/llm-agents/

### エージェントの種類

- **LlmAgent**: 単一のLLMベースのエージェント
- **ParallelAgent**: 複数のエージェントを並列に実行
- **SequentialAgent**: 複数のエージェントを順番に実行

---

## tools.py

`tools.py`にはエージェントが使用するツールを定義します。

ツールとは、エージェントが外部の情報を取得したり、アクションを実行したりするための機能です。

### ツールの書き方

ツールの定義方法として、2つの方法があります：

1. **Built-in tools**: 既に用意されているツールを使う（例：Search tool）
2. **Custom tools**: 自分で関数を定義したツールを作成する

参考: https://google.github.io/adk-docs/tools/

### カスタムツールの例

カスタムツールの場合は、`FunctionTool`を用いて関数を定義します。

そのままPythonで定義して、エージェントに渡すこともできますが、お作法として`FunctionTool`を使用します。

```python
from google.adk.agents.function_tool import FunctionTool

def my_custom_function(query: str) -> str:
    """カスタム関数の説明"""
    # 処理内容
    return result

my_tool = FunctionTool(
    name="my_custom_tool",
    description="このツールの説明",
    func=my_custom_function
)
```

---

## エージェントの実行

ADKの場合、UIは`adk web`コマンドで起動します。

```bash
adk web
```

ブラウザで以下にアクセスしてください：

```
http://127.0.0.1:8000
```

### トラブルシューティング

#### ポートが既に使用されている

別のプロセスが8000番ポートを使用している場合、以下のコマンドでポートを変更できます：

```bash
adk web --port 8080
```

#### 仮想環境が有効化されていない

`adk`コマンドが見つからない場合、仮想環境を有効化してください：

```bash
source .venv/bin/activate
```

#### モジュールが見つからない

必要なパッケージがインストールされていない可能性があります：

```bash
uv sync
```

---

## A4Aプロジェクトの初期構築コマンド

参考として、A4Aプロジェクトを構築した際に使用したコマンドを記載します：

```bash
uv init -p=3.12
uv sync
source .venv/bin/activate
uv add google-adk python-dotenv
adk create agent_4_agent
echo "GOOGLE_API_KEY=your_google_api_key" >> agent_4_agent/.env
```

---

## 次のステップ

- エージェントをA2A対応にする → [a2a_guide.md](a2a_guide.md)
- エージェントをデプロイする → [deployment.md](deployment.md)
- A4Aの使い方を学ぶ → [usage.md](usage.md)
