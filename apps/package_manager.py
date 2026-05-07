import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import json
import os
import httpx

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

# BrayoOS Package Registry
PACKAGES = {
    "security": {
        "nmap": {
            "desc": "Network mapper",
            "install": "pkg install nmap -y",
            "category": "Security"
        },
        "hydra": {
            "desc": "Password cracker",
            "install": "pkg install hydra -y",
            "category": "Security"
        },
        "john": {
            "desc": "John the Ripper",
            "install": "pkg install john -y",
            "category": "Security"
        },
        "aircrack-ng": {
            "desc": "WiFi security",
            "install": "pkg install aircrack-ng -y",
            "category": "Security"
        },
        "sqlmap": {
            "desc": "SQL injection tool",
            "install": "pkg install sqlmap -y",
            "category": "Security"
        },
        "tor": {
            "desc": "Anonymous network",
            "install": "pkg install tor -y",
            "category": "Security"
        },
    },
    "development": {
        "nodejs": {
            "desc": "JavaScript runtime",
            "install": "pkg install nodejs -y",
            "category": "Dev"
        },
        "golang": {
            "desc": "Go language",
            "install": "pkg install golang -y",
            "category": "Dev"
        },
        "ruby": {
            "desc": "Ruby language",
            "install": "pkg install ruby -y",
            "category": "Dev"
        },
        "php": {
            "desc": "PHP language",
            "install": "pkg install php -y",
            "category": "Dev"
        },
        "rust": {
            "desc": "Rust language",
            "install": "pkg install rust -y",
            "category": "Dev"
        },
    },
    "utilities": {
        "ffmpeg": {
            "desc": "Media converter",
            "install": "pkg install ffmpeg -y",
            "category": "Utils"
        },
        "imagemagick": {
            "desc": "Image editor",
            "install": "pkg install imagemagick -y",
            "category": "Utils"
        },
        "vim": {
            "desc": "Text editor",
            "install": "pkg install vim -y",
            "category": "Utils"
        },
        "tmux": {
            "desc": "Terminal multiplexer",
            "install": "pkg install tmux -y",
            "category": "Utils"
        },
        "htop": {
            "desc": "Process viewer",
            "install": "pkg install htop -y",
            "category": "Utils"
        },
    },
    "python": {
        "scapy": {
            "desc": "Packet manipulation",
            "install": "pip install scapy --break-system-packages",
            "category": "Python"
        },
        "pwntools": {
            "desc": "CTF framework",
            "install": "pip install pwntools --break-system-packages",
            "category": "Python"
        },
        "impacket": {
            "desc": "Network protocols",
            "install": "pip install impacket --break-system-packages",
            "category": "Python"
        },
        "selenium": {
            "desc": "Web automation",
            "install": "pip install selenium --break-system-packages",
            "category": "Python"
        },
    }
}

class PackageManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📦 BrayoOS Package Manager")
        self.root.configure(bg=BG)
        self.root.geometry("900x600")
        self.installed = self.load_installed()
        self.build_ui()
        self.root.mainloop()

    def load_installed(self):
        path = os.path.expanduser(
            "~/BrayoOS/memory/installed.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return []

    def save_installed(self):
        path = os.path.expanduser(
            "~/BrayoOS/memory/installed.json")
        os.makedirs(os.path.dirname(path),
                   exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.installed, f)

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=DARK)
        header.pack(fill=tk.X)

        tk.Label(header,
                text="📦 BrayoOS Package Manager",
                bg=DARK, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(
                    side=tk.LEFT, padx=15, pady=10)

        tk.Label(header,
                text=f"Installed: {len(self.installed)}",
                bg=DARK, fg=TEXT,
                font=("monospace", 10)).pack(
                    side=tk.RIGHT, padx=15)

        # Search
        search_frame = tk.Frame(self.root, bg=BG)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(search_frame, text="🔍",
                bg=BG, fg=ACCENT,
                font=("monospace", 12)).pack(
                    side=tk.LEFT)

        self.search = tk.Entry(search_frame,
                              bg=DARK, fg=ACCENT,
                              font=("monospace", 11),
                              insertbackground=ACCENT)
        self.search.pack(side=tk.LEFT, fill=tk.X,
                        expand=True, padx=5)
        self.search.bind(
            "<Return>",
            lambda e: self.do_search())

        tk.Button(search_frame, text="Search",
                 bg=ACCENT, fg=BG,
                 command=self.do_search).pack(
                     side=tk.LEFT)

        # Category tabs
        tabs = tk.Frame(self.root, bg=BG)
        tabs.pack(fill=tk.X, padx=10, pady=3)

        for cat in ["All", "Security",
                    "Development", "Utilities",
                    "Python"]:
            tk.Button(tabs, text=cat,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     relief=tk.FLAT,
                     command=lambda c=cat:
                     self.show_category(c)).pack(
                         side=tk.LEFT, padx=2)

        # Main area
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill=tk.BOTH, expand=True,
                 padx=10, pady=5)

        # Package list
        self.pkg_frame = tk.Frame(main, bg=BG,
                                 width=500)
        self.pkg_frame.pack(side=tk.LEFT,
                           fill=tk.BOTH,
                           expand=True)

        # Output log
        self.output = scrolledtext.ScrolledText(
            main, bg=DARK, fg=ACCENT,
            font=("monospace", 9),
            width=35)
        self.output.pack(side=tk.RIGHT,
                        fill=tk.Y)

        self.log("📦 BrayoOS Package Manager Ready!")
        self.log("Select a category or search!")
        self.show_category("All")

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def show_category(self, category):
        for w in self.pkg_frame.winfo_children():
            w.destroy()

        all_pkgs = []
        for cat, pkgs in PACKAGES.items():
            if category == "All" or \
               cat.lower() == category.lower():
                for name, info in pkgs.items():
                    all_pkgs.append((name, info))

        for name, info in all_pkgs:
            self.create_pkg_row(name, info)

    def create_pkg_row(self, name, info):
        frame = tk.Frame(self.pkg_frame,
                        bg=DARK,
                        relief=tk.RAISED, bd=1)
        frame.pack(fill=tk.X, pady=2)

        # Info
        info_frame = tk.Frame(frame, bg=DARK)
        info_frame.pack(side=tk.LEFT,
                       fill=tk.X, expand=True,
                       padx=10, pady=8)

        tk.Label(info_frame, text=name,
                bg=DARK, fg=ACCENT,
                font=("monospace", 11,
                      "bold")).pack(anchor=tk.W)

        tk.Label(info_frame,
                text=info['desc'],
                bg=DARK, fg="#666666",
                font=("monospace", 9)).pack(
                    anchor=tk.W)

        tk.Label(info_frame,
                text=f"[{info['category']}]",
                bg=DARK, fg="#444444",
                font=("monospace", 8)).pack(
                    anchor=tk.W)

        # Buttons
        btn_frame = tk.Frame(frame, bg=DARK)
        btn_frame.pack(side=tk.RIGHT, padx=5)

        is_installed = name in self.installed

        if is_installed:
            tk.Label(btn_frame, text="✅",
                    bg=DARK, fg=ACCENT,
                    font=("monospace", 14)).pack(
                        side=tk.LEFT, padx=5)
            tk.Button(btn_frame,
                     text="🗑️ Remove",
                     bg="#330000", fg="red",
                     font=("monospace", 9),
                     relief=tk.FLAT,
                     command=lambda n=name,
                     i=info: self.remove(n, i)).pack(
                         side=tk.LEFT, padx=2,
                         pady=5)
        else:
            tk.Button(btn_frame,
                     text="📥 Install",
                     bg=ACCENT, fg=BG,
                     font=("monospace", 9),
                     relief=tk.FLAT,
                     command=lambda n=name,
                     i=info: self.install(n, i)).pack(
                         side=tk.LEFT, padx=5,
                         pady=5)

    def install(self, name, info):
        self.log(f"📥 Installing {name}...")
        def run():
            result = subprocess.run(
                info['install'],
                shell=True,
                capture_output=True,
                text=True)
            if result.returncode == 0:
                self.installed.append(name)
                self.save_installed()
                self.log(f"✅ {name} installed!")
                self.show_category("All")
            else:
                self.log(
                    f"❌ Failed: {result.stderr[:100]}")
        threading.Thread(target=run).start()

    def remove(self, name, info):
        pkg = info['install'].split()[2]
        self.log(f"🗑️ Removing {name}...")
        def run():
            cmd = f"pkg remove {pkg} -y"
            subprocess.run(cmd, shell=True)
            if name in self.installed:
                self.installed.remove(name)
                self.save_installed()
            self.log(f"✅ {name} removed!")
            self.show_category("All")
        threading.Thread(target=run).start()

    def do_search(self):
        query = self.search.get().lower()
        for w in self.pkg_frame.winfo_children():
            w.destroy()
        for cat, pkgs in PACKAGES.items():
            for name, info in pkgs.items():
                if query in name.lower() or \
                   query in info['desc'].lower():
                    self.create_pkg_row(name, info)

if __name__ == "__main__":
    PackageManager()
