# Agent to Agent (A2A) ガイド

## A4AにおけるA2A活用

A4Aでは、この仕組みを使って**小さな専門エージェントを組み合わせて複雑なタスクをこなす**システムを実現しています。

- **専門家**: 「沖縄そばエージェント」や「ヤシの木エージェント」などが、それぞれ独立したA2Aエージェントとして待機します。
- **リーダー（Coordinator）**: ユーザーの窓口となるエージェントが、質問内容に応じて適切な専門家（A2Aエージェント）に仕事を振り、その回答をまとめてユーザーに返します。

## Agent to Agent (A2A) 実行
複数のエージェントを連携させて実行する機能です。

### 仕組み
1. **Runner (Coordinator)**: `a4a.agent` が全体を統括するコーディネーターとして機能します。
2. **Sub-agents**: A4Aで作ったエージェント`okinawa_soba_search_agent` や `palm_tree_info_agent` などは、それぞれ専門機能を持つエージェントとして起動します。
3. **Automated Discovery**: `a4a/discovery.py` がプロジェクト内のエージェント（`a2a_agent.py` を持つフォルダ）を自動検出し、コーディネーターに「使える手札」として登録します。

ユーザーが質問をすると、コーディネーターが「これは沖縄そばのエージェントに聞くべきだ」と判断し、裏側でAPIリクエストを飛ばして答えを聞き出し、ユーザーに返します。

`a4a/discovery.py` がプロジェクト内のエージェント（`a2a_agent.py` があるフォルダ）を自動検出し、起動します。

### 1. 起動

ターミナルで以下実行してください

```bash
make run
```
これにより、すべてのエージェントとコーディーネーターが起動します。
ポートは `8001` から順番に割り当てられ、コーディーネーターは `8000` で待機します。

### 2. 呼び出し

起動したコーディーネーターに対して、別のターミナルからクエリを投げます。

別ターミナルで以下実行してください

```bash
make query q="沖縄そば食べたい！"
```
```bash
make query q="ヤシの木について教えて"
```
```bash
make query q="新しいエージェントを作って"
```

成功すると以下のように回答が返ってきます。

![alt text](../assets/image-a2a-1.png)


### 3. トラブルシューティング

もし「ポートが使われています」などのエラーが出る場合は、前のプロセスが残っている可能性があります。
以下のコマンドでクリーンアップしてください。

```bash
make clean
```

## Agent to Agent (A2A) とは？

https://codelabs.developers.google.com/intro-a2a-purchasing-concierge#9

**AIエージェント同士が会話・連携するための標準的な仕組み（プロトコル）** です。
通常、AIエージェントは「人間 <-> AI」の対話で作られますが、A2Aを使うと「AI <-> AI」の対話が可能になります。

![alt text](../assets/image-a2a-3.png)

### ADK to A2A

https://google.github.io/adk-docs/a2a/quickstart-exposing/#exposing-the-remote-agent-with-the-to_a2aroot_agent-function

ADKはエージェントのフレームワークですが、A2Aはエージェント同士のコミュニケーションの仕組み(プロトコル)です。

実際に、プロトコルを導入する手順を説明していきます。

まず以下ライブラリを追加します。

```bash
uv add "google-adk[a2a]"
```

余談ですが、`[]`を含むライブラリの場合、`""`で囲む必要があります。

次に、ADKを用いてA2Aのプロトコル上で動くコードを追加します。

```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Make your agent A2A-compatible
a2a_app = to_a2a(root_agent, port=8001)
```

skills、capabilities、name、descriptionなどメタデータも含めagent cardは自動的に生成されます。

agent cardというのは、はエージェントの名刺見たいなものです。

ここには「私は何ができるか」「どう呼び出せばいいか」が書かれています。

今回のプロジェクトでは `http://localhost:xxxx/.well-known/agent-card.json` に公開されています。

具体的に見てみましょう。

まずターミナルで以下実行します。
```
make run
```
別ターミナルで以下実行します。
```
curl http://localhost:8001/.well-known/agent-card.json
```

確かに、agent cardが作成されていることが確認できますね。

![alt text](../assets/image-a2a-2.png)    

別のエージェントを見たい場合は、port番号を変更することで確認できます
```
curl http://localhost:8002/.well-known/agent-card.json
```

もちろん、自分でagent cardを作成して、それを公開することも可能です。

```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard

# Define A2A agent card
my_agent_card = AgentCard(
    "name": "file_agent",
    "url": "http://example.com",
    "description": "Test agent from file",
    "version": "1.0.0",
    "capabilities": {},
    "skills": [],
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "supportsAuthenticatedExtendedCard": False,
)
a2a_app = to_a2a(root_agent, port=8001, agent_card=my_agent_card)
```

### A2Aの対話フロー

システム内部では、以下のような流れで通信が行われています。

1.  **発見 (Discovery)**
    A2A Client（コーディネーター）は、アクセス可能な全てのA2A Server（サブエージェント）の Agent Card を読み込み、接続クライアントを構築します。
2.  **タスク実行 (Task Execution)**
    必要に応じて、A2A Client はサーバーにメッセージを送信します。サーバーはこれを「完遂すべきタスク」として評価・実行します。
3.  **進捗通知 (Push Notification)**
    （オプション）プッシュ通知の受信URLが設定されており、サーバーがサポートしている場合、サーバーはタスクの進行状況をクライアントに通知することができます。
4.  **完了 (Completion)**
    タスクが完了すると、A2A Server はその成果物（Artifact）を A2A Client に返送します。

  ![alt text](../assets/image-a2a-4.png)
