# BrayoOS — Built by Brayo & ARIA — Kenya 2026
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

class ProcessMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Process Monitor")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.monitoring = False
        self.known_processes = set()
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔍 Process Monitor",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [
            ("▶ Monitor", self.start),
            ("⏹ Stop", self.stop),
            ("📋 All Procs", self.show_all),
            ("🔍 Find Malware", self.find_malware),
            ("💀 Kill Process", self.kill_process),
            ("🧹 Clear", lambda: self.output.delete(1.0, tk.END)),
        ]:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     command=cmd,
                     relief=tk.FLAT).pack(
                         side=tk.LEFT, padx=2)

        # Process filter
        filter_frame = tk.Frame(self.root, bg=BG)
        filter_frame.pack(fill=tk.X, padx=10, pady=3)

        tk.Label(filter_frame, text="Filter:",
                bg=BG, fg=TEXT,
                font=("monospace", 10)).pack(side=tk.LEFT)

        self.filter = tk.Entry(filter_frame,
                              bg=DARK, fg=ACCENT,
                              font=("monospace", 10),
                              insertbackground=ACCENT)
        self.filter.pack(side=tk.LEFT, fill=tk.X,
                        expand=True, padx=5)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 9))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        self.status = tk.Label(self.root,
                              text="● IDLE",
                              bg=DARK, fg="red",
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def start(self):
        self.monitoring = True
        self.status.config(
            text="● MONITORING", fg=ACCENT)
        self.log("🔍 Monitoring for new processes...")
        threading.Thread(
            target=self.monitor_loop).start()

    def stop(self):
        self.monitoring = False
        self.status.config(text="● IDLE", fg="red")

    def monitor_loop(self):
        # Get initial process list
        result = subprocess.run(
            ["ps", "-e", "-o", "pid,name"],
            capture_output=True, text=True)
        for line in result.stdout.split('\n')[1:]:
            if line.strip():
                self.known_processes.add(
                    line.strip().split()[0])

        while self.monitoring:
            result = subprocess.run(
                ["ps", "-e", "-o", "pid,name,%cpu,%mem"],
                capture_output=True, text=True)

            for line in result.stdout.split('\n')[1:]:
                if not line.strip():
                    continue
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                pid = parts[0]
                name = parts[1]

                if pid not in self.known_processes:
                    self.known_processes.add(pid)
                    self.log(
                        f"🆕 New process: {name} "
                        f"(PID:{pid})")

                    # Check suspicious
                    suspicious = [
                        "keylog", "spy", "hack",
                        "sniff", "capture", "record"
                    ]
                    if any(s in name.lower()
                           for s in suspicious):
                        self.log(
                            f"⚠️  SUSPICIOUS: {name}!")
            time.sleep(2)

    def show_all(self):
        self.output.delete(1.0, tk.END)
        filt = self.filter.get().lower()
        result = subprocess.run(
            ["ps", "-e", "-o",
             "pid,name,%cpu,%mem,stat"],
            capture_output=True, text=True)
        self.log("📋 Running Processes:")
        self.log("━"*60)
        for line in result.stdout.split('\n'):
            if filt and filt not in line.lower():
                continue
            self.log(line)

    def find_malware(self):
        self.output.delete(1.0, tk.END)
        self.log("🔍 Scanning for malware...")
        suspicious = [
            "keylog", "spy", "rat", "backdoor",
            "trojan", "virus", "malware", "hack",
            "sniff", "capture", "steal", "inject"
        ]
        result = subprocess.run(
            ["ps", "-e", "-o", "pid,name,cmd"],
            capture_output=True, text=True)
        found = 0
        for line in result.stdout.split('\n'):
            if any(s in line.lower()
                   for s in suspicious):
                self.log(f"⚠️  SUSPICIOUS: {line}")
                found += 1
        if found == 0:
            self.log("✅ No malware detected!")
        else:
            self.log(f"⚠️  Found {found} suspicious processes!")

    def kill_process(self):
        pid = self.filter.get().strip()
        if pid.isdigit():
            subprocess.run(["kill", "-9", pid])
            self.log(f"💀 Killed process {pid}")
        else:
            self.log("Enter PID in filter to kill!")

if __name__ == "__main__":
    ProcessMonitor()
