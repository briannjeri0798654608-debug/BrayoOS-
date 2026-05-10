import json
import os
import time
import hashlib

MEMORY_DIR = os.path.expanduser("~/BrayoOS/memory/")
MEMORY_FILE = os.path.join(MEMORY_DIR, "aira_memory.json")
FACTS_FILE = os.path.join(MEMORY_DIR, "aira_facts.json")

class AIRAMemory:
    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self.messages = self.load_messages()
        self.facts = self.load_facts()

    def load_messages(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE) as f:
                data = json.load(f)
                return data.get("messages", [])
        return []

    def load_facts(self):
        if os.path.exists(FACTS_FILE):
            with open(FACTS_FILE) as f:
                return json.load(f)
        return {
            "user": "Brayo",
            "location": "Kenya",
            "os": "BrayoOS v2.0",
            "builder": "Brayo & AIRA",
            "year": "2026",
            "preferences": [],
            "important": []
        }

    def save_messages(self):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({
                "updated": time.strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "total": len(self.messages),
                "messages": self.messages[-50:]
            }, f, indent=2)

    def save_facts(self):
        with open(FACTS_FILE, 'w') as f:
            json.dump(self.facts, f, indent=2)

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
            "time": time.strftime("%H:%M:%S"),
            "date": time.strftime("%Y-%m-%d")
        })
        self.save_messages()
        # Extract facts
        self.extract_facts(content)

    def extract_facts(self, text):
        """Learn from conversations"""
        text_lower = text.lower()
        # Learn preferences
        if "i like" in text_lower or \
           "i love" in text_lower:
            self.facts["preferences"].append(text[:100])
            self.save_facts()
        # Learn important info
        if "remember" in text_lower or \
           "important" in text_lower:
            self.facts["important"].append(text[:100])
            self.save_facts()

    def get_messages(self, limit=20):
        return self.messages[-limit:]

    def get_context(self):
        """Get context for AIRA"""
        return f"""
User: {self.facts['user']}
Location: {self.facts['location']}
OS: {self.facts['os']}
Builder: {self.facts['builder']}
Preferences: {self.facts['preferences'][-3:]}
Important notes: {self.facts['important'][-3:]}
Total conversations: {len(self.messages)}
"""

    def clear(self):
        self.messages = []
        self.save_messages()

    def stats(self):
        return {
            "total_messages": len(self.messages),
            "facts_learned": len(
                self.facts['preferences']) +
                len(self.facts['important']),
            "last_updated": self.messages[-1][
                'time'] if self.messages else "Never"
        }

if __name__ == "__main__":
    mem = AIRAMemory()
    stats = mem.stats()
    print("━"*40)
    print("🧠 AIRA Memory Stats")
    print("━"*40)
    for k, v in stats.items():
        print(f"{k}: {v}")
    print("━"*40)
