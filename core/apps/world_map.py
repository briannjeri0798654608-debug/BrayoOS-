import tkinter as tk
import threading,time,random,httpx,os
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

CITIES=[
    ("Nairobi",288,318,"🇰🇪"),("Lagos",222,298,"🇳🇬"),("Cairo",312,228,"🇪🇬"),
    ("London",242,158,"🇬🇧"),("Paris",256,168,"🇫🇷"),("Berlin",272,155,"🇩🇪"),
    ("Moscow",332,138,"🇷🇺"),("Dubai",362,238,"🇦🇪"),("Mumbai",402,262,"🇮🇳"),
    ("Beijing",462,202,"🇨🇳"),("Tokyo",512,202,"🇯🇵"),("Sydney",502,368,"🇦🇺"),
    ("New York",132,202,"🇺🇸"),("LA",92,218,"🇺🇸"),("Chicago",132,192,"🇺🇸"),
    ("Sao Paulo",188,348,"🇧🇷"),("Mexico",102,252,"🇲🇽"),("Toronto",148,188,"🇨🇦"),
    ("Singapore",462,302,"🇸🇬"),("Seoul",492,198,"🇰🇷"),("Istanbul",322,202,"🇹🇷"),
    ("Cape Town",272,378,"🇿🇦"),("Johannesburg",298,358,"🇿🇦"),("Accra",232,298,"🇬🇭"),
]

ATTACK_TYPES=["DDoS","Ransomware","Phishing","SQLi","Zero-Day","MITM","Brute Force","APT","Malware","XSS"]
USERS_ONLINE=["KE-Brayo","NG-Hacker","RU-Ghost","US-Agent","JP-Ninja","DE-Coder","BR-Silva","IN-Dev"]

class WorldMap:
    def __init__(self,root):
        self.root=root
        self.root.title("🌍 Live World Map")
        self.root.geometry("780x620")
        self.root.configure(bg=BG)
        self.running=True
        self.attacks=0
        self.users=0
        self.build_ui()
        threading.Thread(target=self.live_loop,daemon=True).start()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🌍 LIVE WORLD MAP",font=("Courier",14,"bold"),bg=BG2,fg=RED).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="Real-time attacks • Users • Threats",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.time_lbl=tk.Label(hdr,text="",font=("Courier",9),bg=BG2,fg=NEON)
        self.time_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=RED,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=10,pady=5)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("ATTACKS",RED),("USERS ONLINE",GREEN),
            ("COUNTRIES",GOLD),("THREAT LEVEL",RED)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="0")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",12,"bold"),bg=BG3,fg=color).pack(pady=2)

        # Map canvas
        self.map=tk.Canvas(self.root,width=760,height=340,bg="#000811",
                          highlightthickness=1,highlightbackground=RED)
        self.map.pack(padx=10,pady=5)
        self._draw_base_map()

        # Bottom panels
        bottom=tk.Frame(self.root,bg=BG);bottom.pack(fill="both",expand=True,padx=10,pady=5)

        # Attack feed
        left=tk.Frame(bottom,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(0,5))
        tk.Label(left,text="◈ ATTACK FEED",font=("Courier",8,"bold"),bg=BG,fg=RED).pack(anchor="w")
        self.feed=tk.Text(left,height=6,bg=BG3,fg=WHITE,font=("Courier",7),relief="flat",state="disabled")
        self.feed.pack(fill="both",expand=True)
        self.feed.tag_config("r",foreground=RED)
        self.feed.tag_config("y",foreground=GOLD)
        self.feed.tag_config("g",foreground=GREEN)

        # Users online
        right=tk.Frame(bottom,bg=BG2,width=200);right.pack(side="left",fill="y")
        right.pack_propagate(False)
        tk.Label(right,text="◈ USERS ONLINE",font=("Courier",8,"bold"),bg=BG2,fg=GREEN).pack(pady=5,padx=8,anchor="w")
        self.users_list=tk.Text(right,bg=BG2,fg=GREEN,font=("Courier",7),relief="flat",state="disabled")
        self.users_list.pack(fill="both",expand=True,padx=5)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=4)
        self.run_btn=tk.Button(bf,text="⏹ STOP",font=("Courier",9,"bold"),bg=BG3,fg=RED,
                              relief="flat",padx=10,pady=4,command=self.toggle)
        self.run_btn.pack(side="left",padx=4)
        tk.Button(bf,text="🛡 BLOCK ALL",font=("Courier",9,"bold"),bg=BG3,fg=GREEN,
                 relief="flat",padx=10,pady=4,command=self.block_all).pack(side="left",padx=4)
        tk.Label(self.root,text="BrayoOS World Map v4.5 • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def _draw_base_map(self):
        self.map.delete("base")
        # Grid
        for x in range(0,760,40):self.map.create_line(x,0,x,340,fill="#030316",tags="base")
        for y in range(0,340,30):self.map.create_line(0,y,760,y,fill="#030316",tags="base")
        # Continents (simplified)
        continents=[
            [(88,82),(172,82),(177,165),(157,215),(112,225),(82,185),(72,125)],
            [(157,225),(197,225),(212,325),(177,355),(147,305),(142,255)],
            [(232,82),(312,82),(322,185),(282,190),(237,165),(227,125)],
            [(227,190),(312,190),(322,345),(272,365),(222,305),(217,245)],
            [(317,68),(562,68),(572,285),(462,305),(382,265),(312,205)],
            [(457,308),(547,308),(552,385),(467,390),(447,348)],
        ]
        for c in continents:
            self.map.create_polygon(c,fill="#0a1a0a",outline="#0f2a0f",width=1,tags="base")
        # Cities
        for name,x,y,flag in CITIES:
            self.map.create_oval(x-4,y-4,x+4,y+4,fill="#001a00",outline=GREEN,tags="base")
            if name=="Nairobi":
                self.map.create_text(x+6,y-10,text=f"🇰🇪 {name}",fill=GREEN,font=("Courier",7),tags="base")

    def log_feed(self,msg,tag="r"):
        self.feed.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.feed.insert("end",f"[{ts}] {msg}\n",tag)
        self.feed.see("end")
        self.feed.config(state="disabled")

    def draw_attack(self,src,dst,atype):
        sx,sy=src[1],src[2]
        dx,dy=dst[1],dst[2]
        line=self.map.create_line(sx,sy,dx,dy,fill=RED,width=1,dash=(3,3))
        dot=self.map.create_oval(dx-6,dy-6,dx+6,dy+6,fill=RED,outline=GOLD)
        label=self.map.create_text(dx+10,dy-10,text=atype,fill=RED,font=("Courier",6))
        self.root.after(2000,lambda:self.map.delete(line,dot,label))

    def update_users(self):
        self.users_list.config(state="normal")
        self.users_list.delete("1.0","end")
        online=random.sample(USERS_ONLINE,min(len(USERS_ONLINE),random.randint(3,8)))
        for u in online:
            self.users_list.insert("end",f"  ⬤ {u}\n")
        self.users_list.config(state="disabled")
        self.svars["USERS ONLINE"].set(str(len(online)))

    def live_loop(self):
        countries=set()
        threat_levels=["LOW","MEDIUM","HIGH","CRITICAL"]
        while self.running:
            src=random.choice(CITIES)
            dst=random.choice(CITIES)
            while dst==src:dst=random.choice(CITIES)
            atype=random.choice(ATTACK_TYPES)
            self.attacks+=1
            countries.add(src[0])
            self.root.after(0,self.draw_attack,src,dst,atype)
            self.root.after(0,self.log_feed,f"⚠ {atype} | {src[0]} → {dst[0]}","r")
            self.root.after(0,self.svars["ATTACKS"].set,str(self.attacks))
            self.root.after(0,self.svars["COUNTRIES"].set,str(len(countries)))
            lvl=threat_levels[min(3,self.attacks//15)]
            self.root.after(0,self.svars["THREAT LEVEL"].set,lvl)
            if self.attacks%5==0:self.root.after(0,self.update_users)
            now=datetime.now().strftime("%H:%M:%S UTC")
            self.root.after(0,self.time_lbl.config,{"text":now})
            time.sleep(random.uniform(0.8,2))

    def toggle(self):
        self.running=not self.running
        self.run_btn.config(text="⏹ STOP" if self.running else "▶ START",
                           fg=RED if self.running else GREEN)
        if self.running:threading.Thread(target=self.live_loop,daemon=True).start()

    def block_all(self):
        self.log_feed("🛡 AIRA activated global shield — all attacks neutralized!","g")
        self.svars["ATTACKS"].set("0")
        self.attacks=0

if __name__=="__main__":
    root=tk.Tk();WorldMap(root);root.mainloop()
