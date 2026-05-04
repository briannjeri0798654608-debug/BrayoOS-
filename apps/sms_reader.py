# BrayoOS — Built by Brayo & ARIA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import json

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class SMSReader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📱 SMS Reader")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📱 SMS Reader",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [("📥 Inbox", self.load_inbox),
                          ("📤 Sent", self.load_sent),
                          ("🔄 Refresh", self.load_inbox)]:
            tk.Button(btn_frame, text=text, bg=DARK,
                     fg=ACCENT, command=cmd,
                     font=("monospace", 10),
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=3)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=TEXT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.status = tk.Label(self.root, text="Ready",
                              bg=DARK, fg=ACCENT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def load_inbox(self):
        self.output.delete(1.0, tk.END)
        self.status.config(text="Loading inbox...")
        def run():
            try:
                result = subprocess.run(
                    ["termux-sms-list", "-l", "50"],
                    capture_output=True, text=True, timeout=10)
                messages = json.loads(result.stdout)
                self.output.delete(1.0, tk.END)
                for msg in messages:
                    self.output.insert(tk.END,
                        f"📨 From: {msg.get('number','Unknown')}\n"
                        f"📅 {msg.get('received','')}\n"
                        f"💬 {msg.get('body','')}\n"
                        f"{'─'*50}\n")
                self.status.config(text=f"✅ {len(messages)} messages")
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}\n")
                self.output.insert(tk.END,
                    "Make sure Termux:API app is installed!\n")
                self.status.config(text="❌ Error")
        threading.Thread(target=run).start()

    def load_sent(self):
        self.output.delete(1.0, tk.END)
        self.status.config(text="Loading sent...")
        def run():
            try:
                result = subprocess.run(
                    ["termux-sms-list", "-l", "50", "-t", "sent"],
                    capture_output=True, text=True, timeout=10)
                messages = json.loads(result.stdout)
                self.output.delete(1.0, tk.END)
                for msg in messages:
                    self.output.insert(tk.END,
                        f"📤 To: {msg.get('number','Unknown')}\n"
                        f"📅 {msg.get('received','')}\n"
                        f"💬 {msg.get('body','')}\n"
                        f"{'─'*50}\n")
                self.status.config(text=f"✅ {len(messages)} sent")
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}\n")
                self.status.config(text="❌ Error")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    SMSReader()
