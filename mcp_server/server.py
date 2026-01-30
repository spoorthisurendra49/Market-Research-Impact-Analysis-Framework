from datetime import datetime

LOG_FILE = "storage/logs.txt"

def log(agent: str, tool: str):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.utcnow()}] {agent} calling tool: {tool}\n")
