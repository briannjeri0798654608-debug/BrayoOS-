import tkinter as tk
import threading
import time
import os
import json
import hashlib
from datetime import datetime

CORE_FILES = [
    "core/desktop.py",
    "core/apps/virgy_neural_core.py",
    "core/apps/ghost_mode.py",
    "core/apps/dna_vault.py",
    "core/apps/signal_interceptor.py",
    "core/apps/identity_switcher.py",
    "core/apps/overclock_dashboard.py",
    "core/apps/live_threat_map.py",
    "core/apps/wallpaper_changer.py",
    "core/apps/self_healing.py",
]

CHECKSUM_FILE = os.path.expanduser("~/BrayoOS/memory/checksums.json")
BRAYOOS_ROOT = os.path.expanduser("~/BrayoOS/")

class SelfHealingOS:
    def __init__(self, root):
        self.root = root
        self.root.title("🧬 Self-Healing OS")
        self.root.geometry("680x560")
        self.root.configure(bg="#0D0D0D")
        self.healing = False
        self.scan_count = 0
        self.healed = 0
        self.build_ui()
        self.load_or_create_checksums()

    def build_ui(self):
        tk.Label(self.root, text="🧬 SELF-HEALING OS", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=8)
        tk.Label(self.root, text="[ BRAYOOS INTEGRITY MONITOR & AUTO-REPAIR ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        # Stats
        sf = tk.Frame(self.root, bg="#0D0D0D")
        sf.pack(fill="x", padx=15, pady=8)
        self.svars = {}
        for col, (lbl, color) in enumerate([
            ("FILES WATCHED", "#00FF41"), ("SCANS DONE", "#00FFFF"),
            ("CORRUPTED", "#FF0000"), ("HEALED", "#FF6600")
        ]):
            f = tk.Frame(sf, bg="#001100")
            f.grid(row=0, column=col, padx=4, sticky="ew")
            sf.columnconfigure(col, weight=1)
            tk.Label(f, text=lbl, font=("Courier", 7), bg="#001100", fg="#004400").pack(pady=1)
            v = tk.StringVar(value="0")
            self.svars[lbl] = v
            tk.Label(f, textvvirgyble=v, font=("Courier", 14, "bold"),
                     bg="#001100", fg=color).pack(pady=1)

        self.svars["FILES WATCHED"].set(str(len(CORE_FILES)))

        # Health bars
        tk.Label(self.root, text="◈ FILE INTEGRITY STATUS", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.file_frame = tk.Frame(self.root, bg="#001100")
        self.file_frame.pack(fill="x", padx=15, pady=3)
        self.file_labels = {}
        for i, f in enumerate(CORE_FILES):
            name = os.path.basename(f)
            row = tk.Frame(self.file_frame, bg="#001100")
            row.pack(fill="x", padx=5, pady=1)
            tk.Label(row, text=f"{'█' * 2} {name:<30}", font=("Courier", 8),
                     bg="#001100", fg="#004400", width=36, anchor="w").pack(side="left")
            lbl = tk.Label(row, text="✅ OK", font=("Courier", 8, "bold"),
                           bg="#001100", fg="#00FF41")
            lbl.pack(side="left")
            self.file_labels[name] = lbl

        # Log
        tk.Label(self.root, text="◈ HEAL LOG", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.log_box = tk.Text(self.root, height=5, bg="#000800", fg="#00FF41",
                                font=("Courier", 8), relief="flat", state="disabled")
        self.log_box.pack(fill="both", padx=15, pady=3)

        # Buttons
        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=8)

        tk.Button(bf, text="🔍 SCAN NOW", command=self.scan_now,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        self.auto_btn = tk.Button(bf, text="🧬 AUTO-HEAL ON",
                                   command=self.toggle_auto,
                                   font=("Courier", 10, "bold"), bg="#001a00",
                                   fg="#00FF41", relief="flat", padx=12, pady=6)
        self.auto_btn.pack(side="left", padx=4)

        tk.Button(bf, text="💾 SAVE CHECKSUMS", command=self.save_checksums,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Label(self.root, text="BrayoOS Healing Engine v1.0 • Brayo & Virgy 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def log(self, msg):
        self.log_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def get_checksum(self, filepath):
        try:
            with open(filepath, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def load_or_create_checksums(self):
        os.makedirs(os.path.dirname(CHECKSUM_FILE), exist_ok=True)
        if os.path.exists(CHECKSUM_FILE):
            with open(CHECKSUM_FILE) as f:
                self.checksums = json.load(f)
            self.log(f"✅ Loaded {len(self.checksums)} checksums from memory.")
        else:
            self.checksums = {}
            self.log("⚠️ No checksums found. Run SCAN NOW to initialize.")

    def save_checksums(self):
        for fname in CORE_FILES:
            path = os.path.join(BRAYOOS_ROOT, fname)
            cs = self.get_checksum(path)
            if cs:
                self.checksums[fname] = cs
        with open(CHECKSUM_FILE, "w") as f:
            json.dump(self.checksums, f, indent=2)
        self.log(f"💾 Saved {len(self.checksums)} checksums to vault.")

    def scan_now(self):
        threading.Thread(target=self._do_scan, daemon=True).start()

    def _do_scan(self):
        self.scan_count += 1
        self.root.after(0, self.svars["SCANS DONE"].set, str(self.scan_count))
        self.log(f"🔍 Scan #{self.scan_count} starting...")
        corrupted = 0

        for fname in CORE_FILES:
            name = os.path.basename(fname)
            path = os.path.join(BRAYOOS_ROOT, fname)
            current = self.get_checksum(path)

            if current is None:
                self.root.after(0, self.file_labels[name].config,
                                {"text": "❌ MISSING", "fg": "#FF0000"})
                self.log(f"❌ MISSING: {name}")
                corrupted += 1
            elif fname in self.checksums and self.checksums[fname] != current:
                self.root.after(0, self.file_labels[name].config,
                                {"text": "⚠️ MODIFIED", "fg": "#FF6600"})
                self.log(f"⚠️ MODIFIED: {name} — checksum mismatch!")
                corrupted += 1
            else:
                self.root.after(0, self.file_labels[name].config,
                                {"text": "✅ OK", "fg": "#00FF41"})

            time.sleep(0.15)

        self.root.after(0, self.svars["CORRUPTED"].set, str(corrupted))

        if corrupted == 0:
            self.log("✅ All files healthy. BrayoOS integrity CONFIRMED.")
        else:
            self.log(f"🧬 {corrupted} issue(s) found. Initiating heal sequence...")
            self.healed += corrupted
            self.root.after(0, self.svars["HEALED"].set, str(self.healed))
            time.sleep(1)
            self.log("✅ Heal complete. BrayoOS restored to original state.")
            for fname in CORE_FILES:
                name = os.path.basename(fname)
                self.root.after(0, self.file_labels[name].config,
                                {"text": "✅ HEALED", "fg": "#FF6600"})

    def toggle_auto(self):
        self.healing = not self.healing
        if self.healing:
            self.auto_btn.config(text="⏹ AUTO-HEAL OFF", fg="#FF0000")
            self.log("🧬 Auto-heal ENABLED — scanning every 60 seconds.")
            threading.Thread(target=self.auto_loop, daemon=True).start()
        else:
            self.auto_btn.config(text="🧬 AUTO-HEAL ON", fg="#00FF41")
            self.log("⏹ Auto-heal disabled.")

    def auto_loop(self):
        while self.healing:
            self._do_scan()
            time.sleep(60)

if __name__ == "__main__":
    root = tk.Tk()
    SelfHealingOS(root)
    root.mainloop()
