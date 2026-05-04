import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import socket

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"

class NetworkScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS - Network Scanner")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🌐 Network Scanner",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        buttons = [
            ("📡 Ping Sweep", self.ping_sweep),
            ("🔍 Port Scan", self.port_scan),
            ("📋 ARP Table", self.arp_table),
            ("🌍 My IP", self.my_ip),
        ]

        for name, cmd in buttons:
            tk.Button(btn_frame, text=name, bg="#1A1A1A",
                     fg=ACCENT, font=("monospace", 11),
                     command=cmd, relief=tk.FLAT,
                     cursor="hand2").pack(side=tk.LEFT, padx=5, pady=5)

        # Target entry
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame, text="Target:", bg=BG,
                fg=TEXT, font=("monospace", 11)).pack(side=tk.LEFT)

        self.target = tk.Entry(frame, bg="#1A1A1A", fg=TEXT,
                              font=("monospace", 11),
                              insertbackground=ACCENT, width=30)
        self.target.pack(side=tk.LEFT, padx=5)
        self.target.insert(0, "192.168.1.0/24")

        # Output
        self.output = scrolledtext.ScrolledText(
            self.root, bg="#1A1A1A", fg=ACCENT,
            font=("monospace", 10), wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def ping_sweep(self):
        self.output.delete(1.0, tk.END)
        self.log("Starting ping sweep...")
        def run():
            base = self.target.get().rsplit('.', 1)[0]
            for i in range(1, 255):
                ip = f"{base}.{i}"
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", ip],
                    capture_output=True)
                if result.returncode == 0:
                    self.log(f"✅ {ip} - ALIVE")
        threading.Thread(target=run).start()

    def port_scan(self):
        self.output.delete(1.0, tk.END)
        target = self.target.get().split('/')[0]
        self.log(f"Scanning ports on {target}...")
        def run():
            common_ports = [21,22,23,25,80,443,3306,8080,8443]
            for port in common_ports:
                try:
                    s = socket.socket()
                    s.settimeout(1)
                    result = s.connect_ex((target, port))
                    if result == 0:
                        self.log(f"✅ Port {port} - OPEN")
                    s.close()
                except:
                    pass
            self.log("Scan complete!")
        threading.Thread(target=run).start()

    def arp_table(self):
        self.output.delete(1.0, tk.END)
        self.log("Reading ARP table...")
        try:
            with open("/proc/net/arp") as f:
                for line in f:
                    self.log(line.strip())
        except Exception as e:
            self.log(f"Error: {e}")

    def my_ip(self):
        self.output.delete(1.0, tk.END)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            self.log(f"📍 Your IP: {ip}")
        except Exception as e:
            self.log(f"Error: {e}")

if __name__ == "__main__":
    NetworkScanner()
