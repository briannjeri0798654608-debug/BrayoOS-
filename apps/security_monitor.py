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

class SecurityMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔒 Security Monitor")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.monitoring = False
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔒 Security Monitor",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [
            ("▶ Start Monitor", self.start_monitor),
            ("⏹ Stop", self.stop_monitor),
            ("🔍 Check Ports", self.check_ports),
            ("👥 Active Users", self.active_users),
            ("📊 Network Stats", self.network_stats),
            ("🧹 Clear", lambda: self.output.delete(1.0, tk.END)),
        ]:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     command=cmd,
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        self.status = tk.Label(self.root,
                              text="● IDLE",
                              bg=DARK, fg="#FF0000",
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def log(self, msg):
        self.output.insert(tk.END,
            f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.output.see(tk.END)

    def start_monitor(self):
        self.monitoring = True
        self.status.config(text="● MONITORING", fg=ACCENT)
        self.log("🔒 Security monitoring started...")
        threading.Thread(target=self.monitor_loop).start()

    def stop_monitor(self):
        self.monitoring = False
        self.status.config(text="● IDLE", fg="#FF0000")
        self.log("⏹ Monitoring stopped")

    def monitor_loop(self):
        while self.monitoring:
            try:
                # Check new connections
                result = subprocess.run(
                    ["cat", "/proc/net/tcp"],
                    capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')
                active = len([l for l in lines if '0A' in l])
                self.log(f"🌐 Active connections: {active}")

                # Check CPU
                with open("/proc/loadavg") as f:
                    load = f.read().split()[0]
                self.log(f"⚡ CPU Load: {load}")

                # Check memory
                with open("/proc/meminfo") as f:
                    mem = f.readlines()
                total = int(mem[0].split()[1])
                free = int(mem[1].split()[1])
                used_pct = ((total-free)/total)*100
                self.log(f"💾 RAM Used: {used_pct:.1f}%")

                if float(load) > 2.0:
                    self.log("⚠️ HIGH CPU LOAD DETECTED!")
                if used_pct > 90:
                    self.log("⚠️ HIGH RAM USAGE!")

            except Exception as e:
                self.log(f"Error: {e}")
            time.sleep(5)

    def check_ports(self):
        self.output.delete(1.0, tk.END)
        self.log("🔍 Checking open ports...")
        def run():
            try:
                result = subprocess.run(
                    ["cat", "/proc/net/tcp"],
                    capture_output=True, text=True)
                self.log("Port Status:")
                self.log("═"*50)
                for line in result.stdout.split('\n')[1:10]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) > 1:
                            port = int(parts[1].split(':')[1], 16)
                            self.log(f"Port: {port}")
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

    def active_users(self):
        self.output.delete(1.0, tk.END)
        def run():
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True, text=True)
            self.log("👥 Active Processes:")
            self.log("═"*50)
            for line in result.stdout.split('\n')[:15]:
                self.log(line)
        threading.Thread(target=run).start()

    def network_stats(self):
        self.output.delete(1.0, tk.END)
        def run():
            try:
                with open("/proc/net/dev") as f:
                    self.log("📊 Network Stats:")
                    self.log("═"*50)
                    self.log(f.read())
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    SecurityMonitor()
