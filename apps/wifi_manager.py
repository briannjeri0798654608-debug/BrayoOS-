# BrayoOS — Built by Brayo & AIRA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import json

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class WiFiManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📡 WiFi Manager")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📡 WiFi Manager",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [
            ("📡 Scan", self.scan_wifi),
            ("📶 Status", self.wifi_status),
            ("🔑 Saved", self.saved_networks),
            ("📊 Speed Test", self.speed_test),
        ]:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 10),
                     command=cmd,
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=3)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def scan_wifi(self):
        self.output.delete(1.0, tk.END)
        self.log("📡 Scanning WiFi networks...")
        def run():
            try:
                result = subprocess.run(
                    ["termux-wifi-scaninfo"],
                    capture_output=True, text=True, timeout=15)
                networks = json.loads(result.stdout)
                self.output.delete(1.0, tk.END)
                for net in networks:
                    signal = net.get('rssi', 0)
                    bars = "▂▄▆█" if signal > -50 else \
                           "▂▄▆_" if signal > -70 else "▂▄__"
                    self.log(
                        f"📶 {net.get('ssid','Hidden')}\n"
                        f"   Signal: {bars} ({signal}dBm)\n"
                        f"   Security: {net.get('capabilities','')}\n"
                        f"   BSSID: {net.get('bssid','')}\n")
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

    def wifi_status(self):
        self.output.delete(1.0, tk.END)
        def run():
            try:
                result = subprocess.run(
                    ["termux-wifi-connectioninfo"],
                    capture_output=True, text=True, timeout=10)
                data = json.loads(result.stdout)
                self.log(
                    f"📶 WiFi Status\n"
                    f"{'═'*50}\n"
                    f"🔗 SSID: {data.get('ssid','')}\n"
                    f"📍 IP: {data.get('ip','')}\n"
                    f"📡 BSSID: {data.get('bssid','')}\n"
                    f"📶 Speed: {data.get('link_speed_mbps','')} Mbps\n"
                    f"🔋 Signal: {data.get('rssi','')} dBm\n")
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

    def saved_networks(self):
        self.output.delete(1.0, tk.END)
        self.log("Loading saved networks...")
        try:
            with open("/proc/net/arp") as f:
                self.log("📋 ARP Table:\n" + f.read())
        except Exception as e:
            self.log(f"Error: {e}")

    def speed_test(self):
        self.output.delete(1.0, tk.END)
        self.log("🚀 Testing internet speed...")
        def run():
            import httpx, time
            try:
                with httpx.Client() as client:
                    start = time.time()
                    r = client.get(
                        "https://speed.cloudflare.com/__down?bytes=10000000",
                        timeout=30)
                    elapsed = time.time() - start
                    size_mb = len(r.content) / 1024 / 1024
                    speed = size_mb / elapsed * 8
                    self.log(
                        f"📊 Speed Test Results\n"
                        f"{'═'*50}\n"
                        f"⬇️  Download: {speed:.1f} Mbps\n"
                        f"📦 Size: {size_mb:.1f} MB\n"
                        f"⏱️  Time: {elapsed:.1f}s\n")
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    WiFiManager()
