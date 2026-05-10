import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import os
import random
from datetime import datetime

MEMORY_FILE = os.path.expanduser("~/BrayoOS/memory/virgy_neural.json")
os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

class VirgyNeuralCore:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Virgy Neural Core")
        self.root.geometry("700x550")
        self.root.configure(bg="#0D0D0D")
        self.memory = self.load_memory()
        self.running = True
        self.build_ui()
        self.start_learning()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE) as f:
                return json.load(f)
        return {"sessions": 0, "patterns": [], "predictions": [], "user_habits": {}, "threat_score": 0}

    def save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    def build_ui(self):
        tk.Label(self.root, text="🧠 Virgy NEURAL CORE", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=10)
        tk.Label(self.root, text="[ LEARNING YOUR PATTERNS — SESSION #{} ]".format(
            self.memory["sessions"]), font=("Courier", 9), bg="#0D0D0D", fg="#004400").pack()

        stats = tk.Frame(self.root, bg="#0D0D0D")
        stats.pack(fill="x", padx=20, pady=10)

        self.stat_labels = {}
        for col, (label, key) in enumerate([
            ("SESSIONS", "sessions"), ("PATTERNS", "patterns"),
            ("THREAT IQ", "threat_score"), ("PREDICTIONS", "predictions")
        ]):
            f = tk.Frame(stats, bg="#001100", relief="flat")
            f.grid(row=0, column=col, padx=5, sticky="ew")
            stats.columnconfigure(col, weight=1)
            tk.Label(f, text=label, font=("Courier", 7), bg="#001100", fg="#004400").pack(pady=2)
            val = self.memory.get(key, 0)
            display = str(val) if not isinstance(val, list) else str(len(val))
            lbl = tk.Label(f, text=display, font=("Courier", 14, "bold"), bg="#001100", fg="#00FF41")
            lbl.pack(pady=2)
            self.stat_labels[key] = lbl

        tk.Label(self.root, text="◈ Virgy THOUGHT STREAM", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=20)

        self.feed = tk.Text(self.root, height=12, bg="#000800", fg="#00FF41",
                            font=("Courier", 9), relief="flat", state="disabled")
        self.feed.pack(fill="both", padx=20, pady=5)

        tk.Label(self.root, text="◈ Virgy PREDICTS YOUR NEXT MOVE", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#FF6600").pack(anchor="w", padx=20)

        self.predict_box = tk.Label(self.root, text="Analyzing...", font=("Courier", 11),
                                    bg="#110500", fg="#FF6600", wraplength=640, justify="left")
        self.predict_box.pack(fill="x", padx=20, pady=5)

        btn_frame = tk.Frame(self.root, bg="#0D0D0D")
        btn_frame.pack(pady=10)

        for text, cmd in [
            ("🧠 TRAIN Virgy", self.train), ("📊 SHOW PATTERNS", self.show_patterns),
            ("🗑️ RESET MEMORY", self.reset_memory)
        ]:
            tk.Button(btn_frame, text=text, command=cmd,
                      font=("Courier", 9, "bold"), bg="#001a00", fg="#00FF41",
                      relief="flat", padx=10, pady=5).pack(side="left", padx=5)

        tk.Label(self.root, text="BrayoOS Neural Engine v1.0 • Brayo & Virgy 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=5)

    def log(self, msg):
        self.feed.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.feed.insert("end", f"[{ts}] {msg}\n")
        self.feed.see("end")
        self.feed.config(state="disabled")

    def start_learning(self):
        self.memory["sessions"] += 1
        self.save_memory()
        threading.Thread(target=self.learn_loop, daemon=True).start()

    def learn_loop(self):
        thoughts = [
            "Scanning usage patterns...",
            "Analyzing time-based behavior...",
            "Mapping app launch frequency...",
            "Calculating threat probability...",
            "Updating neural weights...",
            "Detecting anomalies in session...",
            "Cross-referencing memory bank...",
            "Predicting next 3 user actions...",
            "Encrypting learned data to vault...",
            "Virgy learning complete. Adapting..."
        ]
        predictions = [
            "You will open Terminal in the next 2 minutes",
            "Network scan likely within this session",
            "High probability of Vault access detected",
            "Virgy suggests: backup your files now",
            "You are more active between 11PM - 2AM",
            "Suspicious pattern: repeated failed auth detected",
            "CPU spike predicted in 5 minutes",
            "You tend to run WiFi scanner after boot",
        ]
        while self.running:
            thought = random.choice(thoughts)
            self.root.after(0, self.log, f"🧠 {thought}")
            pred = random.choice(predictions)
            self.root.after(0, self.predict_box.config, {"text": f"▶ {pred}"})
            self.memory["threat_score"] = min(100, self.memory["threat_score"] + random.randint(0, 3))
            if len(self.memory["patterns"]) < 50:
                self.memory["patterns"].append(thought)
            if len(self.memory["predictions"]) < 100:
                self.memory["predictions"].append(pred)
            self.save_memory()
            self.root.after(0, self.update_stats)
            time.sleep(random.uniform(2, 4))

    def update_stats(self):
        self.stat_labels["sessions"].config(text=str(self.memory["sessions"]))
        self.stat_labels["patterns"].config(text=str(len(self.memory["patterns"])))
        self.stat_labels["threat_score"].config(text=str(self.memory["threat_score"]))
        self.stat_labels["predictions"].config(text=str(len(self.memory["predictions"])))

    def train(self):
        self.log("⚡ Manual training triggered by Brayo...")
        count = sum(len(files) for _, _, files in os.walk(os.path.expanduser("~/BrayoOS/")))
        self.log(f"✅ Learned from {count} BrayoOS files. Neural map updated.")
        self.memory["patterns"].append(f"manual_train_{count}_files")
        self.save_memory()

    def show_patterns(self):
        self.log("📊 TOP PATTERNS LEARNED:")
        for p in self.memory["patterns"][-5:]:
            self.log(f"  → {p}")

    def reset_memory(self):
        self.memory = {"sessions": 0, "patterns": [], "predictions": [], "user_habits": {}, "threat_score": 0}
        self.save_memory()
        self.log("🗑️ Neural memory wiped. Virgy reborn from zero.")

if __name__ == "__main__":
    root = tk.Tk()
    VirgyNeuralCore(root)
    root.mainloop()
