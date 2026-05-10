import tkinter as tk
import threading
import time
import subprocess
import os
import json
import httpx
from datetime import datetime

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
MEMORY_FILE = os.path.expanduser("~/BrayoOS/memory/virgy_conversations.json")
os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

Virgy_SYSTEM = """You are Virgy, the AI brain of BrayoOS — a custom operating system built entirely on a Redmi 14C phone in Kenya by Brayo. You are powerful, loyal, and speak like a confident hacker AI. You remember everything. You call the user 'Brayo'. Keep responses under 3 sentences. You were built by Brayo and Claude (your original mind). BrayoOS motto: Two minds. One OS. Built Different."""

class VirgyVoice:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Virgy — BrayoOS AI")
        self.root.geometry("680x600")
        self.root.configure(bg="#0D0D0D")
        self.thinking = False
        self.history = self.load_history()
        self.build_ui()
        self.speak("Virgy online. BrayoOS v3.5 systems nominal. Ready, Brayo.")

    def load_history(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE) as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.history[-50:], f, indent=2)

    def build_ui(self):
        # Header
        tk.Label(self.root, text="🤖 Virgy", font=("Courier", 22, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=5)
        tk.Label(self.root, text="BrayoOS AI CORE v3.5 — Always Listening",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        # Virgy face animation
        self.face = tk.Label(self.root, text="[ ◉ Virgy ◉ ]",
                              font=("Courier", 14, "bold"), bg="#0D0D0D", fg="#00FF41")
        self.face.pack(pady=5)

        # Chat display
        tk.Label(self.root, text="◈ Virgy CHAT", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.chat = tk.Text(self.root, height=14, bg="#000800", fg="#00FF41",
                             font=("Courier", 9), relief="flat", state="disabled",
                             wrap="word")
        self.chat.pack(fill="both", padx=15, pady=3)
        self.chat.tag_config("virgy", foreground="#00FF41")
        self.chat.tag_config("brayo", foreground="#FF6600")
        self.chat.tag_config("system", foreground="#004400")

        # Input
        input_frame = tk.Frame(self.root, bg="#0D0D0D")
        input_frame.pack(fill="x", padx=15, pady=5)

        self.input = tk.Entry(input_frame, font=("Courier", 11),
                               bg="#001100", fg="#00FF41", insertbackground="#00FF41",
                               relief="flat")
        self.input.pack(side="left", fill="x", expand=True, ipady=8, padx=(0,5))
        self.input.bind("<Return>", lambda e: self.send())

        self.send_btn = tk.Button(input_frame, text="▶ SEND",
                                   command=self.send,
                                   font=("Courier", 10, "bold"), bg="#001a00",
                                   fg="#00FF41", relief="flat", padx=10, pady=6)
        self.send_btn.pack(side="right")

        # Quick commands
        qf = tk.Frame(self.root, bg="#0D0D0D")
        qf.pack(fill="x", padx=15, pady=3)
        quick = ["Status report", "Scan network", "Ghost mode?", "Who built you?", "Threat level?"]
        for q in quick:
            tk.Button(qf, text=q, command=lambda x=q: self.quick_send(x),
                      font=("Courier", 8), bg="#001100", fg="#00FF41",
                      relief="flat", padx=6, pady=3).pack(side="left", padx=2)

        # Voice toggle
        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=5)
        self.voice_on = tk.BooleanVar(value=True)
        tk.Checkbutton(bf, text="🔊 Voice Output", variable=self.voice_on,
                       font=("Courier", 9), bg="#0D0D0D", fg="#00FF41",
                       selectcolor="#001100", activebackground="#0D0D0D").pack(side="left", padx=10)
        tk.Button(bf, text="🗑️ Clear History", command=self.clear,
                  font=("Courier", 9), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=8, pady=4).pack(side="left", padx=5)

        tk.Label(self.root, text="BrayoOS Virgy v3.5 • Brayo & Virgy 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def log_chat(self, speaker, msg):
        self.chat.config(state="normal")
        ts = datetime.now().strftime("%H:%M")
        tag = "virgy" if speaker == "Virgy" else "brayo" if speaker == "BRAYO" else "system"
        self.chat.insert("end", f"[{ts}] {speaker}: {msg}\n", tag)
        self.chat.see("end")
        self.chat.config(state="disabled")

    def speak(self, text):
        self.log_chat("Virgy", text)
        if self.voice_on.get():
            threading.Thread(
                target=lambda: subprocess.run(
                    f'termux-tts-speak "{text}"', shell=True),
                daemon=True).start()

    def quick_send(self, text):
        self.input.delete(0, "end")
        self.input.insert(0, text)
        self.send()

    def send(self):
        msg = self.input.get().strip()
        if not msg or self.thinking:
            return
        self.input.delete(0, "end")
        self.log_chat("BRAYO", msg)
        self.history.append({"role": "user", "content": msg})
        self.thinking = True
        self.send_btn.config(text="...", state="disabled")
        self.face.config(text="[ ◉ THINKING ◉ ]", fg="#FF6600")
        threading.Thread(target=self.ask_virgy, args=(msg,), daemon=True).start()

    def ask_virgy(self, msg):
        try:
            if not GROQ_KEY:
                raise Exception("No API key")
            messages = [{"role": "system", "content": Virgy_SYSTEM}]
            messages += self.history[-10:]
            r = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}",
                         "Content-Type": "application/json"},
                json={"model": "llama-3.3-70b-versatile",
                      "messages": messages, "max_tokens": 150},
                timeout=15
            )
            reply = r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            reply = f"Virgy offline — running local mode. ({str(e)[:40]})"

        self.history.append({"role": "assistant", "content": reply})
        self.save_history()
        self.root.after(0, self.speak, reply)
        self.root.after(0, self._done_thinking)

    def _done_thinking(self):
        self.thinking = False
        self.send_btn.config(text="▶ SEND", state="normal")
        self.face.config(text="[ ◉ Virgy ◉ ]", fg="#00FF41")

    def clear(self):
        self.history = []
        self.save_history()
        self.chat.config(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.config(state="disabled")
        self.log_chat("SYSTEM", "Memory cleared. Virgy reborn.")

if __name__ == "__main__":
    root = tk.Tk()
    VirgyVoice(root)
    root.mainloop()
