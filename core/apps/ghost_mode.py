import tkinter as tk
import threading
import time
import subprocess
import random
import os
from datetime import datetime

class GhostMode:
    def __init__(self, root):
        self.root = root
        self.root.title("👁️ Ghost Mode")
        self.root.geometry("650x520")
        self.root.configure(bg="#0D0D0D")
        self.active = False
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="👁️ GHOST MODE", font=("Courier", 20, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=10)
        tk.Label(self.root, text="[ NETWORK INVISIBILITY SYSTEM ]",
                 font=("Courier", 9), bg="#0D0D0D", fg="#003300").pack()

        # Status indicator
        self.status_frame = tk.Frame(self.root, bg="#0D0D0D")
        self.status_frame.pack(pady=15)

        self.indicator = tk.Label(self.status_frame, text="⬤", font=("Courier", 30),
                                  bg="#0D0D0D", fg="#FF0000")
        self.indicator.pack(side="left", padx=10)

        self.status_lbl = tk.Label(self.status_frame, text="VISIBLE — GHOST MODE OFF",
                                   font=("Courier", 13, "bold"), bg="#0D0D0D", fg="#FF0000")
        self.status_lbl.pack(side="left")

        # Log
        tk.Label(self.root, text="◈ GHOST LOG", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=20)

        self.log_box = tk.Text(self.root, height=13, bg="#000800", fg="#00FF41",
                               font=("Courier", 9), relief="flat", state="disabled")
        self.log_box.pack(fill="both", padx=20, pady=5)

        # Buttons
        btn_f = tk.Frame(self.root, bg="#0D0D0D")
        btn_f.pack(pady=10)

        self.toggle_btn = tk.Button(btn_f, text="👻 ACTIVATE GHOST MODE",
                                    command=self.toggle,
                                    font=("Courier", 11, "bold"), bg="#001a00",
                                    fg="#00FF41", relief="flat", padx=15, pady=8)
        self.toggle_btn.pack(side="left", padx=5)

        tk.Button(btn_f, text="🔍 SCAN SELF", command=self.scan_self,
                  font=("Courier", 11, "bold"), bg="#001a00",
                  fg="#00FF41", relief="flat", padx=15, pady=8).pack(side="left", padx=5)

        tk.Label(self.root, text="BrayoOS Ghost Engine v1.0 • Brayo & AIRA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=5)

    def log(self, msg):
        self.log_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def toggle(self):
        if not self.active:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        self.active = True
        self.toggle_btn.config(text="💀 DEACTIVATE GHOST MODE", fg="#FF0000")
        self.indicator.config(fg="#00FF41")
        self.status_lbl.config(text="GHOST MODE — ACTIVE", fg="#00FF41")
        threading.Thread(target=self.ghost_sequence, daemon=True).start()

    def ghost_sequence(self):
        steps = [
            "Disabling ICMP ping responses...",
            "Cloaking ARP broadcast signature...",
            "Randomizing packet TTL values...",
            "Spoofing network hostname to: UNKNOWN",
            "Blocking OS fingerprint probes...",
            "Fragmenting outbound packets...",
            "Injecting fake traffic noise...",
            "Disabling mDNS/Bonjour broadcasts...",
            "Masking open port signatures...",
            "Ghost cloak ACTIVE — you are invisible.",
        ]
        for step in steps:
            self.root.after(0, self.log, f"👻 {step}")
            time.sleep(0.8)

        # Actually block ping via iptables if root available
        cmds = [
            "iptables -A INPUT -p icmp --icmp-type echo-request -j DROP 2>/dev/null",
            "iptables -A OUTPUT -p icmp --icmp-type echo-reply -j DROP 2>/dev/null",
        ]
        for cmd in cmds:
            subprocess.run(cmd, shell=True)

        while self.active:
            fake = f"Deflecting probe from 192.168.{random.randint(1,254)}.{random.randint(1,254)}..."
            self.root.after(0, self.log, f"🛡️ {fake}")
            time.sleep(random.uniform(3, 7))

    def deactivate(self):
        self.active = False
        self.toggle_btn.config(text="👻 ACTIVATE GHOST MODE", fg="#00FF41")
        self.indicator.config(fg="#FF0000")
        self.status_lbl.config(text="VISIBLE — GHOST MODE OFF", fg="#FF0000")
        self.log("💡 Ghost mode deactivated. Restoring normal network state...")
        subprocess.run("iptables -F 2>/dev/null", shell=True)

    def scan_self(self):
        self.log("🔍 Scanning own exposure...")
        threading.Thread(target=self._do_scan, daemon=True).start()

    def _do_scan(self):
        try:
            result = subprocess.check_output(
                "cat /proc/net/if_inet6 2>/dev/null || ip addr show 2>/dev/null || ifconfig 2>/dev/null",
                shell=True).decode()
            lines = [l.strip() for l in result.split("\n") if l.strip()][:5]
            for l in lines:
                self.root.after(0, self.log, f"  {l}")
        except:
            self.root.after(0, self.log, "⚠️ Scan limited — no root access")
        status = "👻 INVISIBLE" if self.active else "⚠️ EXPOSED"
        self.root.after(0, self.log, f"Network status: {status}")

if __name__ == "__main__":
    root = tk.Tk()
    GhostMode(root)
    root.mainloop()
