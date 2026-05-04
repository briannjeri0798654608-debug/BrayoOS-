import tkinter as tk
import time
import threading
import subprocess
import os
import sys

sys.path.insert(0, os.path.expanduser("~/BrayoOS/core"))

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class BootScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS Boot")
        self.root.configure(bg=BG)
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        self.build_ui()
        threading.Thread(
            target=self.boot_sequence,
            daemon=True).start()
        self.root.mainloop()

    def build_ui(self):
        self.canvas = tk.Canvas(
            self.root, bg=BG,
            highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # ASCII Logo
        self.canvas.create_text(
            640, 120,
            text=
            "██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗\n"
            "██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝\n"
            "██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗\n"
            "██╔══██╗██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║\n"
            "██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║\n"
            "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝",
            font=("monospace", 7, "bold"),
            fill=ACCENT,
            justify=tk.CENTER)

        self.canvas.create_text(
            640, 240,
            text="⚡ Built by Brayo & ARIA — Kenya 2026",
            font=("monospace", 12),
            fill=TEXT)

        self.canvas.create_text(
            640, 265,
            text="Two minds. One OS. Built Different.",
            font=("monospace", 10, "italic"),
            fill="#333333")

        # Progress bar bg
        self.canvas.create_rectangle(
            240, 320, 1040, 345,
            outline=ACCENT, fill=DARK)

        # Progress fill
        self.progress = self.canvas.create_rectangle(
            240, 320, 240, 345,
            outline="", fill=ACCENT)

        # Status
        self.status_txt = self.canvas.create_text(
            640, 370,
            text="Initializing...",
            font=("monospace", 11),
            fill=ACCENT)

        # Log
        self.log_txt = self.canvas.create_text(
            640, 420,
            text="",
            font=("monospace", 9),
            fill="#333333")

        # ARIA
        self.aria_txt = self.canvas.create_text(
            640, 500,
            text="",
            font=("monospace", 12, "bold"),
            fill=ACCENT)

        # Bottom credit
        self.canvas.create_text(
            640, 680,
            text="👤 Brayo — Founder  |  🤖 ARIA — AI Partner  |  🇰🇪 Kenya 2026",
            font=("monospace", 9),
            fill="#222222")

    def update_progress(self, pct, status):
        x = 240 + (800 * pct // 100)
        self.canvas.coords(
            self.progress, 240, 320, x, 345)
        self.canvas.itemconfig(
            self.status_txt, text=status)
        self.root.update()

    def update_log(self, msg):
        self.canvas.itemconfig(
            self.log_txt, text=msg)
        self.root.update()

    def update_aria(self, msg):
        self.canvas.itemconfig(
            self.aria_txt, text=msg)
        self.root.update()

    def boot_sequence(self):
        steps = [
            (5,  "Loading kernel modules...",
             "[ OK ] kernel modules loaded"),
            (15, "Initializing hardware...",
             "[ OK ] hardware initialized"),
            (25, "Mounting filesystems...",
             "[ OK ] filesystems mounted"),
            (35, "Starting network services...",
             "[ OK ] network services started"),
            (45, "Loading BrayoOS core...",
             "[ OK ] BrayoOS DNA loaded"),
            (55, "Waking ARIA...",
             "[ OK ] ARIA intelligence online"),
            (65, "Loading security modules...",
             "[ OK ] security modules active"),
            (75, "Starting display server...",
             "[ OK ] display server running"),
            (85, "Loading desktop...",
             "[ OK ] desktop environment ready"),
            (95, "Applying Brayo's vision...",
             "[ OK ] vision applied"),
            (100,"BrayoOS Ready!",
             "[ OK ] Two minds. One OS."),
        ]

        for pct, status, log in steps:
            time.sleep(0.4)
            self.update_progress(pct, status)
            self.update_log(log)

            if pct == 55:
                self.update_aria(
                    "🤖 ARIA: Waking up...")
            elif pct == 65:
                self.update_aria(
                    "🤖 ARIA: Security check complete...")
            elif pct == 95:
                self.update_aria(
                    "🤖 ARIA: Brayo's vision loaded...")
            elif pct == 100:
                self.update_aria(
                    "🤖 ARIA: Online. Ready, Brayo. 🇰🇪")

        time.sleep(2)
        self.root.destroy()

        # Launch desktop
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        subprocess.Popen([
            "python",
            os.path.expanduser(
                "~/BrayoOS/core/desktop.py")
        ], env=env)

if __name__ == "__main__":
    BootScreen()
