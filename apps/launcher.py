import tkinter as tk
import subprocess
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class Launcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ BrayoOS Launcher")
        self.root.configure(bg=BG)
        self.root.geometry("700x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root,
                text="⚡ BrayoOS App Launcher",
                bg=BG, fg=ACCENT,
                font=("monospace", 18, "bold")).pack(pady=20)

        grid = tk.Frame(self.root, bg=BG)
        grid.pack(expand=True)

        apps = [
            ("🖥️\nTerminal", "terminal"),
            ("🤖\nAI Chat", "ai_chat.py"),
            ("🌐\nNetwork", "network.py"),
            ("📁\nFiles", "files.py"),
            ("💻\nCode Editor", "code_editor.py"),
            ("📊\nSystem", "system_monitor.py"),
            ("🎵\nMusic", "music_player.py"),
            ("📱\nSMS", "sms_reader.py"),
            ("🔐\nPasswords", "password_manager.py"),
            ("🌍\nIP Tracker", "ip_tracker.py"),
            ("🌐\nBrowser", "mini_browser.py"),
            ("🛡️\nVuln Scan", "vuln_scanner.py"),
            ("🤖\nTelegram", "telegram_bot.py"),
            ("⚙️\nSettings", "settings.py"),
        ]

        row, col = 0, 0
        for name, script in apps:
            tk.Button(grid, text=name,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 11),
                     relief=tk.FLAT,
                     cursor="hand2",
                     command=lambda s=script: self.launch(s),
                     width=12, height=4,
                     activebackground=ACCENT,
                     activeforeground=BG).grid(
                         row=row, column=col,
                         padx=8, pady=8)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def launch(self, script):
        if script == "terminal":
            subprocess.Popen(["bash"])
        else:
            path = os.path.expanduser(
                f"~/BrayoOS/apps/{script}")
            subprocess.Popen(["python", path])

if __name__ == "__main__":
    Launcher()
