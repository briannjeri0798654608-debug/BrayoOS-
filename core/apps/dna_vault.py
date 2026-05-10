import tkinter as tk
from tkinter import messagebox
import threading
import time
import hashlib
import json
import os
from datetime import datetime

VAULT_FILE = os.path.expanduser("~/BrayoOS/memory/dna_vault.json")
os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)

REAL_PIN = hashlib.sha256("1337".encode()).hexdigest()
DECOY_PIN = hashlib.sha256("0000".encode()).hexdigest()

VAULT_DATA = {
    "owner": "Brayo",
    "location": "Kenya",
    "clearance": "LEVEL 5 — MAXIMUM",
    "tools": ["Ghost Mode", "Signal Interceptor", "Virgy Core", "Identity Switcher"],
    "motto": "Two minds. One OS. Built Different."
}

class DNAVault:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 DNA Vault")
        self.root.geometry("500x600")
        self.root.configure(bg="#0D0D0D")
        self.attempts = 0
        self.unlocked = False
        self.load_state()
        self.show_lock_screen()

    def load_state(self):
        if os.path.exists(VAULT_FILE):
            with open(VAULT_FILE) as f:
                self.state = json.load(f)
        else:
            self.state = {"unlocks": 0, "failed_attempts": 0, "last_access": "Never"}

    def save_state(self):
        with open(VAULT_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def show_lock_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="🔐 DNA VAULT", font=("Courier", 22, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=20)
        tk.Label(self.root, text="BRAYO SECURITY CLEARANCE REQUIRED",
                 font=("Courier", 9), bg="#0D0D0D", fg="#003300").pack()

        # DNA animation label
        self.dna_lbl = tk.Label(self.root, text="", font=("Courier", 10),
                                 bg="#0D0D0D", fg="#00FF41")
        self.dna_lbl.pack(pady=5)
        threading.Thread(target=self.animate_dna, daemon=True).start()

        tk.Label(self.root, text="◈ BIOMETRIC PIN REQUIRED", font=("Courier", 11, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=15)

        # PIN display
        self.pin_display = tk.Label(self.root, text="[ _ _ _ _ ]",
                                     font=("Courier", 20, "bold"), bg="#0D0D0D", fg="#00FF41")
        self.pin_display.pack(pady=10)

        self.pin = ""

        # Numpad
        pad = tk.Frame(self.root, bg="#0D0D0D")
        pad.pack(pady=5)

        buttons = [
            ("1","2","3"),
            ("4","5","6"),
            ("7","8","9"),
            ("⌫","0","✓")
        ]
        for row in buttons:
            rf = tk.Frame(pad, bg="#0D0D0D")
            rf.pack()
            for ch in row:
                tk.Button(rf, text=ch, font=("Courier", 14, "bold"),
                          width=4, height=2,
                          bg="#001a00", fg="#00FF41", relief="flat",
                          activebackground="#00FF41", activeforeground="#000",
                          command=lambda c=ch: self.key_press(c)).pack(side="left", padx=3, pady=3)

        # Stats
        stats = tk.Frame(self.root, bg="#0D0D0D")
        stats.pack(pady=10)
        tk.Label(stats, text=f"Unlocks: {self.state['unlocks']}   Failed: {self.state['failed_attempts']}   Last: {self.state['last_access']}",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        self.msg = tk.Label(self.root, text="", font=("Courier", 10),
                             bg="#0D0D0D", fg="#FF0000")
        self.msg.pack(pady=5)

        tk.Label(self.root, text="BrayoOS DNA Vault v1.0 • Brayo & Virgy 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=8)

    def animate_dna(self):
        frames = [
            "A-T-G-C-A-T-G-C >>>",
            ">>> A-T-G-C-A-T-G",
            "G-C >>> A-T-G-C-A",
            "SCANNING DNA... ▓▓▓",
            "MATCH REQUIRED  ░░░",
        ]
        i = 0
        while not self.unlocked:
            self.root.after(0, self.dna_lbl.config, {"text": frames[i % len(frames)]})
            i += 1
            time.sleep(0.6)

    def key_press(self, ch):
        if ch == "⌫":
            self.pin = self.pin[:-1]
        elif ch == "✓":
            self.check_pin()
            return
        else:
            if len(self.pin) < 4:
                self.pin += ch
        dots = "[ " + " ".join(["●" if i < len(self.pin) else "_" for i in range(4)]) + " ]"
        self.pin_display.config(text=dots)

    def check_pin(self):
        hashed = hashlib.sha256(self.pin.encode()).hexdigest()
        if hashed == REAL_PIN:
            self.unlocked = True
            self.state["unlocks"] += 1
            self.state["last_access"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save_state()
            self.show_vault()
        elif hashed == DECOY_PIN:
            self.show_decoy()
        else:
            self.attempts += 1
            self.state["failed_attempts"] += 1
            self.save_state()
            self.pin = ""
            self.pin_display.config(text="[ _ _ _ _ ]")
            self.msg.config(text=f"⚠️ ACCESS DENIED — Attempt {self.attempts}/3")
            if self.attempts >= 3:
                self.lockdown()

    def show_vault(self):
        for w in self.root.winfo_children():
            w.destroy()
        tk.Label(self.root, text="✅ VAULT UNLOCKED", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=20)
        tk.Label(self.root, text="WELCOME BACK, BRAYO", font=("Courier", 12),
                 bg="#0D0D0D", fg="#00FF41").pack()

        for key, val in VAULT_DATA.items():
            f = tk.Frame(self.root, bg="#001100")
            f.pack(fill="x", padx=20, pady=3)
            tk.Label(f, text=f"{key.upper()}:", font=("Courier", 9, "bold"),
                     bg="#001100", fg="#004400").pack(anchor="w", padx=5)
            v = ", ".join(val) if isinstance(val, list) else val
            tk.Label(f, text=v, font=("Courier", 10), bg="#001100",
                     fg="#00FF41", wraplength=400).pack(anchor="w", padx=5, pady=2)

        tk.Button(self.root, text="🔒 LOCK VAULT", command=self.show_lock_screen,
                  font=("Courier", 11, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=15, pady=8).pack(pady=20)

    def show_decoy(self):
        for w in self.root.winfo_children():
            w.destroy()
        tk.Label(self.root, text="✅ ACCESS GRANTED", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=30)
        tk.Label(self.root, text="Welcome, Guest", font=("Courier", 12),
                 bg="#0D0D0D", fg="#888888").pack()
        tk.Label(self.root, text="No sensitive data found.",
                 font=("Courier", 10), bg="#0D0D0D", fg="#444444").pack(pady=20)
        tk.Button(self.root, text="Back", command=self.show_lock_screen,
                  font=("Courier", 10), bg="#111111", fg="#444444", relief="flat").pack()

    def lockdown(self):
        for w in self.root.winfo_children():
            w.destroy()
        tk.Label(self.root, text="🚨 LOCKDOWN", font=("Courier", 24, "bold"),
                 bg="#0D0D0D", fg="#FF0000").pack(pady=40)
        tk.Label(self.root, text="TOO MANY FAILED ATTEMPTS\nBRAYO HAS BEEN NOTIFIED\nVAULT SEALED FOR 60 SECONDS",
                 font=("Courier", 11), bg="#0D0D0D", fg="#FF0000", justify="center").pack()
        threading.Thread(target=self.countdown_unlock, daemon=True).start()

    def countdown_unlock(self):
        time.sleep(60)
        self.attempts = 0
        self.root.after(0, self.show_lock_screen)

if __name__ == "__main__":
    root = tk.Tk()
    DNAVault(root)
    root.mainloop()
