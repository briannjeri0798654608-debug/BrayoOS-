import json
import os
import time

MEMORY_FILE = os.path.expanduser(
    "~/BrayoOS/memory/aria_memory.json")

def save_memory(messages):
    os.makedirs(os.path.dirname(MEMORY_FILE),
                exist_ok=True)
    data = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "messages": messages[-20:]
    }
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE) as f:
            data = json.load(f)
            return data.get("messages", [])
    return []

def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
