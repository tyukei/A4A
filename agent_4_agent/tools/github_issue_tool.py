import subprocess
from google.adk.tools.function_tool import FunctionTool


def create_github_issue(title: str, body: str, labels: str = "") -> str:
    """GitHub issueを作成する

    Args:
        title: issueのタイトル（簡潔に）
        body: issueの本文（改善内容の詳細）
        labels: ラベル（カンマ区切り、例: "enhancement,bug"）

    Returns:
        作成されたissueのURLまたはエラーメッセージ
    """
    try:
        cmd = ["gh", "issue", "create", "--title", title, "--body", body]
        if labels:
            for label in [l.strip() for l in labels.split(",") if l.strip()]:
                cmd.extend(["--label", label])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            return f"Issue作成成功: {result.stdout.strip()}"
        else:
            return f"Issue作成失敗: {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "エラー: gh コマンドがタイムアウトしました"
    except FileNotFoundError:
        return "エラー: gh コマンドが見つかりません。GitHub CLI をインストールしてください: https://cli.github.com/"
    except Exception as e:
        return f"エラー: {str(e)}"


# FunctionToolとして登録
create_github_issue_tool = FunctionTool(func=create_github_issue)
