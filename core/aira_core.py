import json
import os

MEMORY_FILE = os.path.expanduser(
    "~/BrayoOS/memory/aira_brain.json"
)


class AIRA:

    def __init__(self):
        self.memory = self.load()

    def load(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE) as f:
                return json.load(f)

        return {
            "projects": [],
            "goals": [],
            "notes": []
        }

    def save(self):
        os.makedirs(
            os.path.dirname(MEMORY_FILE),
            exist_ok=True
        )

        with open(MEMORY_FILE, "w") as f:
            json.dump(
                self.memory,
                f,
                indent=2
            )

    def remember(
        self,
        category,
        text
    ):
        if category not in self.memory:
            self.memory[category] = []

        self.memory[category].append(text)

        self.save()

        return True

    def recall(
        self,
        category
    ):
        return self.memory.get(
            category,
            []
        )
