# BrayoOS — Built by Brayo & AIRA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import time
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class SystemMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📊 System Monitor")
        self.root.configure(bg=BG)
        self.root.geometry("700x600")
        self.build_ui()
        self.update_loop()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📊 System Monitor",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [
            ("🔄 Refresh", self.refresh),
            ("📈 Processes", self.show_processes),
            ("💾 Memory", self.show_memory),
            ("💿 Storage", self.show_storage),
            ("⚡ Power", self.show_power)
        ]:
            tk.Button(btn_frame, text=text, bg=DARK,
                     fg=ACCENT, font=("monospace", 10),
                     command=cmd, relief=tk.FLAT).pack(
                         side=tk.LEFT, padx=3)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10), wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        self.status = tk.Label(self.root, text="Ready",
                              bg=DARK, fg=TEXT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def refresh(self):
        self.output.delete(1.0, tk.END)
        self.show_memory()
        self.show_storage()

    def show_memory(self):
        self.output.delete(1.0, tk.END)
        self.log("💾 MEMORY INFO:")
        self.log("═" * 50)
        try:
            with open("/proc/meminfo") as f:
                for line in f.readlines()[:10]:
                    self.log(line.strip())
        except:
            self.log("Error reading memory info")

    def show_storage(self):
        self.log("\n" + "═" * 50)
        self.log("💿 STORAGE INFO:")
        self.log("═" * 50)
        try:
            result = subprocess.run(
                ["df", "-h"],
                capture_output=True, text=True)
            self.log(result.stdout)
        except:
            self.log("Error reading storage")

    def show_processes(self):
        self.output.delete(1.0, tk.END)
        self.log("📈 TOP PROCESSES:")
        self.log("═" * 50)
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True, text=True)
            lines = result.stdout.split('\n')[:15]
            for line in lines:
                self.log(line)
        except:
            self.log("Error reading processes")

    def show_power(self):
        self.output.delete(1.0, tk.END)
        self.log("⚡ POWER INFO:")
        self.log("═" * 50)
        try:
            result = subprocess.run(
                ["termux-battery-status"],
                capture_output=True, text=True, timeout=5)
            self.log(result.stdout)
        except:
            self.log("Battery info not available on this system")

    def update_loop(self):
        self.status.config(
            text=f"Updated: {time.strftime('%H:%M:%S')}")
        self.root.after(1000, self.update_loop)

if __name__ == "__main__":
    SystemMonitor()
