import tkinter as tk
import threading
import time
import random
from datetime import datetime

CITIES = [
    ("Nairobi", 280, 310), ("Lagos", 220, 290), ("Cairo", 310, 220),
    ("London", 240, 150), ("Paris", 255, 160), ("Berlin", 270, 148),
    ("Moscow", 330, 130), ("Dubai", 360, 230), ("Mumbai", 400, 255),
    ("Beijing", 460, 195), ("Tokyo", 510, 195), ("Sydney", 500, 360),
    ("New York", 130, 195), ("LA", 90, 210), ("Chicago", 130, 185),
    ("Sao Paulo", 185, 340), ("Mexico", 100, 245), ("Toronto", 145, 180),
    ("Singapore", 460, 295), ("Seoul", 490, 190), ("Istanbul", 320, 195),
]

ATTACK_TYPES = [
    "DDoS", "SQL Injection", "Ransomware", "Phishing",
    "Zero-Day", "Brute Force", "MITM", "Malware", "APT"
]

class LiveThreatMap:
    def __init__(self, root):
        self.root = root
        self.root.title("🔴 Live Threat Map")
        self.root.geometry("720x560")
        self.root.configure(bg="#0D0D0D")
        self.running = True
        self.attack_count = 0
        self.build_ui()
        threading.Thread(target=self.attack_loop, daemon=True).start()

    def build_ui(self):
        tk.Label(self.root, text="🔴 LIVE THREAT MAP", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#FF0000").pack(pady=6)
        tk.Label(self.root, text="[ GLOBAL CYBERATTACK MONITOR — BRAYOOS ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#330000").pack()

        # Stats
        sf = tk.Frame(self.root, bg="#0D0D0D")
        sf.pack(fill="x", padx=15, pady=5)
        self.stat_vars = {}
        for col, (label, color) in enumerate([
            ("ATTACKS", "#FF0000"), ("BLOCKED", "#00FF41"),
            ("COUNTRIES", "#FF6600"), ("THREAT LVL", "#FF0000")
        ]):
            f = tk.Frame(sf, bg="#110000")
            f.grid(row=0, column=col, padx=4, sticky="ew")
            sf.columnconfigure(col, weight=1)
            tk.Label(f, text=label, font=("Courier", 7), bg="#110000", fg="#330000").pack(pady=1)
            v = tk.StringVar(value="0")
            self.stat_vars[label] = v
            tk.Label(f, textvariable=v, font=("Courier", 14, "bold"),
                     bg="#110000", fg=color).pack(pady=1)

        # World map canvas
        self.canvas = tk.Canvas(self.root, width=690, height=280,
                                bg="#000811", highlightthickness=1,
                                highlightbackground="#330000")
        self.canvas.pack(padx=15, pady=5)
        self.draw_map()

        # Attack log
        tk.Label(self.root, text="◈ ATTACK FEED", font=("Courier", 9, "bold"),
                 bg="#0D0D0D", fg="#FF0000").pack(anchor="w", padx=15)

        self.feed = tk.Text(self.root, height=5, bg="#080000", fg="#FF4444",
                             font=("Courier", 8), relief="flat", state="disabled")
        self.feed.pack(fill="x", padx=15, pady=3)

        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=5)
        tk.Button(bf, text="⏹ STOP", command=self.stop,
                  font=("Courier", 9, "bold"), bg="#1a0000", fg="#FF0000",
                  relief="flat", padx=10, pady=4).pack(side="left", padx=4)
        tk.Button(bf, text="🛡️ BLOCK ALL", command=self.block_all,
                  font=("Courier", 9, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=10, pady=4).pack(side="left", padx=4)

        tk.Label(self.root, text="BrayoOS Threat Engine v1.0 • Brayo & AIRA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#220000").pack(side="bottom", pady=4)

    def draw_map(self):
        # Draw simple world outline grid
        self.canvas.create_rectangle(0, 0, 690, 280, fill="#000811", outline="")
        # Grid lines
        for x in range(0, 690, 50):
            self.canvas.create_line(x, 0, x, 280, fill="#0a0a1a", width=1)
        for y in range(0, 280, 40):
            self.canvas.create_line(0, y, 690, y, fill="#0a0a1a", width=1)
        # Continents rough shapes
        continents = [
            # North America
            [(85,80),(170,80),(175,160),(155,210),(110,220),(80,180),(70,120)],
            # South America
            [(155,220),(195,220),(210,320),(175,350),(145,300),(140,250)],
            # Europe
            [(230,80),(310,80),(320,180),(280,185),(235,160),(225,120)],
            # Africa
            [(225,185),(310,185),(320,340),(270,360),(220,300),(215,240)],
            # Asia
            [(315,65),(560,65),(570,280),(460,300),(380,260),(310,200)],
            # Australia
            [(455,305),(545,305),(550,380),(465,385),(445,345)],
        ]
        for c in continents:
            self.canvas.create_polygon(c, fill="#0d2b0d", outline="#1a3a1a", width=1)

        # City dots
        for name, x, y in CITIES:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="#003300", outline="#00FF41")
            if name == "Nairobi":
                self.canvas.create_text(x+5, y-8, text="🇰🇪", font=("Courier", 8),
                                        fill="#00FF41", anchor="w")

    def log_attack(self, msg):
        self.feed.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.feed.insert("end", f"[{ts}] {msg}\n")
        self.feed.see("end")
        self.feed.config(state="disabled")

    def draw_attack(self, src, dst, attack_type):
        sx, sy = src[1], src[2]
        dx, dy = dst[1], dst[2]
        # Draw attack line
        line = self.canvas.create_line(sx, sy, dx, dy,
                                        fill="#FF0000", width=1, dash=(3,3))
        dot = self.canvas.create_oval(dx-5, dy-5, dx+5, dy+5,
                                       fill="#FF0000", outline="#FF4444")
        self.root.after(1500, lambda: self.canvas.delete(line))
        self.root.after(1500, lambda: self.canvas.delete(dot))

    def attack_loop(self):
        blocked = 0
        countries = set()
        threat_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

        while self.running:
            src = random.choice(CITIES)
            dst = random.choice(CITIES)
            while dst == src:
                dst = random.choice(CITIES)

            attack = random.choice(ATTACK_TYPES)
            self.attack_count += 1
            blocked += random.randint(0, 1)
            countries.add(src[0])

            self.root.after(0, self.draw_attack, src, dst, attack)
            self.root.after(0, self.log_attack,
                            f"⚠️ {attack} | {src[0]} → {dst[0]}")

            self.root.after(0, self.stat_vars["ATTACKS"].set, str(self.attack_count))
            self.root.after(0, self.stat_vars["BLOCKED"].set, str(blocked))
            self.root.after(0, self.stat_vars["COUNTRIES"].set, str(len(countries)))
            lvl = threat_levels[min(3, self.attack_count // 10)]
            self.root.after(0, self.stat_vars["THREAT LVL"].set, lvl)

            time.sleep(random.uniform(0.5, 1.5))

    def stop(self):
        self.running = False
        self.log_attack("⏹ Threat monitor stopped.")

    def block_all(self):
        self.log_attack("🛡️ AIRA activating global block — all threats neutralized!")
        self.stat_vars["BLOCKED"].set(str(self.attack_count))

if __name__ == "__main__":
    root = tk.Tk()
    LiveThreatMap(root)
    root.mainloop()
