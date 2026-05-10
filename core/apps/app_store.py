import tkinter as tk
from tkinter import messagebox
import threading
import time
import subprocess
import os
from datetime import datetime

APPS_AVAILABLE = [
    {"name": "🌐 Tor Browser", "desc": "Anonymous browsing", "size": "2.1MB", "cat": "Privacy", "installed": False},
    {"name": "📡 NetHunter", "desc": "Mobile pentest suite", "size": "4.5MB", "cat": "Security", "installed": False},
    {"name": "🔑 PassVault", "desc": "Password manager", "size": "0.8MB", "cat": "Security", "installed": False},
    {"name": "📊 SysMonitor", "desc": "Advanced system stats", "size": "1.2MB", "cat": "System", "installed": False},
    {"name": "🎵 BeatMaker", "desc": "Music production tool", "size": "3.3MB", "cat": "Media", "installed": False},
    {"name": "🗺️ OfflineMaps", "desc": "Maps without internet", "size": "8.0MB", "cat": "Tools", "installed": False},
    {"name": "💬 CryptoChat", "desc": "Encrypted messaging", "size": "1.5MB", "cat": "Privacy", "installed": False},
    {"name": "🧪 CodeLab", "desc": "Multi-language IDE", "size": "2.8MB", "cat": "Dev", "installed": False},
    {"name": "🔍 LogAnalyzer", "desc": "System log parser", "size": "0.9MB", "cat": "System", "installed": False},
    {"name": "🛡️ FirewallPro", "desc": "Advanced firewall UI", "size": "1.1MB", "cat": "Security", "installed": False},
    {"name": "📷 StegoCam", "desc": "Hide data in images", "size": "1.7MB", "cat": "Privacy", "installed": False},
    {"name": "⚙️ KernelTuner", "desc": "Kernel parameter editor", "size": "0.6MB", "cat": "System", "installed": False},
]

class AppStore:
    def __init__(self, root):
        self.root = root
        self.root.title("🏪 BrayoOS App Store")
        self.root.geometry("700x580")
        self.root.configure(bg="#0D0D0D")
        self.installed = []
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="🏪 BRAYOOS APP STORE", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=8)
        tk.Label(self.root, text="[ POWERED BY AIRA — BUILT DIFFERENT 🇰🇪 ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        # Search bar
        sf = tk.Frame(self.root, bg="#0D0D0D")
        sf.pack(fill="x", padx=15, pady=8)
        tk.Label(sf, text="🔍", font=("Courier", 12), bg="#0D0D0D", fg="#00FF41").pack(side="left")
        self.search = tk.Entry(sf, font=("Courier", 11), bg="#001100", fg="#00FF41",
                                insertbackground="#00FF41", relief="flat")
        self.search.pack(side="left", fill="x", expand=True, ipady=6, padx=5)
        self.search.bind("<KeyRelease>", self.filter_apps)

        # Stats
        statsf = tk.Frame(self.root, bg="#0D0D0D")
        statsf.pack(fill="x", padx=15, pady=3)
        self.stats_lbl = tk.Label(statsf,
                                   text=f"📦 {len(APPS_AVAILABLE)} apps available  |  ✅ 0 installed",
                                   font=("Courier", 9), bg="#0D0D0D", fg="#004400")
        self.stats_lbl.pack(side="left")

        # App list
        list_frame = tk.Frame(self.root, bg="#0D0D0D")
        list_frame.pack(fill="both", expand=True, padx=15, pady=3)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.app_list = tk.Canvas(list_frame, bg="#000800",
                                   yscrollcommand=scrollbar.set,
                                   highlightthickness=0)
        self.app_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.app_list.yview)

        self.cards_frame = tk.Frame(self.app_list, bg="#000800")
        self.app_list.create_window((0,0), window=self.cards_frame, anchor="nw")
        self.cards_frame.bind("<Configure>",
                               lambda e: self.app_list.configure(
                                   scrollregion=self.app_list.bbox("all")))

        self.render_apps(APPS_AVAILABLE)

        # Log
        self.log_box = tk.Text(self.root, height=4, bg="#000500", fg="#00FF41",
                                font=("Courier", 8), relief="flat", state="disabled")
        self.log_box.pack(fill="x", padx=15, pady=3)

        tk.Label(self.root, text="BrayoOS App Store v1.0 • Brayo & AIRA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def render_apps(self, apps):
        for w in self.cards_frame.winfo_children():
            w.destroy()
        for app in apps:
            self.make_card(app)

    def make_card(self, app):
        card = tk.Frame(self.cards_frame, bg="#001100", relief="flat")
        card.pack(fill="x", padx=5, pady=3)

        tk.Label(card, text=app["name"], font=("Courier", 11, "bold"),
                 bg="#001100", fg="#00FF41").pack(side="left", padx=10, pady=8)
        tk.Label(card, text=app["desc"], font=("Courier", 8),
                 bg="#001100", fg="#004400").pack(side="left")
        tk.Label(card, text=f"[{app['cat']}]", font=("Courier", 8),
                 bg="#001100", fg="#003300").pack(side="left", padx=5)
        tk.Label(card, text=app["size"], font=("Courier", 8),
                 bg="#001100", fg="#003300").pack(side="left")

        status = "✅ Installed" if app["installed"] else "⬇ Install"
        color = "#FF6600" if app["installed"] else "#00FF41"
        tk.Button(card, text=status, font=("Courier", 9, "bold"),
                  bg="#002200", fg=color, relief="flat", padx=8, pady=4,
                  command=lambda a=app: self.install(a)).pack(side="right", padx=10, pady=5)

    def install(self, app):
        if app["installed"]:
            messagebox.showinfo("Already Installed", f"{app['name']} is already installed!")
            return
        threading.Thread(target=self._install_anim, args=(app,), daemon=True).start()

    def _install_anim(self, app):
        self.log(f"⬇ Installing {app['name']}...")
        for i in range(0, 101, 10):
            self.log(f"  Progress: {'█' * (i//10)}{'░' * (10-i//10)} {i}%")
            time.sleep(0.2)
        app["installed"] = True
        self.installed.append(app["name"])
        self.log(f"✅ {app['name']} installed successfully!")
        self.root.after(0, self.render_apps, APPS_AVAILABLE)
        self.root.after(0, self.stats_lbl.config,
                        {"text": f"📦 {len(APPS_AVAILABLE)} apps  |  ✅ {len(self.installed)} installed"})

    def filter_apps(self, event=None):
        query = self.search.get().lower()
        filtered = [a for a in APPS_AVAILABLE
                    if query in a["name"].lower() or query in a["desc"].lower()]
        self.render_apps(filtered)

    def log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"{msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    AppStore(root)
    root.mainloop()
