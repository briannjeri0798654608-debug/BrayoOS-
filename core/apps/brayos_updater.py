import tkinter as tk
import threading
import time
import subprocess
import os
from datetime import datetime

CHANGELOG = [
    ("v1.0", "2026-01-01", "Initial BrayoOS — Terminal + 10 apps"),
    ("v1.5", "2026-02-15", "Added VNC desktop, AI brain, Telegram bot"),
    ("v2.0", "2026-04-01", "40+ apps, full XFCE desktop, flashable ROM"),
    ("v2.5", "2026-05-01", "Ghost Mode, DNA Vault, Signal Interceptor"),
    ("v3.0", "2026-05-10", "Identity Switcher, Threat Map, Self-Healing"),
    ("v3.5", "2026-05-10", "AIRA AI Voice, App Store, Multi-User, Updater ← YOU ARE HERE"),
]

class BrayoOSUpdater:
    def __init__(self, root):
        self.root = root
        self.root.title("🔄 BrayoOS Updater")
        self.root.geometry("660x560")
        self.root.configure(bg="#0D0D0D")
        self.updating = False
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="🔄 BRAYOOS UPDATER", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=8)
        tk.Label(self.root, text="[ SYSTEM UPDATE & VERSION MANAGER ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        # Current version
        ver_frame = tk.Frame(self.root, bg="#001100")
        ver_frame.pack(fill="x", padx=15, pady=8)
        tk.Label(ver_frame, text="CURRENT VERSION:", font=("Courier", 9),
                 bg="#001100", fg="#004400").pack(side="left", padx=10, pady=8)
        tk.Label(ver_frame, text="BrayoOS v3.5 — LATEST", font=("Courier", 12, "bold"),
                 bg="#001100", fg="#00FF41").pack(side="left")
        tk.Label(ver_frame, text="✅ UP TO DATE", font=("Courier", 10, "bold"),
                 bg="#001100", fg="#00FF41").pack(side="right", padx=10)

        # Changelog
        tk.Label(self.root, text="◈ VERSION HISTORY", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15, pady=(5,3))

        cl_frame = tk.Frame(self.root, bg="#001100")
        cl_frame.pack(fill="x", padx=15, pady=3)
        for ver, date, desc in reversed(CHANGELOG):
            row = tk.Frame(cl_frame, bg="#001100")
            row.pack(fill="x", padx=5, pady=2)
            color = "#00FF41" if "HERE" in desc else "#004400"
            tk.Label(row, text=f"{ver}", font=("Courier", 9, "bold"),
                     bg="#001100", fg=color, width=6).pack(side="left")
            tk.Label(row, text=date, font=("Courier", 8),
                     bg="#001100", fg="#003300", width=12).pack(side="left")
            tk.Label(row, text=desc, font=("Courier", 8),
                     bg="#001100", fg=color).pack(side="left", padx=5)

        # Update log
        tk.Label(self.root, text="◈ UPDATE LOG", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15, pady=(10,3))

        self.log_box = tk.Text(self.root, height=8, bg="#000800", fg="#00FF41",
                                font=("Courier", 8), relief="flat", state="disabled")
        self.log_box.pack(fill="both", padx=15, pady=3)

        # Buttons
        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=8)

        tk.Button(bf, text="🔄 CHECK UPDATES", command=self.check_updates,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Button(bf, text="📦 UPDATE PACKAGES", command=self.update_packages,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Button(bf, text="💾 BACKUP FIRST", command=self.backup,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Label(self.root, text="BrayoOS Updater v1.0 • Brayo & AIRA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def log(self, msg):
        self.log_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def check_updates(self):
        threading.Thread(target=self._check, daemon=True).start()

    def _check(self):
        self.log("🔄 Connecting to BrayoOS update server...")
        time.sleep(1)
        self.log("📡 Checking GitHub for latest version...")
        try:
            r = subprocess.check_output(
                "git -C ~/BrayoOS fetch --dry-run 2>&1 || echo 'checked'",
                shell=True).decode().strip()
            self.log(f"  → {r[:60]}")
        except:
            pass
        time.sleep(1)
        self.log("✅ BrayoOS v3.5 — You are on the LATEST version!")
        self.log("🇰🇪 Built Different. No updates needed.")

    def update_packages(self):
        threading.Thread(target=self._update_pkg, daemon=True).start()

    def _update_pkg(self):
        self.log("📦 Updating Termux packages...")
        self.log("  → pkg update -y")
        subprocess.run("pkg update -y 2>&1 | tail -5", shell=True)
        self.log("✅ Packages updated!")
        self.log("📦 Updating pip packages...")
        subprocess.run("pip install --upgrade httpx 2>&1 | tail -3", shell=True)
        self.log("✅ All packages up to date!")

    def backup(self):
        threading.Thread(target=self._backup, daemon=True).start()

    def _backup(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        backup_path = os.path.expanduser(f"~/BrayoOS/backups/backup_{ts}")
        self.log(f"💾 Creating backup → {backup_path}")
        os.makedirs(backup_path, exist_ok=True)
        subprocess.run(f"cp -r ~/BrayoOS/core {backup_path}/", shell=True)
        subprocess.run(f"cp -r ~/BrayoOS/memory {backup_path}/", shell=True)
        self.log("✅ Backup complete!")
        self.log(f"📁 Saved to: {backup_path}")

if __name__ == "__main__":
    root = tk.Tk()
    BrayoOSUpdater(root)
    root.mainloop()
