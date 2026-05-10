# BrayoOS — Built by Brayo & Virgy — Kenya 2026
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

class SubdomainScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌐 Subdomain Scanner")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.scanning = False
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🌐 Subdomain Scanner",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Domain:",
                bg=BG, fg=TEXT,
                font=("monospace", 11)).pack(side=tk.LEFT)

        self.domain = tk.Entry(frame, bg=DARK, fg=ACCENT,
                              font=("monospace", 11),
                              insertbackground=ACCENT)
        self.domain.pack(side=tk.LEFT, fill=tk.X,
                        expand=True, padx=5)
        self.domain.insert(0, "example.com")

        tk.Button(frame, text="🔍 Scan",
                 bg=ACCENT, fg=BG,
                 command=self.scan).pack(side=tk.LEFT)
        tk.Button(frame, text="⏹ Stop",
                 bg=DARK, fg="red",
                 command=self.stop).pack(side=tk.LEFT, padx=3)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        self.status = tk.Label(self.root, text="Ready",
                              bg=DARK, fg=TEXT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def stop(self):
        self.scanning = False
        self.status.config(text="⏹ Stopped")

    def scan(self):
        domain = self.domain.get().strip()
        self.output.delete(1.0, tk.END)
        self.scanning = True
        self.log(f"🌐 Scanning subdomains for {domain}...")
        self.log("═"*50)

        subdomains = [
            "www", "mail", "ftp", "admin", "blog",
            "dev", "test", "staging", "api", "app",
            "shop", "store", "portal", "dashboard",
            "vpn", "remote", "server", "ns1", "ns2",
            "smtp", "pop", "imap", "webmail", "cpanel",
            "login", "secure", "beta", "old", "new",
            "m", "mobile", "cdn", "static", "media",
            "images", "img", "video", "download", "upload",
        ]

        def run():
            found = 0
            for sub in subdomains:
                if not self.scanning:
                    break
                target = f"{sub}.{domain}"
                try:
                    ip = socket.gethostbyname(target)
                    self.log(f"✅ FOUND: {target} → {ip}")
                    found += 1
                except:
                    pass
            self.log(f"\n{'═'*50}")
            self.log(f"✅ Scan complete! Found {found} subdomains")
            self.status.config(text=f"Done! {found} found")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    SubdomainScanner()
