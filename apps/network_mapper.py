# BrayoOS — Built by Brayo & Virgy — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import socket
import ipaddress

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class NetworkMapper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🗺️ Network Mapper")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.scanning = False
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🗺️ Network Mapper",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Network:",
                bg=BG, fg=TEXT,
                font=("monospace", 11)).pack(side=tk.LEFT)

        self.network = tk.Entry(frame, bg=DARK,
                               fg=ACCENT,
                               font=("monospace", 11),
                               insertbackground=ACCENT)
        self.network.pack(side=tk.LEFT, fill=tk.X,
                         expand=True, padx=5)
        self.network.insert(0, "192.168.1.0/24")

        for text, cmd in [
            ("🗺️ Map", self.map_network),
            ("⏹ Stop", self.stop),
        ]:
            tk.Button(frame, text=text,
                     bg=ACCENT if text=="🗺️ Map" else DARK,
                     fg=BG if text=="🗺️ Map" else "red",
                     command=cmd).pack(side=tk.LEFT, padx=2)

        # Results tree
        result_frame = tk.Frame(self.root, bg=BG)
        result_frame.pack(fill=tk.BOTH, expand=True,
                         padx=10, pady=5)

        self.output = scrolledtext.ScrolledText(
            result_frame, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True)

        self.status = tk.Label(self.root,
                              text="Ready",
                              bg=DARK, fg=TEXT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def stop(self):
        self.scanning = False
        self.status.config(text="⏹ Stopped")

    def map_network(self):
        network = self.network.get().strip()
        self.output.delete(1.0, tk.END)
        self.scanning = True
        self.log(f"🗺️ Mapping network: {network}")
        self.log("═"*60)

        def run():
            try:
                net = ipaddress.IPv4Network(network,
                                           strict=False)
                hosts = list(net.hosts())
                self.log(f"📊 Total hosts: {len(hosts)}")
                self.log("━"*60)

                alive = 0
                for ip in hosts:
                    if not self.scanning:
                        break
                    ip_str = str(ip)
                    result = subprocess.run(
                        ["ping", "-c", "1",
                         "-W", "1", ip_str],
                        capture_output=True)

                    if result.returncode == 0:
                        alive += 1
                        # Try to get hostname
                        try:
                            hostname = socket.gethostbyaddr(
                                ip_str)[0]
                        except:
                            hostname = "Unknown"

                        # Quick port check
                        open_ports = []
                        for port in [22, 80, 443, 8080]:
                            s = socket.socket()
                            s.settimeout(0.5)
                            if s.connect_ex(
                                    (ip_str, port)) == 0:
                                open_ports.append(port)
                            s.close()

                        self.log(
                            f"✅ {ip_str}\n"
                            f"   Host: {hostname}\n"
                            f"   Ports: {open_ports}\n")

                self.log("━"*60)
                self.log(f"✅ Done! Found {alive} hosts")
                self.status.config(
                    text=f"✅ {alive} hosts found")
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    NetworkMapper()
