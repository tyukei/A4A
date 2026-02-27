# Usage — A4A の使い方

このドキュメントでは、**A4Aを使って実際にエージェントを作成・利用するまでの流れ**を説明します。  


---

## 前提条件

- Python 3.12（推奨）
- `uv` がインストールされていること
- Google Gemini API Key を持っていること

---

## セットアップ

### リポジトリの取得と環境構築

```bash
git clone https://github.com/tyukei/A4A.git
cd A4A
uv sync --frozen
source .venv/bin/activate
```

### 環境変数の設定

```bash
cp src/agent_4_agent/.env.example src/agent_4_agent/.env
```

`.env` ファイルに以下を設定してください。

```env
GEMINI_API_KEY=your_api_key_here
```

APIキーは以下から取得できます。  
https://aistudio.google.com/api-keys

---

## Web UI の起動

A4Aは **ADK Web UI** を使って操作します。

```bash
adk web src/
```

ブラウザで以下にアクセスしてください。

```
http://127.0.0.1:8000
```

---

## エージェントを作成する

### 1. チャットに要望を入力する

画面中央のチャットに、**作りたいエージェントの要望**を自然文で入力します。

例：

> 沖縄そばエージェントを作成したい

![チャットに要望を入力](../assets/image.png)

---

### 2. A4Aの質問に答える

A4A（PMエージェント）が、  
エージェントを作るために必要な情報を質問してきます。

- エージェントの目的
- 想定ユーザー
- 調査方針
- 振る舞いの方針 など

質問に順番に答えていくことで、  
**エージェントの仕様が段階的に明確化されていきます。**

![質問に答える](../assets/image-1.png)

---

### 3. 最終報告を確認する

すべての質問に答えると、  
A4Aが **作成されたエージェントの最終報告** を出力します。

![最終報告](../assets/image-2.png)

この時点で以下が完了しています。

- エージェント仕様の確定
- エージェントコードの生成
- ADK / A2A 対応エージェントとしての登録

---

## 作成されたエージェントを使う

### 1. ブラウザをリフレッシュする

ページをリロードします。

---

### 2. 左上のエージェントを切り替える

左上のエージェント選択ドロップダウンから、  
**新しく作成されたエージェント**を選択します。

![エージェント切り替え](../assets/image-3.png)

---

### 3. エージェントに質問する

選択したエージェントに対して、  
通常のチャットと同じように質問します。

例：

> おすすめのお店を教えて

![エージェントに質問](../assets/image-4.png)

エージェントが、自分の専門性に基づいて回答します。

---

## 補足：A4Aで作られたエージェントについて

- 作成されたエージェントは **A2A（Agent to Agent）対応**です
- `a2a_agent.py` を持つエージェントは自動的に検出されます
- A2A Coordinator から「専門家エージェント」として呼び出されます

A2Aの仕組みや全体構成については以下を参照してください。

→ [architecture.md](architecture.md)

---

## トラブルシューティング

### Web UI が起動しない
- 仮想環境が有効化されているか確認してください
- `GEMINI_API_KEY` が設定されているか確認してください

### エージェントが増えない
- 最終報告が表示されているか確認してください
- ブラウザをリロードしてください

### ポートが使用中と表示される
別プロセスが残っている可能性があります。

```bash
make clean
```

---

## 次に読むもの

- A4A / A2A の仕組みと全体像  
  → [architecture.md](architecture.md)

- Agent Engine へのデプロイ方法  
  → [deploy-agent-engine.md](deploy-agent-engine.md)

- A4Aを作った背景・思想  
  → [why-a4a.md](why-a4a.md)

---

## CLI でエージェントを自動作成する（`a4a`）

Web UI を使わず、コマンドラインから**エージェント作成〜PR提出〜レビュー〜GitHub issue 起票**まで実行できます。
各操作はフラグで個別に制御できます。

### フラグ一覧

| フラグ | 説明 |
|---|---|
| `--idea KEYWORD` | キーワードからLLMがプロンプトを自動生成 |
| `--pr` | エージェント作成後に GitHub PR を作成する |
| `--review` | コードレビューを実行する（issueは作成しない） |
| `--issue` | コードレビューを実行し GitHub issue も起票する（`--review`を兼ねる） |
| `--review-only AGENT_NAME` | 既存エージェントのみレビューする（作成はスキップ） |

### 基本的な使い方

```bash
# エージェントを作成するだけ（PR・issueなし）
a4a --idea "天気"
a4a "天気予報エージェントを作って"

# 作成 + PR作成
a4a --idea "天気" --pr

# 作成 + GitHub issue起票（レビューも実行）
a4a --idea "天気" --issue

# 作成 + PR作成 + issue起票まで全部
a4a --idea "天気" --pr --issue

# コードレビューのみ（issueは作成しない）
a4a --idea "天気" --review

# 既存エージェントをレビュー（issueなし）
a4a --review-only okinawa_travel_agent

# 既存エージェントをレビューしてissueも起票
a4a --review-only okinawa_travel_agent --issue
```

### 実行フロー

```
a4a --idea "天気" --pr --issue
       │
       ▼ ① LLM がプロンプトを自動生成
       │   例: "weather_forecast_agent を作って。都市名から
       │       Yahoo天気とGoogle検索のURLを動的生成するツールを持つエージェントに"
       │
       ▼ ② agent_4_agent がエージェントを自動作成
       │   PM が質問してきたら LLM が自動回答（人間の操作不要）
       │   → agents/{agent_name}/ に生成される
       │
       ▼ ③ --pr: GitHub PR を作成
       │   feat/add-{agent-name} ブランチを作成してコミット・プッシュ・PR提出
       │
       ▼ --issue（または --review）がある場合
       ├─④ [レビュー①] 作成したエージェントのコード品質をレビュー
       └─⑤ [レビュー②] A4A フレームワーク自体の改善提案
            └─ --issue のときのみ GitHub issue を起票
```

### `--pr` による PR 作成

`--pr` フラグを付けると以下の処理が行われます。

1. `feat/add-{agent-name}` ブランチを作成
2. `agents/{agent_name}/` のファイルをコミット（`.env` は除外）
3. リモートにプッシュ
4. `[{agent_name}(shink-shinka)] Add {agent_name}` タイトルで PR を提出

```
[weather_forecast_agent(shink-shinka)] Add weather_forecast_agent
```

PR本文は `.github/pull_request_template.md` の構造（概要・変更内容・関連Issue・動作確認方法・チェックリスト）に準拠して自動生成されます。

### `--issue` で作成される GitHub issue

`--issue` フラグを付けると2種類のレビューが自動実行され、それぞれ GitHub issue が起票されます。

| レビュー | 担当エージェント | 観点 |
|---|---|---|
| ① 作成エージェントのレビュー | `quality_reporter_agent` | コード品質、instructionの完成度、ツール品質 |
| ② A4Aシステムのレビュー | `system_reviewer_agent` | 機能の抜け漏れ、UX改善、アーキテクチャ改善 |

issue タイトルは `[エージェント名(shink-shinka)]` の形式になります。

```
[okinawa_travel_agent(shink-shinka)] デフォルトモデル名に誤字がある
[A4A(shink-shinka)] バッチ実行機能を追加する
```

> **前提**: `--pr` / `--issue` を使う場合は `gh auth login` で GitHub CLI の認証が必要です。未認証の場合はスキップされ、改善内容がテキストで出力されます。
