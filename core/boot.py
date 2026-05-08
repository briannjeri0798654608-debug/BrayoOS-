import tkinter as tk
import time
import threading
import subprocess
import os
import sys

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class BootScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS")
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
        self.canvas.pack(
            fill=tk.BOTH, expand=True)

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
            640, 235,
            text="⚡ Built by Brayo & ARIA — Kenya 2026",
            font=("monospace", 11),
            fill=TEXT)

        self.canvas.create_text(
            640, 258,
            text="Two minds. One OS. Built Different.",
            font=("monospace", 9, "italic"),
            fill="#333333")

        self.canvas.create_rectangle(
            240, 300, 1040, 322,
            outline=ACCENT, fill=DARK)

        self.progress = self.canvas.create_rectangle(
            240, 300, 240, 322,
            outline="", fill=ACCENT)

        self.status_txt = self.canvas.create_text(
            640, 345,
            text="Initializing...",
            font=("monospace", 10),
            fill=ACCENT)

        self.log_txt = self.canvas.create_text(
            640, 390,
            text="",
            font=("monospace", 8),
            fill="#333333")

        self.aria_txt = self.canvas.create_text(
            640, 480,
            text="",
            font=("monospace", 11, "bold"),
            fill=ACCENT)

        self.canvas.create_text(
            640, 690,
            text="👤 Brayo — Founder  |  🤖 ARIA — AI Partner  |  🇰🇪 Kenya 2026",
            font=("monospace", 8),
            fill="#1A1A1A")

    def update(self, pct, status, log=""):
        x = 240 + (800 * pct // 100)
        self.canvas.coords(
            self.progress, 240, 300, x, 322)
        self.canvas.itemconfig(
            self.status_txt, text=status)
        if log:
            self.canvas.itemconfig(
                self.log_txt, text=log)
        self.root.update()

    def update_aria(self, msg):
        self.canvas.itemconfig(
            self.aria_txt, text=msg)
        self.root.update()

    def boot_sequence(self):
        steps = [
            (10, "Loading kernel...",
             "[ OK ] kernel loaded"),
            (20, "Initializing hardware...",
             "[ OK ] hardware ready"),
            (30, "Mounting filesystems...",
             "[ OK ] filesystems mounted"),
            (40, "Starting network...",
             "[ OK ] network active"),
            (50, "Loading BrayoOS DNA...",
             "[ OK ] DNA verified"),
            (60, "Waking ARIA...",
             "[ OK ] ARIA online"),
            (70, "Loading memory...",
             "[ OK ] memory loaded"),
            (80, "Starting security...",
             "[ OK ] security active"),
            (90, "Preparing login...",
             "[ OK ] login ready"),
            (100, "BrayoOS Ready!",
             "[ OK ] system ready"),
        ]

        for pct, status, log in steps:
            time.sleep(0.35)
            self.update(pct, status, log)
            if pct == 60:
                self.update_aria(
                    "🤖 ARIA: Waking up...")
            elif pct == 70:
                self.update_aria(
                    "🤖 ARIA: Memory loaded...")
            elif pct == 100:
                self.update_aria(
                    "🤖 ARIA: Ready, Brayo. 🇰🇪")

        time.sleep(1.5)
        self.root.destroy()

        # Launch login
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        subprocess.Popen([
            "python",
            os.path.expanduser(
                "~/BrayoOS/core/login.py")
        ], env=env)

if __name__ == "__main__":
    BootScreen()
