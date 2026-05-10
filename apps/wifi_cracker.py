# BrayoOS — Built by Brayo & AIRA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class WiFiCracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📡 WiFi Analyzer")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📡 WiFi Analyzer",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [
            ("📡 Scan Networks", self.scan),
            ("📊 Signal Strength", self.signal),
            ("🔑 Saved Passwords", self.saved_pass),
            ("📋 ARP Table", self.arp),
            ("🌐 Gateway Info", self.gateway),
        ]:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     command=cmd,
                     relief=tk.FLAT).pack(
                         side=tk.LEFT, padx=2)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def scan(self):
        self.output.delete(1.0, tk.END)
        self.log("📡 Scanning WiFi networks...")
        def run():
            try:
                result = subprocess.run(
                    ["termux-wifi-scaninfo"],
                    capture_output=True,
                    text=True, timeout=15)
                import json
                networks = json.loads(result.stdout)
                for net in networks:
                    signal = net.get('rssi', 0)
                    self.log(
                        f"📶 {net.get('ssid','Hidden')}\n"
                        f"   BSSID: {net.get('bssid','')}\n"
                        f"   Signal: {signal}dBm\n"
                        f"   Security: {net.get('capabilities','')}\n")
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

    def signal(self):
        self.output.delete(1.0, tk.END)
        def run():
            try:
                result = subprocess.run(
                    ["termux-wifi-connectioninfo"],
                    capture_output=True,
                    text=True, timeout=10)
                import json
                data = json.loads(result.stdout)
                rssi = data.get('rssi', 0)
                if rssi > -50:
                    quality = "Excellent 🟢"
                elif rssi > -70:
                    quality = "Good 🟡"
                else:
                    quality = "Poor 🔴"
                self.log(
                    f"📶 Signal: {rssi}dBm\n"
                    f"Quality: {quality}\n"
                    f"SSID: {data.get('ssid','')}\n"
                    f"Speed: {data.get('link_speed_mbps','')}Mbps\n"
                    f"IP: {data.get('ip','')}\n")
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=run).start()

    def saved_pass(self):
        self.output.delete(1.0, tk.END)
        self.log("🔑 Checking saved passwords...")
        paths = [
            "/data/misc/wifi/WifiConfigStore.xml",
            "/data/misc/wifi/wpa_supplicant.conf",
        ]
        found = False
        for path in paths:
            if os.path.exists(path):
                with open(path) as f:
                    self.log(f.read())
                found = True
        if not found:
            self.log("❌ Need root access for saved passwords!\n"
                    "Try rooting device first with Magisk.")

    def arp(self):
        self.output.delete(1.0, tk.END)
        self.log("📋 ARP Table:")
        try:
            with open("/proc/net/arp") as f:
                self.log(f.read())
        except Exception as e:
            self.log(f"Error: {e}")

    def gateway(self):
        self.output.delete(1.0, tk.END)
        def run():
            result = subprocess.run(
                ["ip", "route"],
                capture_output=True, text=True)
            self.log("🌐 Network Routes:")
            self.log(result.stdout)
        threading.Thread(target=run).start()

if __name__ == "__main__":
    WiFiCracker()
