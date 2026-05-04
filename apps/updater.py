import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import httpx

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

CURRENT_VERSION = "2.0"

class Updater:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔄 BrayoOS Updater")
        self.root.configure(bg=BG)
        self.root.geometry("600x400")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔄 BrayoOS Updater",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        tk.Label(self.root,
                text=f"Current Version: {CURRENT_VERSION}",
                bg=BG, fg=TEXT,
                font=("monospace", 11)).pack()

        for text, cmd in [
            ("🔍 Check Updates", self.check_updates),
            ("📦 Update Packages", self.update_packages),
            ("🐍 Update Python Libs", self.update_python),
            ("⚡ Full System Update", self.full_update),
        ]:
            tk.Button(self.root, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 11),
                     command=cmd,
                     relief=tk.FLAT,
                     width=25).pack(pady=5)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def check_updates(self):
        self.log("🔍 Checking for updates...")
        self.log(f"✅ Current: BrayoOS v{CURRENT_VERSION}")
        self.log("📡 Checking Termux packages...")
        def run():
            result = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True, text=True)
            self.log(result.stdout or "✅ All up to date!")
        threading.Thread(target=run).start()

    def update_packages(self):
        self.log("📦 Updating packages...")
        def run():
            result = subprocess.run(
                ["pkg", "upgrade", "-y"],
                capture_output=True, text=True)
            self.log(result.stdout)
            self.log("✅ Packages updated!")
        threading.Thread(target=run).start()

    def update_python(self):
        self.log("🐍 Updating Python libraries...")
        def run():
            libs = ["httpx", "requests",
                   "flask", "pillow"]
            for lib in libs:
                result = subprocess.run(
                    ["pip", "install", "--upgrade",
                     lib, "--break-system-packages"],
                    capture_output=True, text=True)
                self.log(f"✅ {lib} updated")
        threading.Thread(target=run).start()

    def full_update(self):
        self.log("⚡ Starting full system update...")
        self.check_updates()
        self.root.after(2000, self.update_packages)
        self.root.after(5000, self.update_python)

if __name__ == "__main__":
    Updater()
