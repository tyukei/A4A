# セットアップと実行

## セットアップ手順
以下ターミナルより実行します。
```bash
git clone https://github.com/tyukei/A4A.git
uv sync --frozen
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

![alt text](../assets/image.png)

質問に答えていきます

![alt text](../assets/image-1.png)

最終報告がされること確認します

![alt text](../assets/image-2.png)

ブラウザをリフレッシュして、左上のエージェントを切り替えます。
作成成功していれば、新しいエージェントが選択できるようになっています。

![alt text](../assets/image-3.png)

新しく作成したエージェントに質問をします。
例：おすすめのお店を教えて

![alt text](../assets/image-4.png)
