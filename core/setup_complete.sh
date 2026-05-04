#!/bin/bash
echo "⚡ BrayoOS Complete Setup Starting..."

# Create Telegram Bot
cat > ~/BrayoOS/apps/telegram_bot.py << 'BOTEOF'
import httpx
import os
import asyncio
import json

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
offset = 0

def ask_groq(prompt):
    with httpx.Client() as client:
        r = client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024
            },
            timeout=30
        )
        return r.json()["choices"][0]["message"]["content"]

def send_message(chat_id, text):
    with httpx.Client() as client:
        client.post(f"{API}/sendMessage",
                   json={"chat_id": chat_id, "text": text})

def get_updates():
    global offset
    with httpx.Client() as client:
        r = client.get(f"{API}/getUpdates",
                      params={"offset": offset, "timeout": 30},
                      timeout=35)
        return r.json().get("result", [])

def run():
    global offset
    print("🤖 BrayoOS Telegram Bot Running...")
    while True:
        try:
            updates = get_updates()
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")
                if text and chat_id:
                    print(f"Message: {text}")
                    if text == "/start":
                        send_message(chat_id, "⚡ BrayoOS Bot Active!\nSend any message to chat with AI.")
                    elif text == "/ip":
                        import socket
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(("8.8.8.8", 80))
                        ip = s.getsockname()[0]
                        send_message(chat_id, f"📍 IP: {ip}")
                    else:
                        reply = ask_groq(text)
                        send_message(chat_id, f"🤖 {reply}")
        except Exception as e:
            print(f"Error: {e}")
            import time
            time.sleep(5)

if __name__ == "__main__":
    run()
BOTEOF

# Create Code Editor
cat > ~/BrayoOS/apps/code_editor.py << 'EDEOF'
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"

class CodeEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS - Code Editor")
        self.root.configure(bg=BG)
        self.root.geometry("900x700")
        self.current_file = None
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        # Menu bar
        menubar = tk.Menu(self.root, bg="#1A1A1A", fg=TEXT)
        file_menu = tk.Menu(menubar, tearoff=0, bg="#1A1A1A", fg=TEXT)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        menubar.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menubar, tearoff=0, bg="#1A1A1A", fg=TEXT)
        run_menu.add_command(label="Run Python", command=self.run_python)
        run_menu.add_command(label="Run Bash", command=self.run_bash)
        menubar.add_cascade(label="Run", menu=run_menu)
        self.root.config(menu=menubar)

        tk.Label(self.root, text="💻 Code Editor",
                bg=BG, fg=ACCENT,
                font=("monospace", 14, "bold")).pack(pady=5)

        # Editor
        self.editor = scrolledtext.ScrolledText(
            self.root, bg="#1A1A1A", fg=ACCENT,
            font=("monospace", 12), wrap=tk.NONE,
            insertbackground=ACCENT)
        self.editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Output
        tk.Label(self.root, text="Output:",
                bg=BG, fg=TEXT,
                font=("monospace", 10)).pack(anchor=tk.W, padx=10)
        self.output = scrolledtext.ScrolledText(
            self.root, bg="#0A0A0A", fg="#00FF41",
            font=("monospace", 10), height=8)
        self.output.pack(fill=tk.X, padx=10, pady=5)

        # Status
        self.status = tk.Label(self.root, text="New File",
                              bg="#1A1A1A", fg=ACCENT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def new_file(self):
        self.editor.delete(1.0, tk.END)
        self.current_file = None
        self.status.config(text="New File")

    def open_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path) as f:
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, f.read())
            self.current_file = path
            self.status.config(text=path)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as f:
                f.write(self.editor.get(1.0, tk.END))
            self.status.config(text=f"Saved: {self.current_file}")
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.current_file = path
            self.save_file()

    def run_python(self):
        self.save_file()
        if self.current_file:
            import subprocess
            result = subprocess.run(
                ["python", self.current_file],
                capture_output=True, text=True)
            self.output.delete(1.0, tk.END)
            self.output.insert(1.0, result.stdout + result.stderr)

    def run_bash(self):
        self.save_file()
        if self.current_file:
            import subprocess
            result = subprocess.run(
                ["bash", self.current_file],
                capture_output=True, text=True)
            self.output.delete(1.0, tk.END)
            self.output.insert(1.0, result.stdout + result.stderr)

if __name__ == "__main__":
    CodeEditor()
EDEOF

# Create System Monitor
cat > ~/BrayoOS/apps/system_monitor.py << 'SYSEOF'
import tkinter as tk
import subprocess
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"

class SystemMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS - System Monitor")
        self.root.configure(bg=BG)
        self.root.geometry("600x500")
        self.build_ui()
        self.update_stats()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📊 System Monitor",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        self.stats = tk.Text(self.root, bg="#1A1A1A", fg=ACCENT,
                            font=("monospace", 11))
        self.stats.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Button(self.root, text="🔄 Refresh",
                 bg=ACCENT, fg=BG,
                 command=self.update_stats).pack(pady=5)

    def update_stats(self):
        self.stats.delete(1.0, tk.END)
        # CPU
        try:
            with open("/proc/loadavg") as f:
                load = f.read().strip()
            self.stats.insert(tk.END, f"⚡ CPU Load: {load}\n\n")
        except:
            pass
        # Memory
        try:
            with open("/proc/meminfo") as f:
                mem = f.read()
            for line in mem.split('\n')[:5]:
                self.stats.insert(tk.END, f"💾 {line}\n")
        except:
            pass
        # Storage
        try:
            result = subprocess.run(["df", "-h", "/data"],
                                  capture_output=True, text=True)
            self.stats.insert(tk.END, f"\n💿 Storage:\n{result.stdout}\n")
        except:
            pass
        # Battery
        try:
            result = subprocess.run(["termux-battery-status"],
                                  capture_output=True, text=True)
            self.stats.insert(tk.END, f"\n🔋 Battery:\n{result.stdout}\n")
        except:
            pass
        self.root.after(5000, self.update_stats)

if __name__ == "__main__":
    SystemMonitor()
SYSEOF

# Update desktop with all apps
cat > ~/BrayoOS/core/desktop.py << 'DESKEOF'
import tkinter as tk
from tkinter import ttk
import subprocess
import os
import threading
import time

BG_COLOR = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
TASKBAR_BG = "#1A1A1A"

class BrayoOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v2.0")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes('-fullscreen', True)
        self.build_desktop()
        self.update_clock()
        self.root.mainloop()

    def build_desktop(self):
        # Taskbar at bottom
        self.taskbar = tk.Frame(self.root, bg=TASKBAR_BG, height=50)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.taskbar.pack_propagate(False)

        tk.Label(self.taskbar, text="⚡ BrayoOS",
                bg=TASKBAR_BG, fg=ACCENT,
                font=("monospace", 13, "bold")).pack(side=tk.LEFT, padx=10)

        self.clock = tk.Label(self.taskbar, text="",
                             bg=TASKBAR_BG, fg=TEXT,
                             font=("monospace", 12))
        self.clock.pack(side=tk.RIGHT, padx=10)

        # Desktop area
        self.desktop = tk.Frame(self.root, bg=BG_COLOR)
        self.desktop.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.desktop,
                text="⚡ BrayoOS Desktop Environment",
                bg=BG_COLOR, fg=ACCENT,
                font=("monospace", 18, "bold")).pack(pady=20)

        # App Grid
        grid = tk.Frame(self.desktop, bg=BG_COLOR)
        grid.pack(expand=True)

        apps = [
            ("🖥️\nTerminal", self.open_terminal),
            ("🤖\nAI Chat", self.open_ai),
            ("🌐\nNetwork", self.open_network),
            ("📁\nFiles", self.open_files),
            ("💻\nCode Editor", self.open_editor),
            ("📊\nSystem", self.open_sysmon),
            ("🤖\nTelegram Bot", self.open_bot),
            ("⚙️\nSettings", self.open_settings),
        ]

        row, col = 0, 0
        for name, cmd in apps:
            btn = tk.Button(grid, text=name,
                          bg=TASKBAR_BG, fg=ACCENT,
                          font=("monospace", 11),
                          relief=tk.FLAT, cursor="hand2",
                          command=cmd, width=12, height=4,
                          activebackground=ACCENT,
                          activeforeground=BG_COLOR)
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def update_clock(self):
        self.clock.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def launch(self, script):
        subprocess.Popen(["python", os.path.expanduser(script)])

    def open_terminal(self):
        subprocess.Popen(["bash"])

    def open_ai(self):
        self.launch("~/BrayoOS/apps/ai_chat.py")

    def open_network(self):
        self.launch("~/BrayoOS/apps/network.py")

    def open_files(self):
        self.launch("~/BrayoOS/apps/files.py")

    def open_editor(self):
        self.launch("~/BrayoOS/apps/code_editor.py")

    def open_sysmon(self):
        self.launch("~/BrayoOS/apps/system_monitor.py")

    def open_bot(self):
        self.launch("~/BrayoOS/apps/telegram_bot.py")

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.configure(bg=BG_COLOR)
        win.geometry("400x300")
        tk.Label(win, text="⚙️ BrayoOS Settings",
                bg=BG_COLOR, fg=ACCENT,
                font=("monospace", 14, "bold")).pack(pady=20)
        tk.Label(win, text="Version: BrayoOS v2.0",
                bg=BG_COLOR, fg=TEXT,
                font=("monospace", 11)).pack()
        tk.Label(win, text="Built by: Brayo",
                bg=BG_COLOR, fg=TEXT,
                font=("monospace", 11)).pack()

if __name__ == "__main__":
    BrayoOS()
DESKEOF

echo "✅ BrayoOS Complete Setup Done!"
echo "👉 Type 'brayos' to start!"
