# BrayoOS — Built by Brayo & AIRA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import httpx
import threading
import socket

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class IPTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌍 IP Tracker")
        self.root.configure(bg=BG)
        self.root.geometry("600x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🌍 IP Tracker",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        self.ip_entry = tk.Entry(frame, bg=DARK, fg=ACCENT,
                                font=("monospace", 12),
                                insertbackground=ACCENT)
        self.ip_entry.pack(side=tk.LEFT, fill=tk.X,
                          expand=True, padx=5)
        self.ip_entry.insert(0, "8.8.8.8")

        tk.Button(frame, text="🔍 Track",
                 bg=ACCENT, fg=BG,
                 command=self.track).pack(side=tk.LEFT)
        tk.Button(frame, text="📍 My IP",
                 bg=DARK, fg=TEXT,
                 command=self.my_ip).pack(side=tk.LEFT, padx=5)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 11))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        self.status = tk.Label(self.root, text="Ready",
                              bg=DARK, fg=TEXT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def track(self):
        ip = self.ip_entry.get().strip()
        self.output.delete(1.0, tk.END)
        self.status.config(text=f"Tracking {ip}...")
        def run():
            try:
                with httpx.Client() as client:
                    r = client.get(
                        f"http://ip-api.com/json/{ip}",
                        timeout=10)
                    data = r.json()
                    self.output.delete(1.0, tk.END)
                    self.output.insert(tk.END,
                        f"{'═'*50}\n"
                        f"🌍 IP Address : {data.get('query','N/A')}\n"
                        f"🏳️  Country    : {data.get('country','N/A')}\n"
                        f"🏙️  City       : {data.get('city','N/A')}\n"
                        f"📍 Region     : {data.get('regionName','N/A')}\n"
                        f"🌐 ISP        : {data.get('isp','N/A')}\n"
                        f"📡 Org        : {data.get('org','N/A')}\n"
                        f"🗺️  Lat/Lon    : {data.get('lat','N/A')}, "
                        f"{data.get('lon','N/A')}\n"
                        f"⏰ Timezone   : {data.get('timezone','N/A')}\n"
                        f"📮 ZIP        : {data.get('zip','N/A')}\n"
                        f"📱 Mobile     : {data.get('mobile','N/A')}\n"
                        f"🛡️  Proxy      : {data.get('proxy','N/A')}\n"
                        f"🖥️  Hosting    : {data.get('hosting','N/A')}\n"
                        f"{'═'*50}\n")
                    self.status.config(text="✅ Done!")
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}\n")
                self.status.config(text="❌ Error")
        threading.Thread(target=run).start()

    def my_ip(self):
        def run():
            try:
                with httpx.Client() as client:
                    r = client.get("http://ip-api.com/json/",
                                  timeout=10)
                    data = r.json()
                    self.ip_entry.delete(0, tk.END)
                    self.ip_entry.insert(0, data.get('query',''))
                    self.track()
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}\n")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    IPTracker()
