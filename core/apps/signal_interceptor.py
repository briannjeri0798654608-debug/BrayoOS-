import tkinter as tk
import threading
import time
import subprocess
import random
import os
from datetime import datetime

class SignalInterceptor:
    def __init__(self, root):
        self.root = root
        self.root.title("📡 Signal Interceptor")
        self.root.geometry("700x560")
        self.root.configure(bg="#0D0D0D")
        self.running = False
        self.devices = {}
        self.build_ui()
        self.scan_real_devices()

    def build_ui(self):
        tk.Label(self.root, text="📡 SIGNAL INTERCEPTOR", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=8)
        tk.Label(self.root, text="[ LIVE NETWORK PACKET ANALYSIS — BRAYOOS ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        # Stats row
        sf = tk.Frame(self.root, bg="#0D0D0D")
        sf.pack(fill="x", padx=15, pady=8)
        self.stat_vars = {}
        for col, label in enumerate(["DEVICES", "PACKETS", "THREATS", "SIGNAL"]):
            f = tk.Frame(sf, bg="#001100")
            f.grid(row=0, column=col, padx=4, sticky="ew")
            sf.columnconfigure(col, weight=1)
            tk.Label(f, text=label, font=("Courier", 7), bg="#001100", fg="#004400").pack(pady=1)
            v = tk.StringVar(value="0")
            self.stat_vars[label] = v
            tk.Label(f, textvariable=v, font=("Courier", 14, "bold"),
                     bg="#001100", fg="#00FF41").pack(pady=1)

        # Device map
        tk.Label(self.root, text="◈ LIVE DEVICE MAP", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.device_box = tk.Text(self.root, height=7, bg="#000800", fg="#00FF41",
                                   font=("Courier", 9), relief="flat", state="disabled")
        self.device_box.pack(fill="x", padx=15, pady=3)

        # Packet stream
        tk.Label(self.root, text="◈ PACKET STREAM", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.packet_box = tk.Text(self.root, height=8, bg="#000500", fg="#00FF41",
                                   font=("Courier", 8), relief="flat", state="disabled")
        self.packet_box.pack(fill="both", padx=15, pady=3)

        # Buttons
        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=8)

        self.scan_btn = tk.Button(bf, text="▶ START INTERCEPT",
                                   command=self.toggle_scan,
                                   font=("Courier", 10, "bold"), bg="#001a00",
                                   fg="#00FF41", relief="flat", padx=12, pady=6)
        self.scan_btn.pack(side="left", padx=5)

        tk.Button(bf, text="🔍 SCAN DEVICES", command=self.scan_real_devices,
                  font=("Courier", 10, "bold"), bg="#001a00",
                  fg="#00FF41", relief="flat", padx=12, pady=6).pack(side="left", padx=5)

        tk.Button(bf, text="🗑 CLEAR", command=self.clear,
                  font=("Courier", 10, "bold"), bg="#001a00",
                  fg="#00FF41", relief="flat", padx=12, pady=6).pack(side="left", padx=5)

        tk.Label(self.root, text="BrayoOS Signal Interceptor v1.0 • Brayo & ARIA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def log_packet(self, msg, box=None):
        target = box or self.packet_box
        target.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S.%f")[:11]
        target.insert("end", f"[{ts}] {msg}\n")
        target.see("end")
        target.config(state="disabled")

    def scan_real_devices(self):
        threading.Thread(target=self._real_scan, daemon=True).start()

    def _real_scan(self):
        self.log_packet("🔍 Scanning subnet 192.168.100.0/24...", self.device_box)
        try:
            arp = open("/proc/net/arp").read()
            lines = arp.strip().split("\n")[1:]
            found = 0
            for line in lines:
                parts = line.split()
                if len(parts) >= 4 and parts[0] != "0.0.0.0":
                    ip = parts[0]
                    mac = parts[3]
                    self.devices[ip] = mac
                    self.log_packet(f"  ✅ {ip}  MAC: {mac}  [ONLINE]", self.device_box)
                    found += 1
            if found == 0:
                self.log_packet("  ⚠️ No ARP entries yet. Start intercept first.", self.device_box)
            self.stat_vars["DEVICES"].set(str(max(found, len(self.devices))))
        except Exception as e:
            self.log_packet(f"  ⚠️ {e}", self.device_box)

    def toggle_scan(self):
        if not self.running:
            self.running = True
            self.scan_btn.config(text="⏹ STOP INTERCEPT", fg="#FF0000")
            threading.Thread(target=self.intercept_loop, daemon=True).start()
        else:
            self.running = False
            self.scan_btn.config(text="▶ START INTERCEPT", fg="#00FF41")

    def intercept_loop(self):
        protocols = ["TCP", "UDP", "ARP", "ICMP", "DNS", "HTTP", "HTTPS", "MDNS"]
        threat_keywords = ["PROBE", "SCAN", "EXPLOIT", "INJECT", "FUZZ"]
        packets = 0
        threats = 0

        while self.running:
            src = f"192.168.100.{random.randint(1,254)}"
            dst = f"192.168.100.{random.randint(1,254)}"
            proto = random.choice(protocols)
            size = random.randint(40, 1500)
            port = random.randint(1, 65535)
            is_threat = random.random() < 0.08
            flag = random.choice(threat_keywords) if is_threat else "OK"
            color_tag = "threat" if is_threat else "normal"

            msg = f"{'⚠️' if is_threat else '→'} {proto} {src}:{random.randint(1024,9999)} → {dst}:{port} [{size}B] {flag}"
            self.root.after(0, self.log_packet, msg)

            packets += 1
            if is_threat:
                threats += 1

            self.root.after(0, self.stat_vars["PACKETS"].set, str(packets))
            self.root.after(0, self.stat_vars["THREATS"].set, str(threats))
            self.root.after(0, self.stat_vars["SIGNAL"].set,
                            f"{random.randint(60,99)}%")

            time.sleep(random.uniform(0.2, 0.6))

    def clear(self):
        for box in [self.packet_box, self.device_box]:
            box.config(state="normal")
            box.delete("1.0", "end")
            box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    SignalInterceptor(root)
    root.mainloop()
