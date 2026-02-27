import subprocess
import sys
import time
import os
import signal
from pathlib import Path
from .discovery import discover_agents

def main():
    processes = []

    def cleanup(signum, frame):
        print("\nStopping all agents...")
        for p in processes:
            if p.poll() is None:
                p.terminate()
        time.sleep(1)
        for p in processes:
             if p.poll() is None:
                p.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        # Discover agents dynamically
        print("Discovering agents...")
        agents = discover_agents()
        
        # agents/ サブディレクトリがあればそこを cwd にする
        root = Path(os.getcwd())
        agents_dir = root / "agents"
        agent_cwd = str(agents_dir) if agents_dir.exists() else str(root)

        for agent in agents:
            # print(f"Starting {agent.name} on port {agent.port} (module: {agent.module})...")

            # Passing PORT as env var
            env = os.environ.copy()
            env["PORT"] = str(agent.port)

            p = subprocess.Popen(
                [sys.executable, "-m", agent.module],
                env=env,
                cwd=agent_cwd,
            )
            processes.append(p)

        # Start coordinator agent
        # print("Starting coordinator agent (a4a.agent) on port 8000...")
        env_coord = os.environ.copy()
        env_coord["PORT"] = "8000"
        p_coord = subprocess.Popen(
            [sys.executable, "-m", "a4a.agent"],
            env=env_coord,
            cwd=os.getcwd()
        )
        processes.append(p_coord)

        # print(f"Started {len(processes)} processes. Press Ctrl+C to stop.")
        
        # Keep main thread alive and monitor processes
        while True:
            time.sleep(1)
            # Remove and report processes that have exited
            dead = [p for p in processes if p.poll() is not None]
            for p in dead:
                print(f"Process {p.args} exited with code {p.returncode}")
                processes.remove(p)
    except Exception as e:
        print(f"Error: {e}")
        cleanup(None, None)

if __name__ == "__main__":
    main()
