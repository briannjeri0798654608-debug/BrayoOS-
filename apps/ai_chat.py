import tkinter as tk
from tkinter import scrolledtext
import httpx
import os
import threading
import json

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

def ask_groq(prompt, callback):
    def run():
        if not GROQ_KEY:
            callback("❌ No Groq API key set!\nSet: export GROQ_API_KEY=your_key")
            return
        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_KEY}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 1024
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    reply = data["choices"][0]["message"]["content"]
                    callback(reply)
                else:
                    callback(f"❌ Error: {response.status_code}\n{response.text}")
        except Exception as e:
            callback(f"❌ Connection error: {e}")
    threading.Thread(target=run).start()

class AIChat:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 BrayoOS AI Chat")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🤖 AI Chat (Groq LLaMA 3.3)",
                bg=BG, fg=ACCENT,
                font=("monospace", 14, "bold")).pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=TEXT,
            font=("monospace", 10), wrap=tk.WORD)
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(frame, bg=DARK, fg=ACCENT,
                             font=("monospace", 11),
                             insertbackground=ACCENT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda e: self.send())

        tk.Button(frame, text="Send", bg=ACCENT, fg=BG,
                 font=("monospace", 11, "bold"),
                 command=self.send).pack(side=tk.LEFT, padx=5)

        self.chat_area.insert(tk.END,
            "💬 BrayoOS AI Chat\n"
            "Ask anything! Using Groq LLaMA 3.3 70B\n\n")

    def send(self):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, tk.END)
        self.chat_area.insert(tk.END, f"\n👤 You: {msg}\n")
        self.chat_area.see(tk.END)
        self.chat_area.insert(tk.END, "🤖 AI: Thinking...\n")
        self.chat_area.see(tk.END)
        ask_groq(msg, self.receive)

    def receive(self, reply):
        # Remove "🤖 AI: Thinking..." line
        content = self.chat_area.get(1.0, tk.END)
        if "Thinking..." in content:
            self.chat_area.delete("end-2c linestart", "end-1c")
        self.chat_area.insert(tk.END, f"🤖 AI: {reply}\n")
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    AIChat()
