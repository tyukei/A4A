# A4A
![A4A Logo](assets/a4a.png)

エージェントを作るためのエージェント(Agent for Agent)です。略してA4Aと呼びます。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Policy-blue.svg)](SECURITY.md)
[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Contributor%20Covenant-purple.svg)](CODE_OF_CONDUCT.md)

---

## クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/tyukei/A4A.git
cd A4A

# 環境構築
uv sync
source .venv/bin/activate
cp agent_4_agent/.env.example agent_4_agent/.env

# .envファイルにGEMINI_API_KEYを設定
# https://aistudio.google.com/api-keys

# A4Aを起動
adk web
```

ブラウザで http://127.0.0.1:8000 を開いて、エージェント作成を始めましょう！

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
