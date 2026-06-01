import tkinter as tk
import threading,time,random,httpx,os,subprocess
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

CITIES=[
    ("Nairobi",294,318,"🇰🇪",True),
    ("Lagos",228,295,"🇳🇬",False),
    ("Cairo",318,225,"🇪🇬",False),
    ("London",248,155,"🇬🇧",False),
    ("Paris",260,165,"🇫🇷",False),
    ("Moscow",338,135,"🇷🇺",False),
    ("Dubai",368,235,"🇦🇪",False),
    ("Mumbai",408,258,"🇮🇳",False),
    ("Beijing",468,198,"🇨🇳",False),
    ("Tokyo",518,198,"🇯🇵",False),
    ("Sydney",508,365,"🇦🇺",False),
    ("New York",138,198,"🇺🇸",False),
    ("LA",95,215,"🇺🇸",False),
    ("Sao Paulo",192,345,"🇧🇷",False),
    ("Singapore",468,298,"🇸🇬",False),
    ("Istanbul",328,198,"🇹🇷",False),
    ("Johannesburg",300,355,"🇿🇦",False),
    ("Berlin",278,152,"🇩🇪",False),
    ("Toronto",152,185,"🇨🇦",False),
    ("Seoul",498,195,"🇰🇷",False),
]

ATTACK_TYPES=[
    ("DDoS",RED),("Ransomware","#FF6600"),("Phishing",GOLD),
    ("Zero-Day",RED),("MITM",NEON),("Brute Force","#FF8800"),
    ("APT",RED),("Malware","#FF4400"),("SQLi",GOLD),("XSS",NEON),
]

class ThreatMap:
    def __init__(self,root):
        self.root=root
        self.root.title("🌍 BrayoOS Live Threat Map")
        self.root.geometry("800x600")
        self.root.configure(bg=BG)
        self.running=True
        self.attacks=0
        self.blocked=0
        self.build_ui()
        threading.Thread(target=self.threat_loop,daemon=True).start()
        threading.Thread(target=self.pulse_loop,daemon=True).start()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🌍 LIVE THREAT MAP",font=("Courier",14,"bold"),bg=BG2,fg=RED).pack(side="left",padx=12,pady=10)
        self.time_lbl=tk.Label(hdr,text="",font=("Courier",9),bg=BG2,fg=NEON)
        self.time_lbl.pack(side="right",padx=12)
        self.threat_lbl=tk.Label(hdr,text="THREAT: LOW",font=("Courier",9,"bold"),bg=BG2,fg=GREEN)
        self.threat_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=RED,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=10,pady=5)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("ATTACKS",RED),("BLOCKED",GREEN),
            ("COUNTRIES",GOLD),("THREAT LEVEL",RED)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="0")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",12,"bold"),bg=BG3,fg=color).pack(pady=2)

        # Map
        self.map=tk.Canvas(self.root,width=780,height=330,
                          bg="#000811",highlightthickness=1,
                          highlightbackground=RED)
        self.map.pack(padx=10,pady=5)
        self._draw_map()

        # Bottom
        bot=tk.Frame(self.root,bg=BG);bot.pack(fill="both",expand=True,padx=10,pady=5)
        left=tk.Frame(bot,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(0,5))
        tk.Label(left,text="◈ LIVE ATTACK FEED",font=("Courier",8,"bold"),bg=BG,fg=RED).pack(anchor="w")
        self.feed=tk.Text(left,height=5,bg=BG3,fg=WHITE,font=("Courier",7),relief="flat",state="disabled")
        self.feed.pack(fill="both",expand=True)
        self.feed.tag_config("r",foreground=RED)
        self.feed.tag_config("g",foreground=GREEN)
        self.feed.tag_config("y",foreground=GOLD)

        right=tk.Frame(bot,bg=BG2,width=180);right.pack(side="left",fill="y")
        right.pack_propagate(False)
        tk.Label(right,text="◈ ATTACK TYPES",font=("Courier",7,"bold"),bg=BG2,fg=RED).pack(pady=5,padx=8,anchor="w")
        for atype,color in ATTACK_TYPES[:6]:
            f=tk.Frame(right,bg=BG2);f.pack(fill="x",padx=8,pady=1)
            tk.Label(f,text="●",font=("Courier",8),bg=BG2,fg=color).pack(side="left")
            tk.Label(f,text=atype,font=("Courier",7),bg=BG2,fg=WHITE).pack(side="left",padx=4)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=4)
        self.toggle_btn=tk.Button(bf,text="⏹ STOP",font=("Courier",9,"bold"),
                                   bg=BG3,fg=RED,relief="flat",padx=10,pady=4,
                                   command=self.toggle)
        self.toggle_btn.pack(side="left",padx=4)
        tk.Button(bf,text="🛡 BLOCK ALL",font=("Courier",9,"bold"),bg=BG3,fg=GREEN,
                 relief="flat",padx=10,pady=4,command=self.block_all).pack(side="left",padx=4)
        tk.Label(self.root,text="BrayoOS Threat Map v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def _draw_map(self):
        self.map.delete("base")
        for x in range(0,780,35):
            self.map.create_line(x,0,x,330,fill="#020218",tags="base")
        for y in range(0,330,25):
            self.map.create_line(0,y,780,y,fill="#020218",tags="base")
        continents=[
            [(90,78),(175,78),(180,160),(160,210),(115,220),(85,180),(75,120)],
            [(160,220),(200,220),(215,320),(180,350),(150,300),(145,250)],
            [(235,78),(315,78),(325,182),(285,188),(240,162),(230,120)],
            [(230,188),(318,188),(325,342),(275,362),(225,302),(220,242)],
            [(320,65),(565,65),(575,282),(465,302),(385,262),(315,202)],
            [(460,305),(550,305),(555,382),(470,388),(450,345)],
        ]
        for c in continents:
            self.map.create_polygon(c,fill="#0a1a0a",outline="#0f2a0f",width=1,tags="base")
        for name,x,y,flag,is_home in CITIES:
            color=GREEN if is_home else "#003300"
            outline=GREEN if is_home else "#001100"
            size=6 if is_home else 4
            self.map.create_oval(x-size,y-size,x+size,y+size,
                               fill=color,outline=outline,tags="base")
            if is_home:
                self.map.create_text(x+8,y-8,text=f"🇰🇪 Nairobi",
                                   fill=GREEN,font=("Courier",7,"bold"),tags="base")

    def log_feed(self,msg,tag="r"):
        self.feed.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.feed.insert("end",f"[{ts}] {msg}\n",tag)
        self.feed.see("end")
        self.feed.config(state="disabled")

    def draw_attack(self,src,dst,atype,color):
        sx,sy=src[1],src[2]
        dx,dy=dst[1],dst[2]
        line=self.map.create_line(sx,sy,dx,dy,fill=color,width=1,dash=(4,4))
        dot=self.map.create_oval(dx-5,dy-5,dx+5,dy+5,fill=color,outline=GOLD)
        txt=self.map.create_text(dx+8,dy-8,text=atype[:8],
                                fill=color,font=("Courier",6))
        self.root.after(2500,lambda:self.map.delete(line,dot,txt))

    def threat_loop(self):
        countries=set()
        while self.running:
            src=random.choice(CITIES)
            dst=random.choice(CITIES)
            while dst==src:dst=random.choice(CITIES)
            atype,color=random.choice(ATTACK_TYPES)
            self.attacks+=1
            if random.random()<0.4:self.blocked+=1
            countries.add(src[0])
            lvl="CRITICAL" if self.attacks>50 else "HIGH" if self.attacks>25 else "MEDIUM" if self.attacks>10 else "LOW"
            lvl_col=RED if lvl in["CRITICAL","HIGH"] else GOLD if lvl=="MEDIUM" else GREEN
            self.root.after(0,self.draw_attack,src,dst,atype,color)
            self.root.after(0,self.log_feed,f"⚠ {atype} | {src[0]} → {dst[0]}","r")
            self.root.after(0,self.svars["ATTACKS"].set,str(self.attacks))
            self.root.after(0,self.svars["BLOCKED"].set,str(self.blocked))
            self.root.after(0,self.svars["COUNTRIES"].set,str(len(countries)))
            self.root.after(0,self.svars["THREAT LEVEL"].set,lvl)
            self.root.after(0,self.threat_lbl.config,{"text":f"THREAT: {lvl}","fg":lvl_col})
            self.root.after(0,self.time_lbl.config,
                           {"text":datetime.now().strftime("%H:%M:%S UTC")})
            time.sleep(random.uniform(0.5,1.5))

    def pulse_loop(self):
        while self.running:
            for city in CITIES:
                if random.random()<0.1:
                    x,y=city[1],city[2]
                    dot=self.map.create_oval(x-8,y-8,x+8,y+8,
                                           outline=RED,width=1)
                    self.root.after(300,lambda d=dot:self.map.delete(d))
            time.sleep(0.3)

    def toggle(self):
        self.running=not self.running
        self.toggle_btn.config(
            text="⏹ STOP" if self.running else "▶ START",
            fg=RED if self.running else GREEN)
        if self.running:
            threading.Thread(target=self.threat_loop,daemon=True).start()

    def block_all(self):
        self.log_feed("🛡 AIRA shield activated — all attacks neutralized!","g")
        self.blocked+=self.attacks
        self.svars["BLOCKED"].set(str(self.blocked))
        self.threat_lbl.config(text="THREAT: NEUTRALIZED",fg=GREEN)

if __name__=="__main__":
    root=tk.Tk();ThreatMap(root);root.mainloop()
