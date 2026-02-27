from google.adk.tools import FunctionTool
import os

# ファイル作成用のカスタムツール
def create_agent_files(agent_name: str, agent_code: str) -> str:
    """新しいエージェントのディレクトリとファイルを作成する
    agent_name: エージェント名（英小文字+_）
    agent_code: エージェントのPythonコード
    戻り値: 成功/失敗メッセージ
    """
    try:
        script_path = os.path.abspath(__file__) # tools/edit_agent.py
        parent_path = os.path.dirname(script_path) # tools
        grand_parent_dir = os.path.dirname(parent_path) # agent_4_agent
        grand_grand_parent_dir = os.path.dirname(grand_parent_dir) # A4A
        env_path = os.path.join(grand_parent_dir, ".env") # agent_4_agent/.env
        agent_dir = os.path.join(grand_grand_parent_dir, "agents", agent_name) # A4A/agents/agent_name
        # エージェントディレクトリを作成
        os.makedirs(agent_dir, exist_ok=True) 
        # __init__.pyファイルを作成
        with open(os.path.join(agent_dir, "__init__.py"), "w") as f:
            f.write("from .agent import root_agent\n")
            f.write('__all__ = ["root_agent"]\n')
        # a2a_agent.pyファイルを作成
        with open(os.path.join(agent_dir, "a2a_agent.py"), "w") as f:
            f.write("import uvicorn\n")
            f.write("from google.adk.a2a.utils.agent_to_a2a import to_a2a\n")
            f.write("from .import root_agent\n")
            f.write("import os\n")
            f.write("PORT = int(os.getenv(\"PORT\", 8001))\n")
            f.write("a2a_app = to_a2a(root_agent, port=PORT)\n")
            f.write("if __name__ == \"__main__\":\n")
            f.write("    uvicorn.run(a2a_app, host=\"0.0.0.0\", port=PORT)\n")
        # agent.pyファイルを作成
        with open(os.path.join(agent_dir, "agent.py"), "w") as f:
            f.write(agent_code)
        # 実行ファイルの階層にある.envファイルをコピーしてここに配置
        with open(env_path, "r") as f_src:
            env_content = f_src.read()
        with open(os.path.join(agent_dir, ".env"), "w") as f_dst:
            f_dst.write(env_content)

        return f"成功: {agent_name} を作成しました ({agent_dir})"
    except Exception as e:
        return f"エラー: {str(e)}"
    
# ファイル取得用のカスタムツール
def get_agent_file(agent_name: str, file_name: str) -> str:
    """既存のエージェントファイルを取得する
    agent_name: エージェント名（英小文字+_）
    file_name: 取得するファイル名（例: agent.py）
    戻り値: ファイル内容またはエラーメッセージ
    """
    try:
        # このファイルの3階層上のディレクトリを取得
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_path, "agents", agent_name, file_name)

        if not os.path.isfile(file_path):
            return f"エラー: ファイルが存在しません ({file_path})"

        with open(file_path, "r") as f:
            content = f.read()
        
        return content
    except Exception as e:
        return f"エラー: {str(e)}"

# ファイル更新用のカスタムツール
def edit_agent_file(agent_name: str, file_name: str, new_code: str) -> str:
    """既存のエージェントファイルを編集する
    agent_name: エージェント名（英小文字+_）
    file_name: 編集するファイル名（例: agent.py）
    new_code: 新しいコード内容
    戻り値: 成功/失敗メッセージ
    """
    try:
        # このファイルの3階層上のディレクトリを取得
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_path, "agents", agent_name, file_name)

        if not os.path.isfile(file_path):
            return f"エラー: ファイルが存在しません ({file_path})"

        with open(file_path, "w") as f:
            f.write(new_code)
        
        return f"成功: {file_name} を更新しました ({file_path})"
    except Exception as e:
        return f"エラー: {str(e)}"
    

create_agent_files_tool = FunctionTool(func=create_agent_files)
get_agent_file_tool = FunctionTool(func=get_agent_file)
edit_agent_file_tool = FunctionTool(func=edit_agent_file)