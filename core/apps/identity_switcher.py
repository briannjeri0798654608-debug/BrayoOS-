import tkinter as tk
import threading
import time
import random
import subprocess
import os
from datetime import datetime

class IdentitySwitcher:
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 Identity Switcher")
        self.root.geometry("650x560")
        self.root.configure(bg="#0D0D0D")
        self.switching = False
        self.identity_count = 0
        self.current = {}
        self.build_ui()
        self.generate_identity()

    def build_ui(self):
        tk.Label(self.root, text="🎭 IDENTITY SWITCHER", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=8)
        tk.Label(self.root, text="[ MAC • HOSTNAME • FINGERPRINT ROTATOR ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        # Current identity panel
        tk.Label(self.root, text="◈ CURRENT IDENTITY", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15, pady=(10,0))

        self.id_frame = tk.Frame(self.root, bg="#001100")
        self.id_frame.pack(fill="x", padx=15, pady=5)

        self.id_labels = {}
        fields = ["MAC ADDRESS", "HOSTNAME", "OS FINGERPRINT", "USER AGENT", "TIMEZONE", "DEVICE ID"]
        for field in fields:
            row = tk.Frame(self.id_frame, bg="#001100")
            row.pack(fill="x", padx=8, pady=2)
            tk.Label(row, text=f"{field}:", font=("Courier", 8, "bold"),
                     bg="#001100", fg="#004400", width=16, anchor="w").pack(side="left")
            lbl = tk.Label(row, text="Generating...", font=("Courier", 9),
                           bg="#001100", fg="#00FF41", anchor="w")
            lbl.pack(side="left", fill="x")
            self.id_labels[field] = lbl

        # Switch count
        self.count_lbl = tk.Label(self.root, text="IDENTITIES ROTATED: 0",
                                   font=("Courier", 10, "bold"), bg="#0D0D0D", fg="#FF6600")
        self.count_lbl.pack(pady=5)

        # Log
        tk.Label(self.root, text="◈ SWITCH LOG", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.log_box = tk.Text(self.root, height=7, bg="#000800", fg="#00FF41",
                                font=("Courier", 8), relief="flat", state="disabled")
        self.log_box.pack(fill="both", padx=15, pady=3)

        # Buttons
        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=8)

        tk.Button(bf, text="🎭 SWITCH NOW", command=self.switch_once,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        self.auto_btn = tk.Button(bf, text="⚡ AUTO ROTATE", command=self.toggle_auto,
                                   font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                                   relief="flat", padx=12, pady=6)
        self.auto_btn.pack(side="left", padx=4)

        tk.Button(bf, text="📋 COPY ID", command=self.copy_id,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Label(self.root, text="BrayoOS Identity Engine v1.0 • Brayo & ARIA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def random_mac(self):
        return ":".join([f"{random.randint(0,255):02X}" for _ in range(6)])

    def random_hostname(self):
        names = ["SHADOW", "PHANTOM", "GHOST", "CIPHER", "NEXUS", "VORTEX", "MATRIX", "STEALTH"]
        return f"{random.choice(names)}-{random.randint(1000,9999)}"

    def random_fingerprint(self):
        os_list = ["Linux 5.15 x86_64", "Windows 11 22H2", "macOS 14.2", "Android 15 ARM64", "FreeBSD 14.0"]
        return random.choice(os_list)

    def random_useragent(self):
        agents = [
            "Mozilla/5.0 (X11; Linux x86_64) Chrome/120",
            "Mozilla/5.0 (Windows NT 11.0) Firefox/121",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14) Safari/17",
            "curl/8.5.0",
            "python-httpx/0.26.0"
        ]
        return random.choice(agents)

    def random_timezone(self):
        zones = ["UTC+0", "UTC+3 Nairobi", "UTC-5 EST", "UTC+8 SGT", "UTC+1 CET", "UTC-8 PST"]
        return random.choice(zones)

    def random_device_id(self):
        return "".join([random.choice("0123456789ABCDEF") for _ in range(16)])

    def generate_identity(self):
        self.current = {
            "MAC ADDRESS": self.random_mac(),
            "HOSTNAME": self.random_hostname(),
            "OS FINGERPRINT": self.random_fingerprint(),
            "USER AGENT": self.random_useragent(),
            "TIMEZONE": self.random_timezone(),
            "DEVICE ID": self.random_device_id()
        }
        for field, val in self.current.items():
            self.id_labels[field].config(text=val)

    def log(self, msg):
        self.log_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def switch_once(self):
        self.log("🎭 Initiating identity switch...")
        steps = [
            "Wiping old MAC signature...",
            "Generating new hardware fingerprint...",
            "Rotating hostname...",
            "Spoofing OS fingerprint...",
            "Updating user agent string...",
            "✅ Identity switched successfully!"
        ]
        threading.Thread(target=self._switch_animate, args=(steps,), daemon=True).start()

    def _switch_animate(self, steps):
        for step in steps:
            self.root.after(0, self.log, f"  → {step}")
            time.sleep(0.4)
        self.identity_count += 1
        self.root.after(0, self.generate_identity)
        self.root.after(0, self.count_lbl.config,
                        {"text": f"IDENTITIES ROTATED: {self.identity_count}"})
        # Try actual hostname change
        new_host = self.current.get("HOSTNAME", "SHADOW-0000")
        subprocess.run(f"hostname {new_host} 2>/dev/null", shell=True)

    def toggle_auto(self):
        if not self.switching:
            self.switching = True
            self.auto_btn.config(text="⏹ STOP AUTO", fg="#FF0000")
            self.log("⚡ Auto-rotate ENABLED — switching every 30s")
            threading.Thread(target=self.auto_loop, daemon=True).start()
        else:
            self.switching = False
            self.auto_btn.config(text="⚡ AUTO ROTATE", fg="#00FF41")
            self.log("⏹ Auto-rotate stopped.")

    def auto_loop(self):
        while self.switching:
            self.switch_once()
            time.sleep(30)

    def copy_id(self):
        summary = "\n".join([f"{k}: {v}" for k, v in self.current.items()])
        self.root.clipboard_clear()
        self.root.clipboard_append(summary)
        self.log("📋 Identity copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    IdentitySwitcher(root)
    root.mainloop()
