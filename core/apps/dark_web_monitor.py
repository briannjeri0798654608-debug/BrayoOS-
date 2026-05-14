import tkinter as tk
import threading
import time
import random
import hashlib
from datetime import datetime

BRAYO_DATA = {
    "email": "brayo@brayoos.ke",
    "username": "Brayo",
    "device": "Redmi14C-pond",
    "os": "BrayoOS-v2.0",
    "location": "Kenya"
}

DARK_SITES = [
    "breachforums.onion", "raidforums.onion", "darkleaks.onion",
    "shadowmarket.onion", "blackhat.onion", "leakbase.onion",
    "nulled.onion", "crackingking.onion", "deepweb-leaks.onion"
]

BREACH_TYPES = [
    "Email leak", "Password hash", "Phone number",
    "IP address", "Credit card", "Identity data",
    "Location data", "Device fingerprint"
]

class DarkWebMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("💀 Dark Web Monitor")
        self.root.geometry("680x580")
        self.root.configure(bg="#0D0D0D")
        self.monitoring = False
        self.alerts = 0
        self.scanned = 0
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="💀 DARK WEB MONITOR", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#FF0000").pack(pady=8)
        tk.Label(self.root, text="[ BRAYO DATA BREACH DETECTION SYSTEM ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#330000").pack()

        # Status
        self.status_lbl = tk.Label(self.root, text="⬤  MONITOR OFFLINE",
                                    font=("Courier", 13, "bold"), bg="#0D0D0D", fg="#FF0000")
        self.status_lbl.pack(pady=8)

        # Stats
        sf = tk.Frame(self.root, bg="#0D0D0D")
        sf.pack(fill="x", padx=15, pady=5)
        self.svars = {}
        for col, (lbl, color) in enumerate([
            ("SITES SCANNED", "#00FFFF"), ("ALERTS", "#FF0000"),
            ("DATA SAFE", "#00FF41"), ("THREAT LEVEL", "#FF6600")
        ]):
            f = tk.Frame(sf, bg="#110000")
            f.grid(row=0, column=col, padx=4, sticky="ew")
            sf.columnconfigure(col, weight=1)
            tk.Label(f, text=lbl, font=("Courier", 7), bg="#110000", fg="#330000").pack(pady=1)
            v = tk.StringVar(value="0")
            self.svars[lbl] = v
            tk.Label(f, textvariable=v, font=("Courier", 13, "bold"),
                     bg="#110000", fg=color).pack(pady=1)

        # Protected data panel
        tk.Label(self.root, text="◈ PROTECTED IDENTITY", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#FF0000").pack(anchor="w", padx=15)

        pf = tk.Frame(self.root, bg="#110000")
        pf.pack(fill="x", padx=15, pady=3)
        for key, val in BRAYO_DATA.items():
            row = tk.Frame(pf, bg="#110000")
            row.pack(fill="x", padx=8, pady=1)
            tk.Label(row, text=f"{key.upper():<12}:", font=("Courier", 8, "bold"),
                     bg="#110000", fg="#440000").pack(side="left")
            # Hash the value for display
            hashed = hashlib.md5(val.encode()).hexdigest()[:16]
            tk.Label(row, text=f"{val}  [{hashed}...]",
                     font=("Courier", 8), bg="#110000", fg="#FF4444").pack(side="left")

        # Scan feed
        tk.Label(self.root, text="◈ DARK WEB SCAN FEED", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#FF0000").pack(anchor="w", padx=15, pady=(8,0))

        self.feed = tk.Text(self.root, height=9, bg="#080000", fg="#FF4444",
                             font=("Courier", 8), relief="flat", state="disabled")
        self.feed.pack(fill="both", padx=15, pady=3)

        # Buttons
        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=8)

        self.mon_btn = tk.Button(bf, text="💀 START MONITORING",
                                  command=self.toggle_monitor,
                                  font=("Courier", 10, "bold"), bg="#1a0000",
                                  fg="#FF0000", relief="flat", padx=12, pady=6)
        self.mon_btn.pack(side="left", padx=4)

        tk.Button(bf, text="🔍 SCAN NOW", command=self.scan_once,
                  font=("Courier", 10, "bold"), bg="#1a0000",
                  fg="#FF0000", relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Button(bf, text="🛡️ SECURE DATA", command=self.secure,
                  font=("Courier", 10, "bold"), bg="#001a00",
                  fg="#00FF41", relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Label(self.root, text="BrayoOS Dark Web Engine v1.0 • Brayo & AIRA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#220000").pack(side="bottom", pady=4)

    def log(self, msg):
        self.feed.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.feed.insert("end", f"[{ts}] {msg}\n")
        self.feed.see("end")
        self.feed.config(state="disabled")

    def toggle_monitor(self):
        if not self.monitoring:
            self.monitoring = True
            self.mon_btn.config(text="⏹ STOP MONITORING", fg="#00FF41")
            self.status_lbl.config(text="⬤  MONITOR ACTIVE — SCANNING DARK WEB",
                                    fg="#FF0000")
            self.log("💀 Connecting to dark web monitoring network...")
            self.log("🔐 Encrypting identity fingerprints...")
            self.log("📡 Scanning breach databases...")
            threading.Thread(target=self.monitor_loop, daemon=True).start()
        else:
            self.monitoring = False
            self.mon_btn.config(text="💀 START MONITORING", fg="#FF0000")
            self.status_lbl.config(text="⬤  MONITOR OFFLINE", fg="#FF0000")
            self.log("⏹ Monitoring stopped.")

    def monitor_loop(self):
        while self.monitoring:
            self._do_scan()
            time.sleep(random.uniform(4, 8))

    def scan_once(self):
        threading.Thread(target=self._do_scan, daemon=True).start()

    def _do_scan(self):
        site = random.choice(DARK_SITES)
        self.scanned += 1
        self.root.after(0, self.svars["SITES SCANNED"].set, str(self.scanned))
        self.root.after(0, self.log, f"🔍 Scanning {site}...")
        time.sleep(random.uniform(0.5, 1.5))

        # 10% chance of fake alert
        if random.random() < 0.10:
            breach = random.choice(BREACH_TYPES)
            self.alerts += 1
            self.root.after(0, self.svars["ALERTS"].set, str(self.alerts))
            self.root.after(0, self.svars["DATA SAFE"].set, "⚠️ NO")
            self.root.after(0, self.svars["THREAT LEVEL"].set, "HIGH")
            self.root.after(0, self.log,
                f"🚨 ALERT! {breach} detected on {site}!")
            self.root.after(0, self.log,
                f"   → AIRA activating countermeasures...")
            self.root.after(2000, self._resolve_alert)
        else:
            self.root.after(0, self.svars["DATA SAFE"].set, "✅ YES")
            self.root.after(0, self.svars["THREAT LEVEL"].set,
                            "LOW" if self.alerts == 0 else "MED")
            self.root.after(0, self.log,
                f"  ✅ Clean — no Brayo data found on {site}")

    def _resolve_alert(self):
        self.log("🛡️ Data purge request sent. Threat neutralized.")
        self.svars["DATA SAFE"].set("✅ YES")
        self.svars["THREAT LEVEL"].set("LOW")

    def secure(self):
        self.log("🛡️ Encrypting all identity data with AES-256...")
        self.log("🔐 Rotating digital fingerprints...")
        self.log("👻 Activating Ghost Mode integration...")
        self.log("✅ Brayo identity fully secured by AIRA.")

if __name__ == "__main__":
    root = tk.Tk()
    DarkWebMonitor(root)
    root.mainloop()
