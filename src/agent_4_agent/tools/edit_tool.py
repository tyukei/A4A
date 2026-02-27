import os
from typing import Optional
from google.adk.tools.function_tool import FunctionTool

# カスタムツール作成用のツール
def create_custom_tool(
    tool_name: str,
    tool_code: str,
    agent_name: Optional[str] = None
) -> str:
    """新しいカスタムツールを作成する
    
    Args:
        tool_name: ツール名（例: get_animal_location_map）
        tool_code: ツールの関数コード全体（def文から完全なコードを含む）
        agent_name: ツールを追加するエージェント名（指定されない場合はagent_4_agentに作成）
    
    Returns:
        成功/失敗メッセージ
        
    Example:
        tool_code = '''
def get_animal_location_map(location_name: str) -> str:
    \"\"\"那覇空港から指定された場所までのGoogle Mapsルートリンクを生成します。
    
    Args:
        location_name: 目的地の名前（例: 美ら海水族館、ヤンバルクイナ生態展示学習施設）
        
    Returns:
        Google Mapsのルートリンク
    \"\"\"
    from urllib.parse import quote
    origin = "那覇空港"
    destination = location_name
    encoded_origin = quote(origin)
    encoded_destination = quote(destination)
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_destination}&travelmode=driving"
    return maps_url
'''
        create_custom_tool("get_animal_location_map", tool_code, "okinawa_agent")
    """
    try:
        # このファイルのパスを取得
        script_path = os.path.abspath(__file__)  # tools/edit_tool.py
        parent_path = os.path.dirname(script_path)  # tools
        grand_parent_dir = os.path.dirname(parent_path)  # agent_4_agent
        grand_grand_parent_dir = os.path.dirname(grand_parent_dir)  # A4A
        
        # ツールファイルを作成するディレクトリを決定
        if agent_name:
            # 特定のエージェント用のツールとして作成
            tools_dir = os.path.join(grand_grand_parent_dir, "agents", agent_name, "tools")
        else:
            # agent_4_agentのtoolsディレクトリに作成
            tools_dir = parent_path
        
        # toolsディレクトリが存在しない場合は作成
        os.makedirs(tools_dir, exist_ok=True)
        
        # __init__.pyが存在しない場合は作成
        init_file = os.path.join(tools_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("")
        
        # ツールファイルのパス
        tool_file_path = os.path.join(tools_dir, f"{tool_name}_tool.py")
        
        # ツールファイルを作成
        with open(tool_file_path, "w") as f:
            # インポート文を追加
            f.write("from google.adk.tools.function_tool import FunctionTool\n\n")
            
            # ツールコードを書き込み
            f.write(tool_code)
            f.write("\n\n")
            
            # FunctionToolインスタンスを作成
            f.write(f"# FunctionToolとして登録\n")
            f.write(f"{tool_name}_tool = FunctionTool(func={tool_name})\n")
        
        # 使用方法のメッセージを生成
        usage_message = f"""
成功: カスタムツール '{tool_name}' を作成しました
ファイルパス: {tool_file_path}

エージェントで使用するには、agent.pyに以下を追加してください:

1. インポート:
   from .tools.{tool_name}_tool import {tool_name}_tool

2. エージェント作成時にツールを追加:
   root_agent = Client(model_name="gemini-2.0-flash-exp").agent(
       tools=[{tool_name}_tool, ...],
       ...
   )
"""
        
        return usage_message
        
    except Exception as e:
        return f"エラー: {str(e)}"


# カスタムツール一覧取得用のツール
def list_custom_tools(agent_name: Optional[str] = None) -> str:
    """作成済みのカスタムツールの一覧を取得する
    
    Args:
        agent_name: エージェント名（指定されない場合はagent_4_agentのツールを取得）
    
    Returns:
        ツール一覧
    """
    try:
        # このファイルのパスを取得
        script_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(script_path)
        grand_parent_dir = os.path.dirname(parent_path)
        grand_grand_parent_dir = os.path.dirname(grand_parent_dir)
        
        # ツールディレクトリを決定
        if agent_name:
            tools_dir = os.path.join(grand_grand_parent_dir, "agents", agent_name, "tools")
        else:
            tools_dir = parent_path

        if not os.path.exists(tools_dir):
            return f"ツールディレクトリが存在しません: {tools_dir}"
        
        # _tool.pyで終わるファイルを検索
        tool_files = [f for f in os.listdir(tools_dir) if f.endswith("_tool.py")]
        
        if not tool_files:
            return "カスタムツールが見つかりませんでした"
        
        result = f"カスタムツール一覧 ({tools_dir}):\n"
        for tool_file in sorted(tool_files):
            result += f"  - {tool_file}\n"
        
        return result
        
    except Exception as e:
        return f"エラー: {str(e)}"


# カスタムツール取得用のツール
def get_custom_tool(tool_name: str, agent_name: Optional[str] = None) -> str:
    """カスタムツールのコードを取得する
    
    Args:
        tool_name: ツール名（例: get_animal_location_map）
        agent_name: エージェント名（指定されない場合はagent_4_agentのツールを取得）
    
    Returns:
        ツールのコード内容またはエラーメッセージ
    """
    try:
        # このファイルのパスを取得
        script_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(script_path)
        grand_parent_dir = os.path.dirname(parent_path)
        grand_grand_parent_dir = os.path.dirname(grand_parent_dir)
        
        # ツールディレクトリを決定
        if agent_name:
            tools_dir = os.path.join(grand_grand_parent_dir, "agents", agent_name, "tools")
        else:
            tools_dir = parent_path

        tool_file_path = os.path.join(tools_dir, f"{tool_name}_tool.py")

        if not os.path.isfile(tool_file_path):
            return f"エラー: ツールファイルが存在しません ({tool_file_path})"

        with open(tool_file_path, "r") as f:
            content = f.read()
        
        return content
        
    except Exception as e:
        return f"エラー: {str(e)}"


# カスタムツール編集用のツール
def edit_custom_tool(
    tool_name: str,
    new_tool_code: str,
    agent_name: Optional[str] = None
) -> str:
    """既存のカスタムツールを編集する
    
    Args:
        tool_name: ツール名（例: get_animal_location_map）
        new_tool_code: 新しいツールの関数コード全体
        agent_name: エージェント名（指定されない場合はagent_4_agentのツールを編集）
    
    Returns:
        成功/失敗メッセージ
    """
    try:
        # このファイルのパスを取得
        script_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(script_path)
        grand_parent_dir = os.path.dirname(parent_path)
        grand_grand_parent_dir = os.path.dirname(grand_parent_dir)
        
        # ツールディレクトリを決定
        if agent_name:
            tools_dir = os.path.join(grand_grand_parent_dir, "agents", agent_name, "tools")
        else:
            tools_dir = parent_path

        tool_file_path = os.path.join(tools_dir, f"{tool_name}_tool.py")

        if not os.path.isfile(tool_file_path):
            return f"エラー: ツールファイルが存在しません ({tool_file_path})"

        # ツールファイルを更新
        with open(tool_file_path, "w") as f:
            # インポート文を追加
            f.write("from google.adk.tools.function_tool import FunctionTool\n\n")
            
            # 新しいツールコードを書き込み
            f.write(new_tool_code)
            f.write("\n\n")
            
            # FunctionToolインスタンスを作成
            f.write(f"# FunctionToolとして登録\n")
            f.write(f"{tool_name}_tool = FunctionTool(func={tool_name})\n")
        
        return f"成功: カスタムツール '{tool_name}' を更新しました ({tool_file_path})"
        
    except Exception as e:
        return f"エラー: {str(e)}"


# カスタムツール削除用のツール
def delete_custom_tool(tool_name: str, agent_name: Optional[str] = None) -> str:
    """カスタムツールを削除する
    
    Args:
        tool_name: ツール名（例: get_animal_location_map）
        agent_name: エージェント名（指定されない場合はagent_4_agentのツールを削除）
    
    Returns:
        成功/失敗メッセージ
    """
    try:
        # このファイルのパスを取得
        script_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(script_path)
        grand_parent_dir = os.path.dirname(parent_path)
        grand_grand_parent_dir = os.path.dirname(grand_parent_dir)
        
        # ツールディレクトリを決定
        if agent_name:
            tools_dir = os.path.join(grand_grand_parent_dir, "agents", agent_name, "tools")
        else:
            tools_dir = parent_path

        tool_file_path = os.path.join(tools_dir, f"{tool_name}_tool.py")

        if not os.path.isfile(tool_file_path):
            return f"エラー: ツールファイルが存在しません ({tool_file_path})"

        # ファイルを削除
        os.remove(tool_file_path)
        
        return f"成功: カスタムツール '{tool_name}' を削除しました ({tool_file_path})"
        
    except Exception as e:
        return f"エラー: {str(e)}"


# FunctionToolとして登録
create_custom_tool_tool = FunctionTool(func=create_custom_tool)
list_custom_tools_tool = FunctionTool(func=list_custom_tools)
get_custom_tool_tool = FunctionTool(func=get_custom_tool)
edit_custom_tool_tool = FunctionTool(func=edit_custom_tool)
delete_custom_tool_tool = FunctionTool(func=delete_custom_tool)
