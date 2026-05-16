import tkinter as tk
import subprocess,os,json,hashlib
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

CONFIG=os.path.expanduser("~/BrayoOS/memory/settings.json")
os.makedirs(os.path.dirname(CONFIG),exist_ok=True)

def load():
    if os.path.exists(CONFIG):
        with open(CONFIG) as f:return json.load(f)
    return {"pin":"1337","brightness":"80","language":"English",
            "owner":"Brayo","device":"Redmi 14C","font_size":"Medium"}

def save(cfg):
    with open(CONFIG,"w") as f:json.dump(cfg,f,indent=2)

class Settings:
    def __init__(self,root):
        self.root=root
        self.root.title("⚙️ Settings")
        self.root.geometry("650x580")
        self.root.configure(bg=BG)
        self.cfg=load()
        self.build_ui()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        self.back=tk.Button(hdr,text="◀",font=("Courier",14),bg=BG2,fg=BG2,relief="flat",command=self.home)
        self.back.pack(side="left",padx=10)
        self.tlbl=tk.Label(hdr,text="⚙️ SETTINGS",font=("Courier",13,"bold"),bg=BG2,fg=NEON)
        self.tlbl.pack(side="left")
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")
        self.body=tk.Frame(self.root,bg=BG)
        self.body.pack(fill="both",expand=True)
        self.home()

    def clear(self):
        for w in self.body.winfo_children():w.destroy()

    def sf(self):
        c=tk.Canvas(self.body,bg=BG,highlightthickness=0)
        sb=tk.Scrollbar(self.body,orient="vertical",command=c.yview,width=6)
        c.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y")
        c.pack(side="left",fill="both",expand=True)
        f=tk.Frame(c,bg=BG)
        c.create_window((0,0),window=f,anchor="nw")
        f.bind("<Configure>",lambda e:c.configure(scrollregion=c.bbox("all")))
        return f

    def sh(self,p,t):
        tk.Label(p,text=t,font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(10,3))

    def row(self,p,icon,title,sub,color,cmd):
        f=tk.Frame(p,bg=BG3,cursor="hand2")
        f.pack(fill="x",padx=15,pady=2)
        tk.Label(f,text=icon,font=("Courier",15),bg=BG3,fg=color).pack(side="left",padx=10,pady=8)
        m=tk.Frame(f,bg=BG3);m.pack(side="left",fill="x",expand=True,pady=6)
        tk.Label(m,text=title,font=("Courier",10,"bold"),bg=BG3,fg=WHITE,anchor="w").pack(anchor="w")
        tk.Label(m,text=sub,font=("Courier",8),bg=BG3,fg=DIM,anchor="w").pack(anchor="w")
        tk.Label(f,text="▶",font=("Courier",11),bg=BG3,fg=DIM).pack(side="right",padx=10)
        for w in [f,m]+m.winfo_children():
            w.bind("<Button-1>",lambda e,x=cmd:x())
            w.bind("<Enter>",lambda e,x=f:x.config(bg="#1a1a3a"))
            w.bind("<Leave>",lambda e,x=f:x.config(bg=BG3))

    def tog(self,p,icon,title,sub,key,color):
        f=tk.Frame(p,bg=BG3);f.pack(fill="x",padx=15,pady=2)
        tk.Label(f,text=icon,font=("Courier",15),bg=BG3,fg=color).pack(side="left",padx=10,pady=8)
        m=tk.Frame(f,bg=BG3);m.pack(side="left",fill="x",expand=True,pady=6)
        tk.Label(m,text=title,font=("Courier",10,"bold"),bg=BG3,fg=WHITE,anchor="w").pack(anchor="w")
        tk.Label(m,text=sub,font=("Courier",8),bg=BG3,fg=DIM,anchor="w").pack(anchor="w")
        v=tk.BooleanVar(value=self.cfg.get(key,False))
        def t():self.cfg[key]=v.get();save(self.cfg)
        tk.Checkbutton(f,variable=v,bg=BG3,selectcolor=PURPLE,activebackground=BG3,command=t).pack(side="right",padx=10)

    def inf(self,p,label,value,color=WHITE):
        f=tk.Frame(p,bg=BG3);f.pack(fill="x",padx=15,pady=1)
        tk.Label(f,text=label,font=("Courier",9),bg=BG3,fg=DIM,width=18,anchor="w").pack(side="left",padx=10,pady=6)
        tk.Label(f,text=value,font=("Courier",9,"bold"),bg=BG3,fg=color,anchor="w").pack(side="left")

    def go(self,title):
        self.tlbl.config(text=title)
        self.back.config(fg=PURPLE)

    def launch(self,script):
        subprocess.Popen(["python3",os.path.expanduser(f"~/BrayoOS/core/apps/{script}")],
                        env={**os.environ,"DISPLAY":":1"})

    def home(self):
        self.clear()
        self.tlbl.config(text="⚙️ SETTINGS")
        self.back.config(fg=BG2)
        f=self.sf()
        card=tk.Frame(f,bg=BG3);card.pack(fill="x",padx=15,pady=8)
        tk.Label(card,text="👤",font=("Courier",26),bg=BG3,fg=NEON).pack(side="left",padx=15,pady=8)
        i=tk.Frame(card,bg=BG3);i.pack(side="left",pady=8)
        tk.Label(i,text=self.cfg.get("owner","Brayo"),font=("Courier",13,"bold"),bg=BG3,fg=NEON).pack(anchor="w")
        tk.Label(i,text="BrayoOS Owner • Kenya 🇰🇪",font=("Courier",8),bg=BG3,fg=DIM).pack(anchor="w")
        tk.Label(i,text=self.cfg.get("device","Redmi 14C"),font=("Courier",8),bg=BG3,fg=PURPLE).pack(anchor="w")
        sections=[
            ("📶","Network & Internet","WiFi, Data, Hotspot","#44AAFF",self.network),
            ("🔔","Notifications","Alerts, Do Not Disturb","#FF8800",self.notifs),
            ("🔋","Battery","Usage, Power saving","#FFD700",self.battery),
            ("🖥️","Display","Brightness, Wallpaper, Theme","#44FFCC",self.display),
            ("🔊","Sound","Volume, Ringtone, Vibration","#FF44FF",self.sound),
            ("🔒","Security","PIN, Vault, Privacy","#FF0044",self.security),
            ("♿","Accessibility","Vision, Hearing, Touch","#88FF88",self.access),
            ("🌍","Language","Language, Keyboard","#FFAA44",self.language),
            ("💾","Storage","Files, Backup, Cache","#AAAAFF",self.storage),
            ("🤖","AIRA Settings","AI, Voice, Memory","#CC44FF",self.aira),
            ("👤","Accounts","Profile, GitHub","#44FFFF",self.accounts),
            ("📱","About BrayoOS","Version, Credits","#FFD700",self.about),
            ("🔧","Developer Options","Debug, Terminal","#FF6644",self.dev),
        ]
        for icon,title,sub,color,cmd in sections:
            self.row(f,icon,title,sub,color,cmd)
        tk.Label(f,text="BrayoOS v3.5 • Brayo & AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(pady=8)

    def network(self):
        self.clear();self.go("📶 Network")
        f=self.sf()
        self.sh(f,"CONNECTIONS")
        self.tog(f,"📶","WiFi","Wireless networks","wifi","#44AAFF")
        self.tog(f,"✈️","Airplane Mode","Disable all","airplane","#AAAAFF")
        self.tog(f,"📡","Mobile Data","Cellular data","mobile_data","#FF8800")
        self.sh(f,"NETWORK INFO")
        try:
            import socket;s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("8.8.8.8",80));ip=s.getsockname()[0];s.close()
        except:ip="Not connected"
        self.inf(f,"IP Address",ip,GREEN)
        self.inf(f,"DNS","8.8.8.8",WHITE)
        self.sh(f,"TOOLS")
        self.row(f,"📡","Network Scanner","Scan WiFi devices","#44CCFF",lambda:self.launch("network_scanner.py"))
        self.row(f,"◉","Ghost Mode","Network invisibility","#44FFCC",lambda:self.launch("ghost_mode.py"))

    def display(self):
        self.clear();self.go("🖥️ Display")
        f=self.sf()
        self.sh(f,"BRIGHTNESS")
        bf=tk.Frame(f,bg=BG3);bf.pack(fill="x",padx=15,pady=4)
        tk.Label(bf,text="☀️",font=("Courier",12),bg=BG3,fg=GOLD).pack(side="left",padx=10,pady=8)
        tk.Label(bf,text="Brightness",font=("Courier",10),bg=BG3,fg=WHITE).pack(side="left")
        bv=tk.IntVar(value=int(self.cfg.get("brightness",80)))
        def sb(v):self.cfg["brightness"]=str(int(float(v)));save(self.cfg);subprocess.run(f"termux-brightness {int(float(v))} 2>/dev/null",shell=True)
        tk.Scale(bf,from_=0,to=100,orient="horizontal",variable=bv,command=sb,bg=BG3,fg=NEON,troughcolor=BG,highlightthickness=0,length=220).pack(side="right",padx=10)
        self.sh(f,"THEME & WALLPAPER")
        self.row(f,"🎨","Theme Changer","Change OS colors","#FF44FF",lambda:self.launch("theme_changer.py"))
        self.row(f,"🖼️","Wallpaper","Change desktop wallpaper","#FFAA00",lambda:self.launch("wallpaper_changer.py"))
        self.sh(f,"FONT SIZE")
        ff=tk.Frame(f,bg=BG3);ff.pack(fill="x",padx=15,pady=4)
        tk.Label(ff,text="🔤 Font:",font=("Courier",9),bg=BG3,fg=WHITE).pack(side="left",padx=10,pady=8)
        fv=tk.StringVar(value=self.cfg.get("font_size","Medium"))
        for s in ["Small","Medium","Large"]:
            tk.Radiobutton(ff,text=s,variable=fv,value=s,bg=BG3,fg=NEON,selectcolor=PURPLE,activebackground=BG3,font=("Courier",8)).pack(side="left",padx=5)

    def security(self):
        self.clear();self.go("🔒 Security")
        f=self.sf()
        self.sh(f,"VAULTS")
        self.row(f,"🔐","DNA Vault","Encrypted + decoy vault","#FFD700",lambda:self.launch("advanced_vault.py"))
        self.row(f,"🔒","Proximity Lock","Lock when moved away","#FF0044",lambda:self.launch("proximity_lock.py"))
        self.sh(f,"CHANGE PIN")
        pf=tk.Frame(f,bg=BG3);pf.pack(fill="x",padx=15,pady=4)
        tk.Label(pf,text="Current PIN:",font=("Courier",9),bg=BG3,fg=DIM).pack(anchor="w",padx=10,pady=(8,2))
        oe=tk.Entry(pf,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat",show="*")
        oe.pack(fill="x",padx=10,ipady=5)
        tk.Label(pf,text="New PIN:",font=("Courier",9),bg=BG3,fg=DIM).pack(anchor="w",padx=10,pady=(6,2))
        ne=tk.Entry(pf,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat",show="*")
        ne.pack(fill="x",padx=10,ipady=5)
        ml=tk.Label(pf,text="",font=("Courier",8),bg=BG3,fg=GREEN);ml.pack(anchor="w",padx=10)
        def cp():
            if oe.get()==self.cfg.get("pin","1337"):
                self.cfg["pin"]=ne.get();save(self.cfg);ml.config(text="✅ PIN changed!",fg=GREEN)
            else:ml.config(text="❌ Wrong PIN",fg=RED)
        tk.Button(pf,text="Change PIN",font=("Courier",9,"bold"),bg=PURPLE,fg=WHITE,relief="flat",padx=10,pady=5,command=cp).pack(pady=6)
        self.sh(f,"PRIVACY")
        self.tog(f,"👻","Ghost Mode","Hide from scanners","ghost_mode",GREEN)
        self.tog(f,"📍","Location","Allow location","location","#44AAFF")
        self.sh(f,"TOOLS")
        self.row(f,"🔍","OSINT Suite","Intelligence tools","#CC44FF",lambda:self.launch("osint_suite.py"))
        self.row(f,"💀","Dark Web Monitor","Breach detection","#FF0000",lambda:self.launch("dark_web_monitor.py"))

    def access(self):
        self.clear();self.go("♿ Accessibility")
        f=self.sf()
        self.sh(f,"VISION")
        self.tog(f,"🔍","Large Text","Bigger text size","large_text","#88FF88")
        self.tog(f,"🌑","High Contrast","Stronger colors","high_contrast",WHITE)
        self.tog(f,"💡","Screen Reader","Read screen aloud","screen_reader","#44FFCC")
        self.sh(f,"HEARING")
        self.tog(f,"🔊","Mono Audio","Combine channels","mono_audio","#FF44FF")
        self.tog(f,"📳","Vibration Alerts","Vibrate instead of sound","vibration","#AAAAFF")
        self.sh(f,"INTERACTION")
        self.tog(f,"✋","Touch Hold Delay","Adjust long press","touch_delay","#FFAA44")
        self.sh(f,"AIRA ASSIST")
        self.row(f,"🤖","AIRA Voice","Hands-free AI","#CC44FF",lambda:self.launch("aria_voice.py"))

    def sound(self):
        self.clear();self.go("🔊 Sound")
        f=self.sf()
        self.sh(f,"VOLUME")
        for icon,label,key in [("🔔","Ringtone","ring"),("🎵","Media","music"),("📳","Alarm","alarm")]:
            vf=tk.Frame(f,bg=BG3);vf.pack(fill="x",padx=15,pady=3)
            tk.Label(vf,text=icon,font=("Courier",12),bg=BG3,fg=NEON).pack(side="left",padx=10,pady=6)
            tk.Label(vf,text=label,font=("Courier",9),bg=BG3,fg=WHITE,width=10,anchor="w").pack(side="left")
            v=tk.IntVar(value=70)
            def sv(val,k=key):subprocess.run(f"termux-volume {k} {int(float(val))} 2>/dev/null",shell=True)
            tk.Scale(vf,from_=0,to=100,orient="horizontal",variable=v,command=sv,bg=BG3,fg=NEON,troughcolor=BG,highlightthickness=0,length=230).pack(side="right",padx=10)
        self.sh(f,"MODES")
        self.tog(f,"🔕","Silent Mode","Mute all","silent_mode",RED)
        self.tog(f,"📳","Vibrate on Ring","Haptic feedback","vibrate_ring","#AAAAFF")

    def battery(self):
        self.clear();self.go("🔋 Battery")
        f=self.sf()
        self.sh(f,"STATUS")
        try:
            import json as j
            r=subprocess.check_output("termux-battery-status 2>/dev/null",shell=True,timeout=3).decode()
            d=j.loads(r);pct=d.get("percentage",0);status=d.get("status","?");temp=d.get("temperature",0)
        except:pct=50;status="Unknown";temp=0
        bf=tk.Frame(f,bg=BG3);bf.pack(fill="x",padx=15,pady=8)
        col=RED if pct<20 else GOLD if pct<50 else GREEN
        tk.Label(bf,text="🔋",font=("Courier",32),bg=BG3,fg=col).pack(side="left",padx=15,pady=8)
        bi=tk.Frame(bf,bg=BG3);bi.pack(side="left",pady=8)
        tk.Label(bi,text=f"{pct}%",font=("Courier",22,"bold"),bg=BG3,fg=col).pack(anchor="w")
        tk.Label(bi,text=f"Status: {status}",font=("Courier",9),bg=BG3,fg=WHITE).pack(anchor="w")
        tk.Label(bi,text=f"Temp: {temp}°C",font=("Courier",9),bg=BG3,fg=WHITE).pack(anchor="w")
        self.sh(f,"POWER")
        self.tog(f,"⚡","Battery Saver","Save power","battery_saver",GOLD)
        self.tog(f,"🌙","Adaptive Battery","Learn usage","adaptive",GREEN)
        self.row(f,"▲","Overclock","Boost CPU performance","#FF4444",lambda:self.launch("overclock_dashboard.py"))

    def notifs(self):
        self.clear();self.go("🔔 Notifications")
        f=self.sf()
        self.sh(f,"GENERAL")
        self.tog(f,"🔔","All Notifications","Enable alerts","notifications",NEON)
        self.tog(f,"🌙","Do Not Disturb","Block interruptions","dnd","#AAAAFF")
        self.sh(f,"BRAYOOS ALERTS")
        self.tog(f,"🚨","Security Alerts","Threat alerts","security_alerts",RED)
        self.tog(f,"🤖","AIRA Messages","AI notifications","aira_notifs",NEON)
        self.tog(f,"💀","Dark Web Alerts","Breach alerts","darkweb_alerts","#FF0000")
        self.tog(f,"📡","Network Alerts","New device alerts","network_alerts","#44AAFF")

    def language(self):
        self.clear();self.go("🌍 Language")
        f=self.sf()
        self.sh(f,"LANGUAGE")
        lf=tk.Frame(f,bg=BG3);lf.pack(fill="x",padx=15,pady=4)
        tk.Label(lf,text="🌍 Language:",font=("Courier",10),bg=BG3,fg=WHITE).pack(side="left",padx=10,pady=8)
        lv=tk.StringVar(value=self.cfg.get("language","English"))
        def sl(*a):self.cfg["language"]=lv.get();save(self.cfg)
        lv.trace("w",sl)
        tk.OptionMenu(lf,lv,"English","Swahili","French","Spanish","Arabic").pack(side="left",padx=10)
        self.sh(f,"KEYBOARD")
        self.tog(f,"⌨️","Auto Correct","Fix mistakes","autocorrect",GREEN)
        self.tog(f,"💡","Word Suggestions","Predictions","suggestions",NEON)
        self.tog(f,"📳","Key Vibration","Haptic keys","key_vibrate","#AAAAFF")

    def storage(self):
        self.clear();self.go("💾 Storage")
        f=self.sf()
        self.sh(f,"USAGE")
        try:
            s=os.statvfs(os.path.expanduser("~"))
            total=s.f_blocks*s.f_frsize//1024//1024
            free=s.f_bfree*s.f_frsize//1024//1024
            used=total-free;pct=int(used*100/total) if total>0 else 0
        except:total=used=free=pct=0
        self.inf(f,"Total",f"{total}MB",WHITE)
        self.inf(f,"Used",f"{used}MB",RED if pct>80 else GOLD)
        self.inf(f,"Free",f"{free}MB",GREEN)
        self.inf(f,"BrayoOS Apps",f"{len(os.listdir(os.path.expanduser('~/BrayoOS/core/apps/')))} files",NEON)
        self.sh(f,"ACTIONS")
        self.row(f,"💾","Backup Now","Save to GitHub","#AAFFAA",lambda:self.launch("backup.py"))
        tk.Button(f,text="🗑 Clean Cache",font=("Courier",10,"bold"),bg=BG3,fg=RED,relief="flat",padx=12,pady=6,
                 command=lambda:subprocess.run("find ~/BrayoOS -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null",shell=True)
                 ).pack(padx=15,pady=5,anchor="w")

    def aira(self):
        self.clear();self.go("🤖 AIRA")
        f=self.sf()
        self.sh(f,"IDENTITY")
        self.inf(f,"Name","AIRA",NEON)
        self.inf(f,"Model","LLaMA 3.3 70B",GREEN)
        self.inf(f,"Provider","Groq API",WHITE)
        key=os.environ.get("GROQ_API_KEY","")
        self.inf(f,"API Key","✅ Set" if key else "❌ Not set",GREEN if key else RED)
        self.sh(f,"FEATURES")
        self.tog(f,"🔊","Voice Output","AIRA speaks","aira_voice",NEON)
        self.tog(f,"💾","Memory","Remember chats","aira_memory",GREEN)
        self.tog(f,"⚡","Auto-Tasks","Execute commands","aira_auto",PURPLE)
        self.sh(f,"OPEN AIRA")
        self.row(f,"★","AIRA Voice Chat","Full AI chat","#FF44FF",lambda:self.launch("aria_voice.py"))
        self.row(f,"🤖","AIRA Auto-Tasks","Command AI","#CC44FF",lambda:self.launch("aira_tasks.py"))
        self.row(f,"🧠","Neural Core","Pattern learning","#CC44FF",lambda:self.launch("aria_neural_core.py"))

    def accounts(self):
        self.clear();self.go("👤 Accounts")
        f=self.sf()
        self.sh(f,"OWNER")
        pf=tk.Frame(f,bg=BG3);pf.pack(fill="x",padx=15,pady=8)
        tk.Label(pf,text="👤",font=("Courier",26),bg=BG3,fg=NEON).pack(side="left",padx=15,pady=8)
        pi=tk.Frame(pf,bg=BG3);pi.pack(side="left",pady=8)
        nv=tk.StringVar(value=self.cfg.get("owner","Brayo"))
        tk.Label(pi,text="Name:",font=("Courier",8),bg=BG3,fg=DIM).pack(anchor="w")
        tk.Entry(pi,textvariable=nv,font=("Courier",11),bg=BG,fg=NEON,insertbackground=NEON,relief="flat").pack(anchor="w",ipady=4)
        def sn():self.cfg["owner"]=nv.get();save(self.cfg)
        tk.Button(pi,text="Save",font=("Courier",8,"bold"),bg=PURPLE,fg=WHITE,relief="flat",padx=8,pady=3,command=sn).pack(anchor="w",pady=4)
        self.sh(f,"CONNECTED")
        self.inf(f,"GitHub","briannjeri0798654608-debug",GREEN)
        self.inf(f,"Groq AI","✅ Connected" if os.environ.get("GROQ_API_KEY") else "❌ Not set",GREEN if os.environ.get("GROQ_API_KEY") else RED)

    def about(self):
        self.clear();self.go("📱 About")
        f=self.sf()
        tk.Label(f,text="◈",font=("Courier",36),bg=BG,fg=NEON).pack(pady=5)
        tk.Label(f,text="BrayoOS",font=("Courier",20,"bold"),bg=BG,fg=NEON).pack()
        tk.Label(f,text="Two minds. One OS. Built Different. 🇰🇪",font=("Courier",8),bg=BG,fg=GOLD).pack(pady=3)
        self.sh(f,"VERSION")
        self.inf(f,"Version","BrayoOS v3.5",NEON)
        self.inf(f,"Build",datetime.now().strftime("%Y-%m-%d"),WHITE)
        self.inf(f,"Device","Redmi 14C (pond)",WHITE)
        self.inf(f,"Platform","Termux + VNC",WHITE)
        self.inf(f,"Apps",f"{len(os.listdir(os.path.expanduser('~/BrayoOS/core/apps/')))} installed",GREEN)
        self.inf(f,"License","GPL-3.0",GOLD)
        self.sh(f,"CREDITS")
        self.inf(f,"Built by","Brayo 🇰🇪",NEON)
        self.inf(f,"AI Partner","AIRA (Claude)",NEON)
        self.inf(f,"Country","Kenya, Africa",GOLD)
        self.inf(f,"Copyright","© 2026 Brayo",WHITE)
        self.row(f,"📖","Our Story","The full BrayoOS story","#FFD700",lambda:self.launch("our_story.py"))

    def dev(self):
        self.clear();self.go("🔧 Developer")
        f=self.sf()
        tk.Label(f,text="⚠️ Advanced options",font=("Courier",8),bg=BG,fg=GOLD).pack(anchor="w",padx=15,pady=5)
        self.sh(f,"DEBUG")
        self.tog(f,"🐛","Debug Mode","Show error logs","debug_mode","#FF8800")
        self.sh(f,"TOOLS")
        self.row(f,"📊","System Monitor","Live stats","#44FF88",lambda:self.launch("system_monitor.py"))
        self.row(f,"🧬","Self-Healing","Check files","#44FF88",lambda:self.launch("self_healing.py"))
        self.row(f,"🔄","Updater","Check updates","#44FF44",lambda:self.launch("brayos_updater.py"))
        self.sh(f,"GITHUB")
        tk.Button(f,text="☁️ Push to GitHub",font=("Courier",10,"bold"),bg=BG3,fg=GREEN,relief="flat",padx=12,pady=6,
                 command=lambda:subprocess.Popen('cd ~/BrayoOS && git add -A && git commit -m "Dev push" && git push origin main',shell=True)
                 ).pack(padx=15,pady=5,anchor="w")
        self.sh(f,"RESTART")
        tk.Button(f,text="🔄 Restart BrayoOS",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,relief="flat",padx=12,pady=6,
                 command=lambda:subprocess.Popen("pkill -f desktop.py;sleep 1;DISPLAY=:1 python3 ~/BrayoOS/core/desktop.py &",shell=True)
                 ).pack(padx=15,pady=5,anchor="w")
        tk.Button(f,text,"⏹ Stop All",font=("Courier",10,"bold"),bg=BG3,fg=RED,relief="flat",padx=12,pady=6,
                 command=lambda:subprocess.Popen("pkill -f python3",shell=True)
                 ).pack(padx=15,pady=5,anchor="w")

    def bluetooth(self):pass

if __name__=="__main__":
    root=tk.Tk()
    Settings(root)
    root.mainloop()
