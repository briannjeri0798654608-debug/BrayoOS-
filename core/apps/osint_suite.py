import tkinter as tk
import threading
import subprocess
import httpx
import time
from datetime import datetime

BG="#080810"; BG2="#0D0D1A"; BG3="#12122A"
PURPLE="#9D00FF"; NEON="#CC44FF"; WHITE="#E0E0FF"
DIM="#444466"; RED="#FF0044"; GREEN="#44FF88"; GOLD="#FFD700"

class OSINTSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 OSINT Suite")
        self.root.geometry("650x500")
        self.root.configure(bg=BG)
        self.tool = "ip"
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="🔍 BRAYOOS OSINT SUITE",
                 font=("Courier",14,"bold"),
                 bg=BG, fg=NEON).pack(pady=8)
        tk.Frame(self.root, bg=PURPLE, height=2).pack(fill="x")

        # Tool selector
        tf = tk.Frame(self.root, bg=BG2)
        tf.pack(fill="x", padx=10, pady=5)
        self.btns = {}
        tools = [
            ("IP Track","ip",RED),
            ("Username","username",NEON),
            ("Domain","domain",GREEN),
            ("Email","email","#44FFFF"),
            ("Breach","breach",GOLD),
            ("Metadata","meta","#FF44AA"),
        ]
        for name, key, color in tools:
            b = tk.Button(tf, text=name,
                          font=("Courier",8,"bold"),
                          bg=BG3, fg=color, relief="flat",
                          padx=8, pady=5,
                          command=lambda k=key,c=color,n=name:
                          self.select(k,c,n))
            b.pack(side="left", padx=2, pady=4)
            self.btns[key] = b

        # Input
        inf = tk.Frame(self.root, bg=BG3)
        inf.pack(fill="x", padx=10, pady=3)
        tk.Label(inf, text="TARGET:", font=("Courier",9,"bold"),
                 bg=BG3, fg=PURPLE).pack(side="left", padx=8)
        self.inp = tk.Entry(inf, font=("Courier",11),
                             bg=BG, fg=WHITE,
                             insertbackground=NEON, relief="flat")
        self.inp.pack(side="left", fill="x", expand=True, ipady=7)
        self.inp.bind("<Return>", lambda e: self.scan())
        self.go_btn = tk.Button(inf, text="SCAN ▶",
                                 font=("Courier",9,"bold"),
                                 bg=PURPLE, fg=WHITE, relief="flat",
                                 padx=12, command=self.scan)
        self.go_btn.pack(side="right", padx=6, pady=4)

        # Results
        self.out = tk.Text(self.root, bg=BG3, fg=WHITE,
                            font=("Courier",9), relief="flat",
                            state="disabled", wrap="word",
                            height=18)
        self.out.pack(fill="both", expand=True, padx=10, pady=5)
        self.out.tag_config("g", foreground=GREEN)
        self.out.tag_config("r", foreground=RED)
        self.out.tag_config("y", foreground=GOLD)
        self.out.tag_config("c", foreground="#44FFFF")
        self.out.tag_config("p", foreground=NEON)

        # Bottom
        bf = tk.Frame(self.root, bg=BG)
        bf.pack(fill="x", padx=10, pady=3)
        tk.Button(bf, text="Clear", font=("Courier",8),
                  bg=BG3, fg=WHITE, relief="flat", padx=8,
                  command=self.clear).pack(side="left", padx=2)
        tk.Button(bf, text="Copy", font=("Courier",8),
                  bg=BG3, fg=NEON, relief="flat", padx=8,
                  command=self.copy).pack(side="left", padx=2)
        tk.Label(bf, text="⚠ Ethical use only",
                 font=("Courier",7), bg=BG, fg=DIM).pack(side="right")

        self.select("ip", RED, "IP Track")
        self.log("BrayoOS OSINT Suite ready 🇰🇪", "p")
        self.log("Select a tool and enter target\n", "y")

    def select(self, tool, color, name):
        self.tool = tool
        self.go_btn.config(bg=color)
        for k, b in self.btns.items():
            b.config(relief="flat")
        self.btns[tool].config(relief="solid")
        hints = {
            "ip": "8.8.8.8 or domain.com",
            "username": "brayo_ke",
            "domain": "brayoos.com",
            "email": "user@gmail.com",
            "breach": "user@gmail.com",
            "meta": "/sdcard/photo.jpg",
        }
        self.inp.delete(0,"end")
        self.inp.insert(0, hints.get(tool,""))

    def log(self, msg, tag="c"):
        self.out.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.out.insert("end", f"[{ts}] {msg}\n", tag)
        self.out.see("end")
        self.out.config(state="disabled")

    def scan(self):
        target = self.inp.get().strip()
        if not target:
            return
        self.log(f"Scanning: {target}", "y")
        threading.Thread(target=self._run,
                         args=(self.tool, target),
                         daemon=True).start()

    def _run(self, tool, target):
        try:
            if tool == "ip":
                r = httpx.get(f"https://ipapi.co/{target}/json/",
                               timeout=8)
                d = r.json()
                for k in ["ip","city","region","country_name",
                           "org","timezone"]:
                    if d.get(k):
                        self.root.after(0, self.log,
                                        f"  {k}: {d[k]}", "g")

            elif tool == "username":
                sites = [
                    ("GitHub","https://github.com/{}"),
                    ("Twitter","https://twitter.com/{}"),
                    ("Instagram","https://instagram.com/{}"),
                    ("Reddit","https://reddit.com/u/{}"),
                    ("TikTok","https://tiktok.com/@{}"),
                    ("Telegram","https://t.me/{}"),
                    ("YouTube","https://youtube.com/@{}"),
                    ("GitLab","https://gitlab.com/{}"),
                ]
                for name, url in sites:
                    try:
                        r = httpx.get(url.format(target),
                                       timeout=5,
                                       follow_redirects=True,
                                       headers={"User-Agent":"Mozilla/5.0"})
                        tag = "g" if r.status_code==200 else "r"
                        status = "FOUND" if r.status_code==200 else "NOT FOUND"
                        self.root.after(0, self.log,
                                        f"  {status} — {name}", tag)
                    except:
                        self.root.after(0, self.log,
                                        f"  TIMEOUT — {name}", "y")
                    time.sleep(0.2)

            elif tool == "domain":
                result = subprocess.check_output(
                    f"nslookup {target} 2>/dev/null",
                    shell=True, timeout=8).decode()
                for line in result.split("\n")[:10]:
                    if line.strip():
                        self.root.after(0, self.log,
                                        f"  {line.strip()}", "g")

            elif tool == "email":
                domain = target.split("@")[-1]
                self.root.after(0, self.log,
                                f"  Domain: {domain}", "g")
                try:
                    r = subprocess.check_output(
                        f"host -t MX {domain} 2>/dev/null",
                        shell=True, timeout=5).decode()
                    for line in r.split("\n")[:3]:
                        if line.strip():
                            self.root.after(0, self.log,
                                            f"  MX: {line.strip()}", "g")
                except:
                    pass
                self.root.after(0, self.log,
                                f"  Check: haveibeenpwned.com", "y")

            elif tool == "breach":
                self.root.after(0, self.log,
                                "  Checking breach databases...", "c")
                time.sleep(1)
                self.root.after(0, self.log,
                                f"  → haveibeenpwned.com/account/{target}", "y")
                self.root.after(0, self.log,
                                f"  → dehashed.com/search?query={target}", "y")
                self.root.after(0, self.log,
                                f"  → intelx.io/?s={target}", "y")

            elif tool == "meta":
                result = subprocess.check_output(
                    f"exiftool '{target}' 2>/dev/null || echo 'Install: pkg install exiftool'",
                    shell=True, timeout=8).decode()
                for line in result.split("\n")[:15]:
                    if line.strip():
                        tag = "g" if any(
                            k in line.lower() for k in
                            ["gps","date","model","location"]
                        ) else "c"
                        self.root.after(0, self.log,
                                        f"  {line}", tag)

        except Exception as e:
            self.root.after(0, self.log, f"Error: {e}", "r")

        self.root.after(0, self.log, "Scan complete ✓\n", "p")

    def clear(self):
        self.out.config(state="normal")
        self.out.delete("1.0","end")
        self.out.config(state="disabled")

    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.out.get("1.0","end"))
        self.log("Copied!", "p")

if __name__ == "__main__":
    root = tk.Tk()
    OSINTSuite(root)
    root.mainloop()
