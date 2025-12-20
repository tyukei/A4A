import os
import sys
import importlib
from pathlib import Path
from dataclasses import dataclass

@dataclass
class AgentConfig:
    name: str
    module: str
    port: int
    url: str
    description: str

def discover_agents(root_dir: Path = None, start_port: int = 8001) -> list[AgentConfig]:
    """
    Scans the directory for agents.
    An agent is a directory containing an 'a2a_agent.py' file.
    """
    if root_dir is None:
        # Assume root is the parent of 'a4a' folder, or current working directory
        # If running as -m a4a.run_all, cwd is usually root.
        root_dir = Path.cwd()

    agents = []
    current_port = start_port

    # List all subdirectories
    for item in root_dir.iterdir():
        if not item.is_dir():
            continue
        
        if item.name.startswith(".") or item.name == "a4a" or item.name == "__pycache__":
            continue
            
        a2a_path = item / "a2a_agent.py"
        if a2a_path.exists():
            agent_name = item.name
            module_name = f"{agent_name}"
            a2a_module_name = f"{agent_name}.a2a_agent"
            
            # Try to import to get description (optional, but good for coordinator)
            description = ""
            try:
                # We need to make sure root_dir is in sys.path
                if str(root_dir) not in sys.path:
                    sys.path.insert(0, str(root_dir))
                
                # Assume naming convention: package exports 'root_agent' in __init__
                mod = importlib.import_module(module_name)
                if hasattr(mod, "root_agent"):
                    description = getattr(mod.root_agent, "description", "")
            except Exception as e:
                print(f"Warning: Could not import {module_name} to read description: {e}")
                description = f"Agent {agent_name}"

            config = AgentConfig(
                name=agent_name,
                module=a2a_module_name,
                port=current_port,
                url=f"http://127.0.0.1:{current_port}/.well-known/agent-card.json",
                description=description
            )
            agents.append(config)
            current_port += 1
    
    return agents
