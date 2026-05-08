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
RED = "#FF4444"

class TaskManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📊 Task Manager")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.running = True
        self.build_ui()
        threading.Thread(
            target=self.auto_refresh,
            daemon=True).start()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root,
                text="📊 BrayoOS Task Manager",
                bg=BG, fg=ACCENT,
                font=("monospace", 16,
                      "bold")).pack(pady=10)

        # Stats bar
        self.stats_frame = tk.Frame(
            self.root, bg=DARK)
        self.stats_frame.pack(
            fill=tk.X, padx=10, pady=5)

        self.cpu_label = tk.Label(
            self.stats_frame,
            text="CPU: --",
            bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.cpu_label.pack(
            side=tk.LEFT, padx=15, pady=5)

        self.ram_label = tk.Label(
            self.stats_frame,
            text="RAM: --",
            bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.ram_label.pack(
            side=tk.LEFT, padx=15)

        self.storage_label = tk.Label(
            self.stats_frame,
            text="Storage: --",
            bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.storage_label.pack(
            side=tk.LEFT, padx=15)

        self.battery_label = tk.Label(
            self.stats_frame,
            text="🔋 --",
            bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.battery_label.pack(
            side=tk.RIGHT, padx=15)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [
            ("🔄 Refresh", self.refresh),
            ("💀 Kill", self.kill_selected),
            ("🔍 Search", self.search_process),
            ("📊 Sort CPU", self.sort_cpu),
            ("💾 Sort MEM", self.sort_mem),
        ]:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     command=cmd,
                     relief=tk.FLAT).pack(
                         side=tk.LEFT, padx=2,
                         pady=5)

        # Search bar
        search_frame = tk.Frame(self.root, bg=BG)
        search_frame.pack(fill=tk.X, padx=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg=DARK, fg=ACCENT,
            font=("monospace", 10),
            insertbackground=ACCENT)
        self.search_entry.pack(
            fill=tk.X, pady=3)
        self.search_var.trace(
            'w', lambda *a: self.refresh())

        # Process list
        self.process_list = tk.Listbox(
            self.root,
            bg=DARK, fg=TEXT,
            font=("monospace", 9),
            selectbackground=ACCENT,
            selectforeground=BG)
        self.process_list.pack(
            fill=tk.BOTH, expand=True,
            padx=10, pady=5)

        self.status = tk.Label(
            self.root, text="",
            bg=DARK, fg=ACCENT,
            font=("monospace", 9))
        self.status.pack(fill=tk.X)

        self.refresh()

    def refresh(self):
        query = self.search_var.get().lower()
        result = subprocess.run(
            ["ps", "aux", "--sort=-%cpu"],
            capture_output=True, text=True)

        self.process_list.delete(0, tk.END)
        lines = result.stdout.split('\n')

        # Header
        self.process_list.insert(
            tk.END,
            f"{'PID':<8}{'CPU%':<8}"
            f"{'MEM%':<8}{'NAME':<20}")
        self.process_list.insert(
            tk.END, "─"*60)

        count = 0
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 11:
                continue
            pid = parts[1]
            cpu = parts[2]
            mem = parts[3]
            name = parts[10].split('/')[-1][:20]

            if query and query not in \
               name.lower():
                continue

            display = (f"{pid:<8}{cpu:<8}"
                      f"{mem:<8}{name:<20}")
            self.process_list.insert(
                tk.END, display)
            count += 1

        self.status.config(
            text=f"Processes: {count}")
        self.update_stats()

    def update_stats(self):
        # CPU
        try:
            with open("/proc/loadavg") as f:
                load = f.read().split()[0]
            self.cpu_label.config(
                text=f"CPU: {load}")
        except:
            pass

        # RAM
        try:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            total = int(
                lines[0].split()[1]) // 1024
            free = int(
                lines[1].split()[1]) // 1024
            used = total - free
            pct = int(used/total*100)
            self.ram_label.config(
                text=f"RAM: {used}MB/{total}MB "
                     f"({pct}%)")
        except:
            pass

        # Storage
        try:
            result = subprocess.run(
                ["df", "-h", "/data"],
                capture_output=True, text=True)
            parts = result.stdout.split(
                '\n')[1].split()
            self.storage_label.config(
                text=f"💿 {parts[2]}/{parts[1]}")
        except:
            pass

    def kill_selected(self):
        selection = self.process_list.curselection()
        if not selection:
            return
        line = self.process_list.get(
            selection[0])
        pid = line.strip().split()[0]
        if pid.isdigit():
            subprocess.run(["kill", "-9", pid])
            self.status.config(
                text=f"💀 Killed PID {pid}")
            self.refresh()

    def search_process(self):
        self.search_entry.focus()

    def sort_cpu(self):
        self.refresh()

    def sort_mem(self):
        result = subprocess.run(
            ["ps", "aux", "--sort=-%mem"],
            capture_output=True, text=True)
        self.process_list.delete(0, tk.END)
        for line in result.stdout.split(
                '\n')[1:20]:
            if line.strip():
                self.process_list.insert(
                    tk.END, line[:80])

    def auto_refresh(self):
        while self.running:
            time.sleep(5)
            self.update_stats()

if __name__ == "__main__":
    TaskManager()
