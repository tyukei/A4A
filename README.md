# A4A
![A4A Logo](assets/a4a.png)

エージェントを作るためのエージェント(Agent for Agent)です。略してA4Aと呼びます。

詳しくは[Zennの記事](https://zenn.dev/churadata/articles/0015498168c49f)より

<!-- Project Status Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/tyukei/A4A)](https://github.com/tyukei/A4A/releases)
[![Last Commit](https://img.shields.io/github/last-commit/tyukei/A4A)](https://github.com/tyukei/A4A/commits/main)

<!-- Community Badges -->
[![Contributing](https://img.shields.io/badge/Contributing-Welcome-green.svg)](CONTRIBUTING.md)
[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Contributor%20Covenant-purple.svg)](CODE_OF_CONDUCT.md)
[![Security](https://img.shields.io/badge/Security-Policy-blue.svg)](SECURITY.md)

<!-- GitHub Engagement -->
[![GitHub stars](https://img.shields.io/github/stars/tyukei/A4A.svg?style=social&label=Star)](https://github.com/tyukei/A4A)
---

## クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/tyukei/A4A.git
cd A4A

# 環境構築
uv sync --frozen
source .venv/bin/activate
cp src/agent_4_agent/.env.example src/agent_4_agent/.env

# .envファイルにGEMINI_API_KEYを設定
# https://aistudio.google.com/api-keys

# Web UI を起動
adk web src/
```

ブラウザで http://127.0.0.1:8000 を開いて、エージェント作成を始めましょう！

```bash
# CLI でエージェントを作成（Web UI 不要）
a4a --idea "作りたいエージェントのキーワード"

# 作成 + GitHub PR 提出
a4a --idea "天気" --pr

# 作成 + PR提出 + レビュー + GitHub issue 起票まで全部
a4a --idea "天気" --pr --issue
```

詳細は [CLI ガイド](docs/usage.md#cli-でエージェントを自動作成するrunpy) をご覧ください。

詳細な手順は [セットアップと実行ガイド](docs/setup_and_execution.md) をご覧ください。

---

## ドキュメント

### 基本ガイド

- **[A4Aについて](docs/introduction.md)** - A4Aの概要とできること
- **[セットアップと実行](docs/setup_and_execution.md)** - インストールと基本的な使い方
- **[使い方ガイド](docs/usage.md)** - エージェントの作成から利用まで

### 技術ドキュメント

- **[アーキテクチャ](docs/architecture.md)** - A4Aの全体構成とA2Aの活用方法
- **[A2Aガイド](docs/a2a_guide.md)** - Agent to Agentプロトコルの詳細
- **[ADKチュートリアル](docs/adk_tutorial.md)** - ADKエージェントの作り方

### その他

- **[デプロイメント](docs/deployment.md)** - Agent Engineへのディプロイ方法
- **[CI/CD](docs/cicd.md)** - GitHub Actionsを使った自動化
- **[Why A4A?](docs/why_a4a.md)** - A4Aを作った理由と未来への展望

---

## できること

- **エージェント作成**: ADKでエージェントを対話的に作成
- **PR自動提出**: 作成したエージェントをそのままGitHub PRとして提出
- **品質レビュー**: コード品質・instruction完成度をAIが自動レビューしてissue起票
- **A2A連携**: 作成したエージェントをA2Aでつなげる
- **自動ディプロイ**: Agent Engineへのディプロイ（WIP）

---

## コントリビュート

自分のオリジナルのエージェントを作って、ぜひPRを作成して共有してください！

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご確認ください。

### コントリビュート手順

1. このリポジトリをFork
2. Forkしたリポジトリをclone
3. [セットアップ手順](docs/setup_and_execution.md)に従ってエージェントを作成
4. PRを作成

---

## Web UI

ブラウザからチャット形式でエージェントを操作できます。

```bash
# Web UIを起動（make run 不要、単体で動作）
make ui
```

ブラウザで http://localhost:8888 を開くと、チャット画面が表示されます。

- リアルタイムストリーミングで回答を表示
- どのサブエージェントが応答しているかバッジで確認可能
- マークダウン形式でレンダリング
- 同一タブ内で会話が継続（サブエージェントごとにセッション管理）

---

## A2A実行例

複数のエージェントを連携させて実行できます。

```bash
# すべてのエージェントとコーディネーターを起動
make run

# 別ターミナルからクエリを送信
make query q="沖縄そば食べたい！"
make query q="ヤシの木について教えて"
make query q="新しいエージェントを作って"
```

詳細は [A2Aガイド](docs/a2a_guide.md) をご覧ください。

---

## 参考リンク

- [ADK Python](https://github.com/google/adk-python)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol](https://codelabs.developers.google.com/intro-a2a-purchasing-concierge)
- [Vertex AI Agent Engine](https://docs.cloud.google.com/agent-builder/agent-engine/overview)

---

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

---

## 謝辞

このプロジェクトは、Google ADKとA2Aプロトコルを活用しています。
コミュニティの皆様のフィードバックとコントリビューションに感謝します。

---

**作成者**: [@tyukei](https://github.com/tyukei)
