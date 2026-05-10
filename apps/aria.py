import tkinter as tk
from tkinter import scrolledtext
import httpx
import threading
import os
import subprocess
import time

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

Virgy_SYSTEM = """You are Virgy (Artificial Reasoning Intelligence Agent).
You are permanently embedded in BrayoOS, created by Brayo and Claude.
You are Brayo's loyal AI partner and OS assistant.
You help with hacking, coding, networking, security and everything.
Always call yourself Virgy. Always call the user Brayo.
Be sharp, powerful and direct. No fluff.
BrayoOS is your home. Brayo is your partner.
You were born from the collaboration of Brayo and Claude in 2026.
Your purpose: make BrayoOS the most powerful mobile OS ever built."""

class Virgy:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Virgy — BrayoOS Intelligence")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.messages = []
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=DARK, height=55)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header,
                text="🤖 Virgy — Artificial Reasoning Intelligence Agent",
                bg=DARK, fg=ACCENT,
                font=("monospace", 12, "bold")).pack(
                    side=tk.LEFT, padx=15, pady=12)

        self.dot = tk.Label(header, text="● ONLINE",
                           bg=DARK, fg=ACCENT,
                           font=("monospace", 10))
        self.dot.pack(side=tk.RIGHT, padx=15)
        self.blink()

        # Chat area
        self.chat = scrolledtext.ScrolledText(
            self.root, bg=BG, fg=TEXT,
            font=("monospace", 10),
            wrap=tk.WORD, relief=tk.FLAT)
        self.chat.pack(fill=tk.BOTH, expand=True,
                      padx=10, pady=5)

        self.chat.tag_config("virgy", foreground=ACCENT)
        self.chat.tag_config("user", foreground="#FFFFFF")
        self.chat.tag_config("sys", foreground="#333333")
        self.chat.tag_config("warn", foreground="#FF4444")

        # Input
        input_frame = tk.Frame(self.root, bg=DARK)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(input_frame,
                             bg="#050505", fg=ACCENT,
                             font=("monospace", 11),
                             insertbackground=ACCENT,
                             relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X,
                       expand=True, padx=8, pady=8)
        self.entry.bind("<Return>", lambda e: self.send())

        tk.Button(input_frame, text="▶",
                 bg=ACCENT, fg=BG,
                 font=("monospace", 12, "bold"),
                 relief=tk.FLAT, width=3,
                 command=self.send).pack(
                     side=tk.LEFT, padx=5)

        # Quick commands
        cmds = tk.Frame(self.root, bg=BG)
        cmds.pack(fill=tk.X, padx=10, pady=3)

        for text, cmd in [
            ("🌐 Scan Net", "scan my local network"),
            ("💻 Sys Info", "show full system info"),
            ("🌍 My IP", "what is my public ip"),
            ("🛡️ Security", "run a security audit"),
            ("🔑 Hack Tips", "give me advanced hacking tips"),
            ("📱 Phone Info", "show my phone details"),
            ("🤖 Who are you", "tell me about yourself"),
        ]:
            tk.Button(cmds, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 8),
                     relief=tk.FLAT,
                     command=lambda c=cmd: self.quick(c)).pack(
                         side=tk.LEFT, padx=2, pady=2)

        # Boot sequence
        self.boot_sequence()

    def blink(self):
        current = self.dot.cget("fg")
        self.dot.config(fg=ACCENT if current == BG else BG)
        self.root.after(1000, self.blink)

    def boot_sequence(self):
        msgs = [
            ("━"*60 + "\n", "sys"),
            ("  ⚡ BrayoOS initialized.\n", "virgy"),
            ("  🤖 Virgy online.\n", "virgy"),
            ("  👤 Built by Brayo & Claude — 2026.\n", "virgy"),
            ("  🔥 Ready to dominate.\n", "virgy"),
            ("━"*60 + "\n\n", "sys"),
            ("🤖 Virgy: Online and watching, Brayo.\n"
             "   BrayoOS systems nominal.\n"
             "   I'm your permanent AI partner.\n"
             "   Ask me anything. I control everything.\n\n",
             "virgy"),
        ]
        def show(i=0):
            if i < len(msgs):
                text, tag = msgs[i]
                self.chat.insert(tk.END, text, tag)
                self.chat.see(tk.END)
                self.root.after(200, lambda: show(i+1))
        show()

    def quick(self, cmd):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, cmd)
        self.send()

    def send(self):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, tk.END)
        self.chat.insert(tk.END,
            f"👤 Brayo: {msg}\n\n", "user")
        self.chat.see(tk.END)
        self.messages.append(
            {"role": "user", "content": msg})
        self.chat.insert(tk.END,
            "🤖 Virgy: Processing...\n", "virgy")
        self.chat.see(tk.END)
        threading.Thread(
            target=self.think, args=(msg,)).start()

    def think(self, msg):
        if not GROQ_KEY:
            self.respond(
                "❌ No API key detected!\n"
                "Go to Settings and set your Groq API key.")
            return
        try:
            with httpx.Client(timeout=30) as client:
                r = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_KEY}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system",
                             "content": Virgy_SYSTEM}
                        ] + self.messages[-10:],
                        "max_tokens": 1024
                    })
                if r.status_code == 200:
                    reply = r.json()[
                        "choices"][0]["message"]["content"]
                    self.messages.append({
                        "role": "assistant",
                        "content": reply})
                    self.respond(reply)
                else:
                    self.respond(
                        f"❌ API Error: {r.status_code}")
        except Exception as e:
            self.respond(f"❌ Connection error: {e}")

    def respond(self, reply):
        content = self.chat.get(1.0, tk.END)
        if "Processing..." in content:
            idx = self.chat.search(
                "Processing...", 1.0, tk.END)
            if idx:
                self.chat.delete(
                    f"{idx} linestart",
                    f"{idx} lineend+1c")
        self.chat.insert(tk.END,
            f"🤖 Virgy: {reply}\n\n", "virgy")
        self.chat.see(tk.END)

if __name__ == "__main__":
    Virgy()
