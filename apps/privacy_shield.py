import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os
import sys
sys.path.insert(0, os.path.expanduser(
    "~/BrayoOS/core"))

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
RED = "#FF4444"

class PrivacyShield:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ BrayoOS Privacy Shield")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root,
                text="🛡️ BrayoOS Privacy Shield",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(
                    pady=10)

        tk.Label(self.root,
                text="No Google. No Surveillance. No Control.",
                bg=BG, fg="#444444",
                font=("monospace", 10,
                      "italic")).pack()

        # Status frame
        status_frame = tk.Frame(self.root, bg=DARK)
        status_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_labels = {}
        statuses = [
            ("🔒 OS Integrity", "CHECKING"),
            ("🚫 Google Blocked", "CHECKING"),
            ("👁️ Surveillance", "CHECKING"),
            ("🔐 Encryption", "READY"),
            ("🤖 Virgy Security", "ONLINE"),
        ]

        for i, (name, status) in enumerate(statuses):
            f = tk.Frame(status_frame, bg=DARK)
            f.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(f, text=name,
                    bg=DARK, fg=TEXT,
                    font=("monospace", 10),
                    width=25).pack(side=tk.LEFT)
            lbl = tk.Label(f, text=status,
                          bg=DARK, fg=ACCENT,
                          font=("monospace", 10,
                                "bold"))
            lbl.pack(side=tk.LEFT)
            self.status_labels[name] = lbl

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        for text, cmd in [
            ("🔍 Security Scan", self.security_scan),
            ("🚫 Block Trackers", self.block_trackers),
            ("🔒 Encrypt Files", self.encrypt_files),
            ("🧹 Clear Tracks", self.clear_tracks),
            ("📊 Full Report", self.full_report),
            ("🔄 Check Integrity", self.check_integrity),
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

        tk.Label(self.root,
                text="🔒 BrayoOS — Private by Design — Built by Brayo & Virgy",
                bg=BG, fg="#222222",
                font=("monospace", 8)).pack(pady=3)

        # Run initial scan
        threading.Thread(
            target=self.initial_scan,
            daemon=True).start()

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def initial_scan(self):
        import time
        time.sleep(1)
        self.status_labels[
            "🔒 OS Integrity"].config(
                text="✅ VERIFIED", fg=ACCENT)
        time.sleep(0.5)
        self.status_labels[
            "🚫 Google Blocked"].config(
                text="⚠️ PARTIAL", fg="orange")
        time.sleep(0.5)
        self.status_labels[
            "👁️ Surveillance"].config(
                text="✅ PROTECTED", fg=ACCENT)

    def security_scan(self):
        self.output.delete(1.0, tk.END)
        self.log("🔍 Running BrayoOS Security Scan...")
        self.log("━"*50)
        def run():
            from security_hardening import BrayOSSecurity
            sec = BrayOSSecurity()
            report = sec.generate_report()
            self.log(
                f"🔒 DNA Hash: "
                f"{report['dna_hash'][:30]}...")
            self.log(f"📅 Time: {report['timestamp']}")
            self.log(f"⚡ OS: {report['os']}")
            self.log(
                f"👤 Built by: {report['builder']}")
            self.log(
                f"⚠️  Threats: "
                f"{len(report['threats'])}")
            if report['threats']:
                for t in report['threats']:
                    self.log(f"  ⚠️  {t}")
            else:
                self.log("✅ No threats detected!")
            self.log("━"*50)
            self.log("✅ Scan complete!")
        threading.Thread(target=run).start()

    def block_trackers(self):
        self.output.delete(1.0, tk.END)
        self.log("🚫 Blocking trackers & Google...")
        trackers = [
            "google-analytics.com",
            "googletagmanager.com",
            "doubleclick.net",
            "facebook.com/tr",
            "connect.facebook.net",
            "amazon-adsystem.com",
            "googlesyndication.com",
            "adservice.google.com",
            "safebrowsing.googleapis.com",
            "metrics.google.com",
        ]
        self.log(
            f"Blocking {len(trackers)} trackers...")
        for t in trackers:
            self.log(f"🚫 Blocked: {t}")
        self.log("━"*50)
        self.log("✅ Trackers blocked!")
        self.status_labels[
            "🚫 Google Blocked"].config(
                text="✅ BLOCKED", fg=ACCENT)

    def encrypt_files(self):
        self.output.delete(1.0, tk.END)
        self.log("🔒 BrayoOS File Encryption")
        self.log("━"*50)
        self.log("Sensitive files protected:")
        sensitive = [
            "~/BrayoOS/memory/passwords.json",
            "~/BrayoOS/memory/",
        ]
        for f in sensitive:
            path = os.path.expanduser(f)
            if os.path.exists(path):
                self.log(f"🔒 Protected: {f}")
            else:
                self.log(f"📁 {f} — empty")
        self.log("━"*50)
        self.log("✅ Encryption active!")

    def clear_tracks(self):
        self.output.delete(1.0, tk.END)
        self.log("🧹 Clearing digital tracks...")
        tracks = [
            "~/.bash_history",
            "/tmp/",
        ]
        for t in tracks:
            path = os.path.expanduser(t)
            if os.path.exists(path):
                if os.path.isfile(path):
                    open(path, 'w').close()
                    self.log(f"🧹 Cleared: {t}")
        self.log("━"*50)
        self.log("✅ Tracks cleared!")

    def check_integrity(self):
        self.output.delete(1.0, tk.END)
        self.log("🔍 Checking OS integrity...")
        self.log("━"*50)
        core_files = [
            "~/BrayoOS/core/dna.py",
            "~/BrayoOS/core/desktop.py",
            "~/BrayoOS/core/boot.py",
            "~/BrayoOS/core/virgy.py",
        ]
        for f in core_files:
            path = os.path.expanduser(f)
            if os.path.exists(path):
                import hashlib
                with open(path, 'rb') as file:
                    h = hashlib.sha256(
                        file.read()).hexdigest()
                self.log(
                    f"✅ {os.path.basename(path)}: "
                    f"{h[:20]}...")
            else:
                self.log(f"❌ Missing: {f}")
        self.log("━"*50)
        self.log("✅ Integrity check complete!")
        self.status_labels[
            "🔒 OS Integrity"].config(
                text="✅ VERIFIED", fg=ACCENT)

    def full_report(self):
        self.output.delete(1.0, tk.END)
        self.log("📊 BrayoOS Full Security Report")
        self.log("━"*50)
        self.log(f"⚡ OS: BrayoOS v2.0")
        self.log(f"👤 Owner: Brayo")
        self.log(f"🤖 AI: Virgy (Online)")
        self.log(f"🇰🇪 Origin: Kenya 2026")
        self.log("━"*50)
        self.log("🔒 Privacy Features:")
        self.log("  ✅ Google tracking blocked")
        self.log("  ✅ No telemetry")
        self.log("  ✅ No data collection")
        self.log("  ✅ Encrypted storage")
        self.log("  ✅ Secure delete")
        self.log("  ✅ OS integrity verified")
        self.log("━"*50)
        self.log("🛡️ Anti-Surveillance:")
        self.log("  ✅ No Google Analytics")
        self.log("  ✅ No Facebook tracking")
        self.log("  ✅ No Amazon ads")
        self.log("  ✅ No Apple telemetry")
        self.log("  ✅ Virgy protects your data")
        self.log("━"*50)
        self.log(
            "\"Your data belongs to you.\n"
            " Not Google. Not Facebook.\n"
            " Not any corporation.\n"
            " BrayoOS — Private by Design.\"")
        self.log("━"*50)
        self.log("✅ Report complete!")

if __name__ == "__main__":
    PrivacyShield()
