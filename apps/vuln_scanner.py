import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import subprocess
import httpx

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class VulnScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ Vulnerability Scanner")
        self.root.configure(bg=BG)
        self.root.geometry("700x600")
        self.scanning = False
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🛡️ Vulnerability Scanner",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        # Target frame
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Target:",
                bg=BG, fg=TEXT,
                font=("monospace", 11)).pack(side=tk.LEFT)

        self.target = tk.Entry(frame, bg=DARK, fg=ACCENT,
                              font=("monospace", 11),
                              insertbackground=ACCENT)
        self.target.pack(side=tk.LEFT, fill=tk.X,
                        expand=True, padx=5)
        self.target.insert(0, "192.168.1.1")

        # Scan buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        for text, cmd in [
            ("🔍 Full Scan", self.full_scan),
            ("🚪 Port Scan", self.port_scan),
            ("🌐 Web Scan", self.web_scan),
            ("📡 Ping", self.ping_target),
            ("⏹ Stop", self.stop_scan)
        ]:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 10),
                     command=cmd,
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=3)

        # Output
        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        # Status
        self.status = tk.Label(self.root, text="Ready",
                              bg=DARK, fg=TEXT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def stop_scan(self):
        self.scanning = False
        self.status.config(text="⏹ Scan stopped!")

    def ping_target(self):
        target = self.target.get().strip()
        self.output.delete(1.0, tk.END)
        self.log(f"📡 Pinging {target}...")
        def run():
            result = subprocess.run(
                ["ping", "-c", "4", target],
                capture_output=True, text=True)
            self.log(result.stdout)
            if result.returncode == 0:
                self.log("✅ Host is ALIVE!")
            else:
                self.log("❌ Host is DOWN or unreachable!")
        threading.Thread(target=run).start()

    def port_scan(self):
        target = self.target.get().strip()
        self.output.delete(1.0, tk.END)
        self.scanning = True
        self.log(f"🔍 Port scanning {target}...")
        self.log("═" * 50)

        vuln_ports = {
            21: ("FTP", "Anonymous login possible"),
            22: ("SSH", "Check weak passwords/old version"),
            23: ("Telnet", "⚠️ INSECURE - plaintext protocol!"),
            25: ("SMTP", "Check open relay"),
            53: ("DNS", "Check zone transfer"),
            80: ("HTTP", "Check web vulnerabilities"),
            110: ("POP3", "Check default credentials"),
            143: ("IMAP", "Check default credentials"),
            443: ("HTTPS", "Check SSL/TLS config"),
            445: ("SMB", "⚠️ Check EternalBlue MS17-010"),
            1433: ("MSSQL", "Check default credentials"),
            3306: ("MySQL", "Check root no password"),
            3389: ("RDP", "⚠️ Check BlueKeep CVE-2019-0708"),
            5432: ("PostgreSQL", "Check default credentials"),
            6379: ("Redis", "Check no authentication"),
            8080: ("HTTP-Alt", "Check misconfigurations"),
            8443: ("HTTPS-Alt", "Check certificates"),
            9200: ("Elasticsearch", "⚠️ Check open access"),
            27017: ("MongoDB", "Check no authentication"),
        }

        def run():
            open_ports = []
            for port, (service, risk) in vuln_ports.items():
                if not self.scanning:
                    break
                try:
                    s = socket.socket()
                    s.settimeout(1)
                    if s.connect_ex((target, port)) == 0:
                        open_ports.append(port)
                        self.log(
                            f"⚠️  {port}/{service} OPEN\n"
                            f"   Risk: {risk}")
                    s.close()
                except:
                    pass

            self.log("\n" + "═" * 50)
            self.log(f"📊 Scan Results for {target}:")
            self.log(f"✅ Open ports found: {len(open_ports)}")

            if len(open_ports) == 0:
                self.log("🟢 RISK: LOW - No common ports open")
            elif len(open_ports) <= 3:
                self.log("🟡 RISK: MEDIUM - Some ports open")
            elif len(open_ports) <= 6:
                self.log("🔴 RISK: HIGH - Many ports open!")
            else:
                self.log("💀 RISK: CRITICAL - Very exposed!")

            self.log("\n✅ Port scan complete!")
            self.status.config(text="✅ Done!")
        threading.Thread(target=run).start()

    def web_scan(self):
        target = self.target.get().strip()
        if not target.startswith("http"):
            target = "http://" + target
        self.output.delete(1.0, tk.END)
        self.log(f"🌐 Web scanning {target}...")
        self.log("═" * 50)

        def run():
            # Check common paths
            paths = [
                "/admin", "/login", "/wp-admin",
                "/phpmyadmin", "/.env", "/config.php",
                "/backup", "/robots.txt", "/sitemap.xml",
                "/.git", "/api", "/dashboard",
                "/manager", "/administrator",
            ]
            try:
                with httpx.Client(
                    follow_redirects=True,
                    timeout=5
                ) as client:
                    for path in paths:
                        if not self.scanning:
                            break
                        try:
                            url = target + path
                            r = client.get(url)
                            if r.status_code == 200:
                                self.log(
                                    f"✅ FOUND: {url} "
                                    f"[{r.status_code}]")
                            elif r.status_code == 403:
                                self.log(
                                    f"🔒 FORBIDDEN: {url} "
                                    f"[{r.status_code}]")
                            elif r.status_code == 401:
                                self.log(
                                    f"🔑 AUTH REQUIRED: {url} "
                                    f"[{r.status_code}]")
                        except:
                            pass
            except Exception as e:
                self.log(f"Error: {e}")
            self.log("\n✅ Web scan complete!")
            self.status.config(text="✅ Done!")
        threading.Thread(target=run).start()

    def full_scan(self):
        self.output.delete(1.0, tk.END)
        self.scanning = True
        target = self.target.get().strip()
        self.log(f"🔍 Starting FULL scan on {target}")
        self.log("═" * 50)
        self.ping_target()
        self.root.after(2000, self.port_scan)
        self.root.after(5000, self.web_scan)

if __name__ == "__main__":
    VulnScanner()
