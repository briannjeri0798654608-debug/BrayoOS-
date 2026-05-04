import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os
import json
import threading

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

# BrayoOS App Store catalog
APPS = {
    "Security Tools": [
        {"name": "Nmap Scanner", "pkg": "nmap", "desc": "Network mapper"},
        {"name": "Metasploit", "pkg": "metasploit", "desc": "Penetration testing"},
        {"name": "Hydra", "pkg": "hydra", "desc": "Password cracker"},
        {"name": "SQLMap", "pkg": "sqlmap", "desc": "SQL injection tool"},
        {"name": "Aircrack", "pkg": "aircrack-ng", "desc": "WiFi security"},
        {"name": "John Ripper", "pkg": "john", "desc": "Password cracker"},
    ],
    "Development": [
        {"name": "Git", "pkg": "git", "desc": "Version control"},
        {"name": "NodeJS", "pkg": "nodejs", "desc": "JavaScript runtime"},
        {"name": "PHP", "pkg": "php", "desc": "PHP interpreter"},
        {"name": "Ruby", "pkg": "ruby", "desc": "Ruby language"},
        {"name": "Golang", "pkg": "golang", "desc": "Go language"},
        {"name": "Rust", "pkg": "rust", "desc": "Rust language"},
    ],
    "Network Tools": [
        {"name": "Wget", "pkg": "wget", "desc": "File downloader"},
        {"name": "Curl", "pkg": "curl", "desc": "URL tool"},
        {"name": "Netcat", "pkg": "netcat", "desc": "Network tool"},
        {"name": "Wireshark", "pkg": "tshark", "desc": "Packet analyzer"},
        {"name": "OpenSSH", "pkg": "openssh", "desc": "SSH client/server"},
        {"name": "Tor", "pkg": "tor", "desc": "Anonymous network"},
    ],
    "Utilities": [
        {"name": "FFmpeg", "pkg": "ffmpeg", "desc": "Media converter"},
        {"name": "ImageMagick", "pkg": "imagemagick", "desc": "Image editor"},
        {"name": "7-Zip", "pkg": "p7zip", "desc": "Archive manager"},
        {"name": "Tree", "pkg": "tree", "desc": "Directory viewer"},
        {"name": "Htop", "pkg": "htop", "desc": "Process viewer"},
        {"name": "Vim", "pkg": "vim", "desc": "Text editor"},
    ],
}

class AppStore:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📦 BrayoOS App Store")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📦 BrayoOS App Store",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        # Category tabs
        tab_frame = tk.Frame(self.root, bg=BG)
        tab_frame.pack(fill=tk.X, padx=10)

        for cat in APPS.keys():
            tk.Button(tab_frame, text=cat,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     command=lambda c=cat: self.show_category(c),
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=3)

        # Search
        search_frame = tk.Frame(self.root, bg=BG)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(search_frame, text="🔍",
                bg=BG, fg=ACCENT,
                font=("monospace", 12)).pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame,
                                    bg=DARK, fg=ACCENT,
                                    font=("monospace", 11),
                                    insertbackground=ACCENT)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search())

        tk.Button(search_frame, text="Search",
                 bg=ACCENT, fg=BG,
                 command=self.search).pack(side=tk.LEFT)

        # App list
        self.app_frame = tk.Frame(self.root, bg=BG)
        self.app_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Output log
        self.log = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 9), height=6)
        self.log.pack(fill=tk.X, padx=10, pady=5)

        # Show all apps
        self.show_category("Security Tools")

    def show_category(self, category):
        for widget in self.app_frame.winfo_children():
            widget.destroy()

        apps = APPS.get(category, [])
        for i, app in enumerate(apps):
            frame = tk.Frame(self.app_frame, bg=DARK,
                           relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=3)

            tk.Label(frame, text=app["name"],
                    bg=DARK, fg=ACCENT,
                    font=("monospace", 11, "bold"),
                    width=20).pack(side=tk.LEFT, padx=10)

            tk.Label(frame, text=app["desc"],
                    bg=DARK, fg=TEXT,
                    font=("monospace", 10)).pack(side=tk.LEFT)

            tk.Button(frame, text="📥 Install",
                     bg=ACCENT, fg=BG,
                     font=("monospace", 9),
                     command=lambda p=app["pkg"],
                     n=app["name"]: self.install(p, n)).pack(
                         side=tk.RIGHT, padx=5, pady=3)

            tk.Button(frame, text="🗑️ Remove",
                     bg="#330000", fg="red",
                     font=("monospace", 9),
                     command=lambda p=app["pkg"]: self.remove(p)).pack(
                         side=tk.RIGHT, padx=2, pady=3)

    def search(self):
        query = self.search_entry.get().lower()
        for widget in self.app_frame.winfo_children():
            widget.destroy()

        for cat, apps in APPS.items():
            for app in apps:
                if query in app["name"].lower() or \
                   query in app["desc"].lower():
                    frame = tk.Frame(self.app_frame,
                                   bg=DARK, relief=tk.RAISED, bd=1)
                    frame.pack(fill=tk.X, pady=2)

                    tk.Label(frame, text=app["name"],
                            bg=DARK, fg=ACCENT,
                            font=("monospace", 11, "bold"),
                            width=20).pack(side=tk.LEFT, padx=10)

                    tk.Label(frame, text=f"[{cat}] {app['desc']}",
                            bg=DARK, fg=TEXT,
                            font=("monospace", 10)).pack(side=tk.LEFT)

                    tk.Button(frame, text="📥 Install",
                             bg=ACCENT, fg=BG,
                             command=lambda p=app["pkg"],
                             n=app["name"]: self.install(p, n)).pack(
                                 side=tk.RIGHT, padx=5)

    def install(self, pkg, name):
        self.log.insert(tk.END, f"📥 Installing {name}...\n")
        self.log.see(tk.END)
        def run():
            result = subprocess.run(
                ["pkg", "install", "-y", pkg],
                capture_output=True, text=True)
            if result.returncode == 0:
                self.log.insert(tk.END, f"✅ {name} installed!\n")
            else:
                self.log.insert(tk.END,
                    f"❌ Failed: {result.stderr[:100]}\n")
            self.log.see(tk.END)
        threading.Thread(target=run).start()

    def remove(self, pkg):
        def run():
            result = subprocess.run(
                ["pkg", "remove", "-y", pkg],
                capture_output=True, text=True)
            self.log.insert(tk.END,
                f"🗑️ Removed {pkg}\n")
            self.log.see(tk.END)
        threading.Thread(target=run).start()

if __name__ == "__main__":
    AppStore()
