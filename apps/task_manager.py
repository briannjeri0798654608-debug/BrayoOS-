import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import time

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class TaskManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📊 Task Manager")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.refresh()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root,
                text="📊 BrayoOS Task Manager",
                bg=BG, fg=ACCENT,
                font=("monospace", 14, "bold")).pack(pady=10)

        self.stats = tk.Label(self.root,
                text="Loading...",
                bg=DARK, fg=ACCENT,
                font=("monospace", 10))
        self.stats.pack(fill=tk.X, padx=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        for text, cmd in [
            ("🔄 Refresh", self.refresh),
            ("💀 Kill", self.kill),
        ]:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 10),
                     command=cmd,
                     relief=tk.FLAT).pack(
                         side=tk.LEFT, padx=3)

        self.listbox = tk.Listbox(
            self.root, bg=DARK, fg=TEXT,
            font=("monospace", 9),
            selectbackground=ACCENT)
        self.listbox.pack(fill=tk.BOTH,
                         expand=True,
                         padx=10, pady=5)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True, text=True)
        for line in result.stdout.split('\n')[:30]:
            if line.strip():
                self.listbox.insert(tk.END, line[:80])
        try:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            total = int(lines[0].split()[1])//1024
            free = int(lines[1].split()[1])//1024
            used = total - free
            self.stats.config(
                text=f"RAM: {used}MB/{total}MB | "
                     f"Processes: {self.listbox.size()}")
        except:
            pass

    def kill(self):
        sel = self.listbox.get(tk.ACTIVE)
        if sel:
            parts = sel.split()
            if len(parts) > 1 and parts[1].isdigit():
                subprocess.run(["kill", "-9", parts[1]])
                self.refresh()

if __name__ == "__main__":
    TaskManager()
