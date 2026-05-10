# BrayoOS — Built by Brayo & AIRA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import httpx
import threading

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class SocialOSINT:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Social OSINT")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔍 Social OSINT Tool",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Username:",
                bg=BG, fg=TEXT,
                font=("monospace", 11)).pack(side=tk.LEFT)

        self.username = tk.Entry(frame, bg=DARK,
                                fg=ACCENT,
                                font=("monospace", 11),
                                insertbackground=ACCENT)
        self.username.pack(side=tk.LEFT, fill=tk.X,
                          expand=True, padx=5)

        tk.Button(frame, text="🔍 Search",
                 bg=ACCENT, fg=BG,
                 command=self.search).pack(side=tk.LEFT)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def search(self):
        username = self.username.get().strip()
        if not username:
            return
        self.output.delete(1.0, tk.END)
        self.log(f"🔍 Searching for: {username}")
        self.log("═"*50)

        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "LinkedIn": f"https://linkedin.com/in/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "Telegram": f"https://t.me/{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "Snapchat": f"https://snapchat.com/add/{username}",
        }

        def run():
            with httpx.Client(
                follow_redirects=True,
                timeout=10) as client:
                for platform, url in platforms.items():
                    try:
                        r = client.get(url)
                        if r.status_code == 200:
                            self.log(
                                f"✅ FOUND: {platform}\n"
                                f"   {url}")
                        else:
                            self.log(
                                f"❌ {platform}: "
                                f"Not found ({r.status_code})")
                    except Exception as e:
                        self.log(f"⚠️ {platform}: Error")
            self.log("\n✅ Search complete!")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    SocialOSINT()
