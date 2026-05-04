import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os
import time

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class BackupSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💾 Backup System")
        self.root.configure(bg=BG)
        self.root.geometry("600x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="💾 BrayoOS Backup",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        for text, cmd in [
            ("💾 Backup Now", self.backup),
            ("📦 Backup To SD", self.backup_sd),
            ("🔄 Restore", self.restore),
            ("📋 List Backups", self.list_backups),
        ]:
            tk.Button(self.root, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 11),
                     command=cmd,
                     relief=tk.FLAT,
                     width=20).pack(pady=5)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def backup(self):
        self.log("💾 Creating backup...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.expanduser(
            f"~/BrayoOS/backups/backup_{timestamp}.zip")
        os.makedirs(os.path.expanduser(
            "~/BrayoOS/backups"), exist_ok=True)
        result = subprocess.run([
            "zip", "-r", backup_file,
            os.path.expanduser("~/BrayoOS/")
        ], capture_output=True, text=True)
        if result.returncode == 0:
            self.log(f"✅ Backup saved: {backup_file}")
        else:
            self.log(f"❌ Error: {result.stderr}")

    def backup_sd(self):
        self.log("📦 Backing up to SD card...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = f"/sdcard/BrayoOS_backup_{timestamp}.zip"
        result = subprocess.run([
            "zip", "-r", backup_file,
            os.path.expanduser("~/BrayoOS/")
        ], capture_output=True, text=True)
        if result.returncode == 0:
            self.log(f"✅ Backup saved to SD: {backup_file}")
        else:
            self.log(f"❌ Error: {result.stderr}")

    def restore(self):
        self.log("🔄 Listing available backups...")
        self.list_backups()
        self.log("\nTo restore, run in terminal:")
        self.log("unzip ~/BrayoOS/backups/[backup_file] -d ~/")

    def list_backups(self):
        backup_dir = os.path.expanduser("~/BrayoOS/backups")
        os.makedirs(backup_dir, exist_ok=True)
        backups = os.listdir(backup_dir)
        if backups:
            self.log("📋 Available backups:")
            for b in backups:
                self.log(f"  📦 {b}")
        else:
            self.log("❌ No backups found!")

if __name__ == "__main__":
    BackupSystem()
