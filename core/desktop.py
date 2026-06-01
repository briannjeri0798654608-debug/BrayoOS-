import tkinter as tk
import subprocess,os,threading,time,json,random
from datetime import datetime

# ── THEME v5.0 ─────────────────────────────────────────────────
BG="#080810";BG2="#0D0D1A";BG3="#12122A";BG4="#0A0A18"
PURPLE="#9D00FF";NEON="#CC44FF";NEON2="#FF44FF"
GREEN="#44FF88";CYAN="#44FFFF";AMBER="#FFB300"
RED="#FF0044";WHITE="#E0E0FF";DIM="#444466"
PURPLE2="#6A0DAD";PURPLE3="#3D0066";PURPLE4="#1A0033"

# ── PATHS ──────────────────────────────────────────────────────
BASE=os.path.expanduser("~/BrayoOS")
APPS_DIR=os.path.join(BASE,"core","apps")
MEM_DIR=os.path.join(BASE,"memory")
STATS=os.path.join(MEM_DIR,"stats.json")
os.makedirs(MEM_DIR,exist_ok=True)

# ── APPS v5.0 ──────────────────────────────────────────────────
APPS=[
    ("★","AIRA AI","aria_voice.py",NEON2),
    ("⚡","Code Gen","code_generator.py","#CC44FF"),
    ("🚀","Speed Test","speed_test.py","#44FF88"),
    ("⏰","Alarms","alarm_system.py","#FFD700"),
    ("📱","QR Codes","qr_generator.py","#CC44FF"),
    ("📝","Smart Notes","smart_notes.py","#44FFFF"),

    ("🔐","Sec Msg","secure_messenger.py","#44FFFF"),
    ("📊","Dashboard","system_dashboard.py","#44FF88"),

    ("◈","Neural","aria_neural_core.py",NEON),
    ("🤖","Auto AIRA","aira_autonomous.py",NEON),
    ("🎯","AIRA Tasks","aira_tasks.py",NEON),
    ("🌐","Web Agent","aira_web_agent.py","#00AAFF"),
    ("🎨","AI Images","ai_image_gen.py",NEON2),
    ("📰","AI News","ai_news.py",AMBER),
    ("🧠","Habits","habit_learner.py",NEON),
    ("◉","Ghost Mode","ghost_mode.py",CYAN),
    ("▣","DNA Vault","dna_vault.py",AMBER),
    ("🔮","Quantum","quantum_vault.py",CYAN),
    ("🔐","Adv Vault","advanced_vault.py",AMBER),
    ("◎","Signal","signal_interceptor.py","#44CCFF"),
    ("◆","Identity","identity_switcher.py","#FF6644"),
    ("●","Threats","live_threat_map.py",RED),
    ("☠","Dark Web","dark_web_monitor.py",RED),
    ("🕷","Dark Browse","dark_web_browser.py",RED),
    ("🔍","OSINT","osint_suite.py","#CC44FF"),
    ("🔥","Firewall","firewall.py",RED),
    ("🌐","VPN","vpn_engine.py",GREEN),
    ("📡","eSIM","esim_manager.py",CYAN),
    ("📶","WiFi Pass","wifi_passwords.py","#44AAFF"),
    ("🎯","IP Grabber","ip_grabber.py",RED),
    ("📡","Net Scan","network_scanner.py",CYAN),
    ("📷","Surveil","surveillance.py",RED),
    ("🔑","Pass Mgr","password_manager.py",AMBER),
    ("🔐","Encryptor","file_encryptor.py",CYAN),
    ("👁","Face Lock","face_lock.py","#44FFCC"),
    ("📶","WiFi Audit","wifi_auditor.py","#44AAFF"),
    ("🧬","Lie Detect","lie_detector.py",NEON),
    ("▲","Overclock","overclock_dashboard.py",RED),
    ("📊","Sys Mon","system_monitor.py",GREEN),
    ("🧬","Self-Heal","self_healing.py",GREEN),
    ("♟","Users","user_manager.py","#AAAAFF"),
    ("↻","Updater","brayos_updater.py",GREEN),
    ("☁","Cloud","brayos_cloud.py",CYAN),
    ("🌙","Dream Mode","dream_mode.py",PURPLE),
    ("🎨","Themes","theme_changer.py",NEON2),
    ("🛸","Satellites","satellite_tracker.py",CYAN),
    ("🌍","World Map","world_map.py",RED),
    ("📱","Phone Ctrl","phone_controller.py",NEON),
    ("💀","Hack Term","hack_terminal.py",GREEN),
    ("💀","Hacker RPG","hacker_rpg.py",GREEN),
    ("📱","Social Hub","social_hub.py","#1DA1F2"),
    ("💰","Crypto Wallet","crypto_wallet.py",AMBER),
    ("🎙","Voice Cmd","voice_commands.py",NEON2),
    ("⊗","Browser","browser.py","#44AAFF"),
    ("♫","Music","music_player.py","#FF44AA"),
    ("☁","Weather","weather.py","#88AAFF"),
    ("¤","Crypto","crypto.py",AMBER),
    ("▨","News","news.py",AMBER),
    ("▤","Files","file_manager.py",AMBER),
    ("▧","Editor","editor.py","#88FFAA"),
    ("#","Calc","calculator.py","#FFFF44"),
    ("◷","Clock","clock.py",CYAN),
    ("✓","Tasks","tasks.py",GREEN),
    ("▯","SMS","sms.py",NEON2),
    ("♛","Contacts","contacts.py","#FFAAFF"),
    ("▦","Wallpaper","wallpaper_changer.py",AMBER),
    ("◫","App Store","app_store.py","#00AAFF"),
    ("▪","Backup","backup.py","#AAFFAA"),
    ("▶","Our Story","our_story.py",AMBER),
    ("✦","Settings","settings.py","#CCCCFF"),
]

CATS={
    "ALL":None,
    "AI":["aria_voice.py","aria_neural_core.py","aira_autonomous.py",
          "aira_tasks.py","aira_web_agent.py","ai_image_gen.py",
          "ai_news.py","habit_learner.py"],
    "SECURITY":["ghost_mode.py","dna_vault.py","quantum_vault.py",
                "signal_interceptor.py","identity_switcher.py",
                "live_threat_map.py","dark_web_monitor.py","firewall.py",
                "vpn_engine.py","proximity_lock.py","advanced_vault.py",
                "face_lock.py","lie_detector.py"],
    "HACK":["hack_terminal.py","dark_web_browser.py","hacker_rpg.py",
            "network_scanner.py","ip_grabber.py","wifi_passwords.py",
            "wifi_auditor.py","osint_suite.py","signal_interceptor.py"],
    "NETWORK":["vpn_engine.py","esim_manager.py","satellite_tracker.py",
               "network_scanner.py","ip_grabber.py"],
    "SYSTEM":["overclock_dashboard.py","self_healing.py","brayos_updater.py",
              "user_manager.py","settings.py","backup.py","system_monitor.py",
              "dream_mode.py","brayos_cloud.py","theme_changer.py"],
    "TOOLS":["calculator.py","clock.py","editor.py","tasks.py",
             "wallpaper_changer.py","app_store.py","file_encryptor.py",
             "password_manager.py","voice_commands.py"],
    "MEDIA":["music_player.py","browser.py","weather.py","crypto.py",
             "world_map.py","satellite_tracker.py","ai_news.py",
             "social_hub.py","crypto_wallet.py"],
    "PERSONAL":["sms.py","contacts.py","file_manager.py","our_story.py",
                "phone_controller.py","surveillance.py"],
}

def load_stats():
    try:
        with open(STATS) as f:return json.load(f)
    except:return {"launches":0,"most_used":{},"last_boot":str(datetime.now())}

def save_stats(s):
    try:
        with open(STATS,"w") as f:json.dump(s,f,indent=2)
    except:pass

class BootScreen:
    def __init__(self,root,on_done):
        self.root=root
        self.on_done=on_done
        self.frame=tk.Frame(root,bg="#000000")
        self.frame.place(relwidth=1,relheight=1)
        self.canvas=tk.Canvas(self.frame,bg="#000000",highlightthickness=0)
        self.canvas.pack(fill="both",expand=True)
        self.y=60
        self.idx=0
        self.lines=[
            ("◈ BrayoOS v5.0 — Initializing kernel...",PURPLE),
            ("  [OK] Loading Python 3.13 runtime",GREEN),
            ("  [OK] Mounting BrayoOS filesystem",GREEN),
            ("  [OK] Starting AIRA neural engine...",NEON),
            ("  [OK] Loading 63 applications",GREEN),
            ("  [OK] Decrypting DNA Vault",AMBER),
            ("  [OK] Arming Ghost Mode",CYAN),
            ("  [OK] Connecting Groq AI (LLaMA 3.3 70B)",NEON),
            ("  [OK] Calibrating threat detection",RED),
            ("  [OK] Initializing satellite tracker",CYAN),
            ("  [OK] Loading BrayoOS v5.0 theme",PURPLE),
            ("  [OK] Two minds. One OS. Built Different.",GREEN),
            ("",""),
            ("  ██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗",PURPLE),
            ("  ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝",PURPLE),
            ("  ██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗",NEON),
            ("  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═╝   ╚═════╝  ╚═════╝  ╚══════╝",NEON),
            ("",""),
            ("  v5.0 — Kenya 🇰🇪 — Built by Brayo & AIRA",AMBER),
            ("  Welcome back, Brayo. Systems ready.",GREEN),
        ]
        self._type_next()

    def _type_next(self):
        if self.idx<len(self.lines):
            text,color=self.lines[self.idx]
            if text:
                self.canvas.create_text(
                    40,self.y,text=text,fill=color,
                    font=("Courier",10),anchor="w")
                self.y+=22
            else:
                self.y+=8
            self.idx+=1
            delay=60 if "██" in text else 120
            self.root.after(delay,self._type_next)
        else:
            self.root.after(800,self._finish)

    def _finish(self):
        self.frame.destroy()
        self.on_done()

class NotifCenter:
    def __init__(self,root):
        self.root=root
        self.notifs=[]
        self.win=None

    def add(self,title,msg,color=NEON):
        ts=datetime.now().strftime("%H:%M")
        self.notifs.insert(0,{"title":title,"msg":msg,"color":color,"time":ts})
        if self.win and self.win.winfo_exists():
            self._render()

    def toggle(self):
        if self.win and self.win.winfo_exists():
            self.win.destroy();self.win=None;return
        self.win=tk.Toplevel(self.root)
        self.win.title("Notifications")
        self.win.geometry("300x400+900+50")
        self.win.configure(bg=BG2)
        self.win.attributes("-topmost",True)
        hdr=tk.Frame(self.win,bg=BG3)
        hdr.pack(fill="x",padx=6,pady=6)
        tk.Label(hdr,text="🔔 NOTIFICATIONS",font=("Courier",10,"bold"),bg=BG3,fg=NEON).pack(side="left",padx=8,pady=6)
        tk.Button(hdr,text="CLEAR",font=("Courier",8),bg=PURPLE3,fg=WHITE,
                 relief="flat",command=self.clear).pack(side="right",padx=6,pady=4)
        self.notif_frame=tk.Frame(self.win,bg=BG2)
        self.notif_frame.pack(fill="both",expand=True,padx=6)
        self._render()

    def _render(self):
        if not self.win:return
        for w in self.notif_frame.winfo_children():w.destroy()
        if not self.notifs:
            tk.Label(self.notif_frame,text="No notifications",
                    font=("Courier",9),bg=BG2,fg=DIM).pack(pady=20)
            return
        for n in self.notifs[:10]:
            card=tk.Frame(self.notif_frame,bg=BG3);card.pack(fill="x",pady=3)
            tk.Frame(card,bg=n["color"],width=3).pack(side="left",fill="y")
            c=tk.Frame(card,bg=BG3);c.pack(side="left",fill="x",expand=True,padx=6,pady=5)
            tk.Label(c,text=n["title"],font=("Courier",9,"bold"),bg=BG3,fg=n["color"]).pack(anchor="w")
            tk.Label(c,text=n["msg"],font=("Courier",8),bg=BG3,fg=WHITE,wraplength=200).pack(anchor="w")
            tk.Label(card,text=n["time"],font=("Courier",6),bg=BG3,fg=DIM).pack(side="right",padx=4,anchor="n",pady=4)

    def clear(self):
        self.notifs=[]
        self._render()

class WidgetBar:
    def __init__(self,parent,root):
        self.root=root
        self.frame=tk.Frame(parent,bg=BG4,height=82)
        self.frame.pack(fill="x")
        self.frame.pack_propagate(False)
        tk.Frame(self.frame,bg=PURPLE3,height=1).pack(fill="x")
        inner=tk.Frame(self.frame,bg=BG4)
        inner.pack(fill="both",expand=True,padx=8,pady=4)

        # Clock widget
        cw=self._widget(inner,PURPLE)
        self.clock_lbl=tk.Label(cw,text="",font=("Courier",15,"bold"),bg=BG3,fg=NEON)
        self.clock_lbl.pack(pady=(4,0))
        self.date_lbl=tk.Label(cw,text="",font=("Courier",7),bg=BG3,fg=DIM)
        self.date_lbl.pack(pady=(0,4))

        # AIRA widget
        aw=self._widget(inner,NEON2)
        tk.Label(aw,text="AIRA v5.0",font=("Courier",8,"bold"),bg=BG3,fg=NEON2).pack(pady=(4,0))
        self.aira_dot=tk.Label(aw,text="◉ ONLINE",font=("Courier",7),bg=BG3,fg=GREEN)
        self.aira_dot.pack()
        self.aira_msg=tk.Label(aw,text="Watching over you",font=("Courier",6),bg=BG3,fg=DIM,wraplength=120)
        self.aira_msg.pack(pady=(0,4))

        # Battery widget
        bw=self._widget(inner,AMBER)
        tk.Label(bw,text="BATTERY",font=("Courier",7,"bold"),bg=BG3,fg=AMBER).pack(pady=(4,0))
        self.bat_lbl=tk.Label(bw,text="--",font=("Courier",14,"bold"),bg=BG3,fg=AMBER)
        self.bat_lbl.pack()
        self.bat_bar=tk.Canvas(bw,width=100,height=6,bg=BG3,highlightthickness=0)
        self.bat_bar.pack(pady=(0,4))

        # Stats widget
        sw=self._widget(inner,GREEN)
        tk.Label(sw,text="BRAYOOS",font=("Courier",7,"bold"),bg=BG3,fg=GREEN).pack(pady=(4,0))
        self.apps_lbl=tk.Label(sw,text=f"{len(APPS)} apps",font=("Courier",8),bg=BG3,fg=WHITE)
        self.apps_lbl.pack()
        self.launch_lbl=tk.Label(sw,text="0 launches",font=("Courier",6),bg=BG3,fg=DIM)
        self.launch_lbl.pack(pady=(0,4))

        # Uptime widget
        self.start=datetime.now()
        uw=self._widget(inner,CYAN)
        tk.Label(uw,text="SESSION",font=("Courier",7,"bold"),bg=BG3,fg=CYAN).pack(pady=(4,0))
        self.uptime_lbl=tk.Label(uw,text="00:00",font=("Courier",14,"bold"),bg=BG3,fg=CYAN)
        self.uptime_lbl.pack()
        tk.Label(uw,text="🇰🇪 Built Different",font=("Courier",6),bg=BG3,fg=DIM).pack(pady=(0,4))

        # Version widget
        vw=self._widget(inner,PURPLE)
        tk.Label(vw,text="VERSION",font=("Courier",7,"bold"),bg=BG3,fg=PURPLE).pack(pady=(4,0))
        tk.Label(vw,text="v5.0",font=("Courier",14,"bold"),bg=BG3,fg=NEON).pack()
        tk.Label(vw,text="Brayo & AIRA",font=("Courier",6),bg=BG3,fg=DIM).pack(pady=(0,4))

        tk.Frame(self.frame,bg=PURPLE3,height=1).pack(fill="x")
        self._tick()

    def _widget(self,parent,color):
        outer=tk.Frame(parent,bg=color,padx=1,pady=1)
        outer.pack(side="left",padx=5,pady=2)
        inner=tk.Frame(outer,bg=BG3,width=125)
        inner.pack();inner.pack_propagate(False)
        return inner

    def _tick(self):
        now=datetime.now()
        self.clock_lbl.config(text=now.strftime("%H:%M:%S"))
        self.date_lbl.config(text=now.strftime("%a %d %b %Y"))
        elapsed=now-self.start
        m,s=divmod(int(elapsed.total_seconds()),60)
        h,m=divmod(m,60)
        self.uptime_lbl.config(text=f"{h:02}:{m:02}:{s:02}" if h else f"{m:02}:{s:02}")
        self._get_battery()
        self.root.after(1000,self._tick)

    def _get_battery(self):
        try:
            r=subprocess.run(["termux-battery-status"],capture_output=True,text=True,timeout=2)
            if r.returncode==0:
                d=json.loads(r.stdout)
                p=d.get("percentage",0)
                st=d.get("status","")
                col=GREEN if p>50 else AMBER if p>20 else RED
                self.bat_lbl.config(text=f"{p}%{'⚡' if st=='CHARGING' else ''}",fg=col)
                self.bat_bar.delete("all")
                self.bat_bar.create_rectangle(0,0,100,6,fill=BG2,outline="")
                self.bat_bar.create_rectangle(0,0,p,6,fill=col,outline="")
        except:
            self.bat_lbl.config(text="OK",fg=GREEN)

    def set_launches(self,n):
        self.launch_lbl.config(text=f"{n} launches")

    def set_aira(self,msg):
        self.aira_msg.config(text=msg)

class BrayoOS:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("BrayoOS v5.0")
        self.root.geometry("1280x800")
        self.root.configure(bg=BG)
        self.root.resizable(True,True)
        self.cat="ALL"
        self.search_q=""
        self.stats=load_stats()
        self.notif=NotifCenter(self.root)
        self.pulse_state=True
        self._setup_keys()
        BootScreen(self.root,self._build)
        self.root.mainloop()

    def _setup_keys(self):
        self.root.bind("<F5>",lambda e:self.render_apps(self.cat))
        self.root.bind("<Escape>",lambda e:self._focus_search())
        self.root.bind("<Control-q>",lambda e:self.root.destroy())
        self.root.bind("<F1>",lambda e:self._show_help())

    def _focus_search(self):
        try:self.search_entry.focus_set()
        except:pass

    def _show_help(self):
        w=tk.Toplevel(self.root);w.title("Help");w.configure(bg=BG);w.geometry("400x300")
        tk.Label(w,text="BrayoOS v5.0 Shortcuts",font=("Courier",12,"bold"),bg=BG,fg=NEON).pack(pady=10)
        for key,desc in [("F1","Show this help"),("F5","Refresh app grid"),
                         ("ESC","Focus search bar"),("Ctrl+Q","Quit BrayoOS"),
                         ("Click app","Launch application")]:
            f=tk.Frame(w,bg=BG3);f.pack(fill="x",padx=20,pady=2)
            tk.Label(f,text=key,font=("Courier",9,"bold"),bg=BG3,fg=NEON,width=12).pack(side="left",padx=8,pady=4)
            tk.Label(f,text=desc,font=("Courier",9),bg=BG3,fg=WHITE).pack(side="left")

    def _build(self):
        # TOP BAR
        top=tk.Frame(self.root,bg=BG2,height=40)
        top.pack(fill="x",side="top");top.pack_propagate(False)
        tk.Label(top,text="◈ BrayoOS",font=("Courier",13,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=8)
        tk.Label(top,text="v5.0",font=("Courier",9),bg=BG2,fg=DIM).pack(side="left")
        tk.Label(top,text="| Kenya 🇰🇪 | Built by Brayo & AIRA",font=("Courier",8),bg=BG2,fg=PURPLE2).pack(side="left",padx=8)
        # Right side top bar
        self.clock_top=tk.Label(top,text="",font=("Courier",10),bg=BG2,fg=NEON)
        self.clock_top.pack(side="right",padx=8)
        tk.Button(top,text="🔔",font=("Arial",11),bg=BG2,fg=WHITE,relief="flat",
                 command=self.notif.toggle).pack(side="right",padx=4)
        self.pulse_lbl=tk.Label(top,text="⬤ AIRA",font=("Courier",9,"bold"),bg=BG2,fg=PURPLE)
        self.pulse_lbl.pack(side="right",padx=8)
        tk.Label(top,text="F1:Help  F5:Refresh  ESC:Search  Ctrl+Q:Quit",
                font=("Courier",7),bg=BG2,fg=PURPLE3).pack(side="right",padx=10)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # WIDGET BAR
        self.wb=WidgetBar(self.root,self.root)
        self.wb.set_launches(self.stats.get("launches",0))

        # SEARCH BAR
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=10,pady=4)
        tk.Label(sf,text="🔍",font=("Courier",11),bg=BG,fg=PURPLE).pack(side="left",padx=5)
        self.search_var=tk.StringVar()
        self.search_var.trace("w",lambda *a:self._on_search())
        self.search_entry=tk.Entry(sf,textvariable=self.search_var,
                                   font=("Courier",10),bg=BG3,fg=WHITE,
                                   insertbackground=NEON,relief="flat")
        self.search_entry.pack(side="left",fill="x",expand=True,ipady=6,ipadx=8)
        tk.Label(sf,text="Type to search apps...",font=("Courier",7),bg=BG,fg=DIM).pack(side="right",padx=8)
        tk.Frame(self.root,bg=PURPLE3,height=1).pack(fill="x")

        # CATEGORY BAR
        catbar=tk.Frame(self.root,bg=BG,height=34)
        catbar.pack(fill="x");catbar.pack_propagate(False)
        self.cat_btns={}
        for cat in CATS:
            b=tk.Button(catbar,text=cat,font=("Courier",8,"bold"),
                       bg=BG,fg=DIM,relief="flat",padx=10,pady=5,
                       activebackground=PURPLE3,activeforeground=NEON,
                       command=lambda c=cat:self.switch_cat(c))
            b.pack(side="left",padx=1)
            self.cat_btns[cat]=b
        self.cat_btns["ALL"].config(bg=PURPLE3,fg=NEON)
        tk.Frame(self.root,bg=PURPLE3,height=1).pack(fill="x")

        # MAIN AREA
        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True)
        self._build_sidebar(main)
        self._build_grid(main)
        self._build_dock()

        # Start loops
        threading.Thread(target=self._pulse_loop,daemon=True).start()
        threading.Thread(target=self._clock_loop,daemon=True).start()
        self.notif.add("BrayoOS v5.0","System booted successfully",GREEN)
        self.notif.add("AIRA","AI partner online. Ready Brayo!",NEON)
        self.notif.add("Security","All 63 apps loaded",CYAN)

    def _build_sidebar(self,parent):
        side=tk.Frame(parent,bg=BG2,width=155)
        side.pack(side="left",fill="y");side.pack_propagate(False)

        # AIRA card
        ac=tk.Frame(side,bg=BG3,highlightbackground=PURPLE,highlightthickness=1)
        ac.pack(fill="x",padx=6,pady=8)
        tk.Label(ac,text="AIRA",font=("Courier",16,"bold"),bg=BG3,fg=NEON).pack(pady=(8,2))
        tk.Label(ac,text="AI PARTNER v5.0",font=("Courier",6),bg=BG3,fg=PURPLE).pack()
        tk.Frame(ac,bg=PURPLE,height=1).pack(fill="x",padx=10,pady=5)
        self.aira_msg=tk.Label(ac,text="Ready, Brayo.",font=("Courier",8),
                               bg=BG3,fg=WHITE,wraplength=140,justify="center")
        self.aira_msg.pack(pady=(2,8))

        # AIRA quick chat
        tk.Label(side,text="◈ QUICK CHAT",font=("Courier",7,"bold"),bg=BG2,fg=PURPLE).pack(padx=6,anchor="w",pady=(0,2))
        self.chat_entry=tk.Entry(side,font=("Courier",8),bg=BG3,fg=WHITE,
                                insertbackground=NEON,relief="flat")
        self.chat_entry.pack(fill="x",padx=6,ipady=4)
        self.chat_entry.bind("<Return>",lambda e:self._quick_chat())
        tk.Button(side,text="Ask AIRA →",font=("Courier",7),bg=PURPLE3,fg=NEON,
                 relief="flat",command=self._quick_chat).pack(fill="x",padx=6,pady=2)

        # Recent apps
        tk.Frame(side,bg=PURPLE3,height=1).pack(fill="x",padx=6,pady=6)
        tk.Label(side,text="◈ RECENT APPS",font=("Courier",7,"bold"),bg=BG2,fg=PURPLE).pack(padx=6,anchor="w",pady=(0,2))
        self.recent_frame=tk.Frame(side,bg=BG2);self.recent_frame.pack(fill="x",padx=4)

        # Quick launch
        tk.Frame(side,bg=PURPLE3,height=1).pack(fill="x",padx=6,pady=6)
        tk.Label(side,text="◈ QUICK LAUNCH",font=("Courier",7,"bold"),bg=BG2,fg=PURPLE).pack(padx=6,anchor="w",pady=(0,2))
        quick=[("★","AIRA","aria_voice.py",NEON2),("◉","Ghost","ghost_mode.py",CYAN),
               ("☠","Dark Web","dark_web_monitor.py",RED),("🔍","OSINT","osint_suite.py",NEON),
               ("🌐","VPN","vpn_engine.py",GREEN)]
        for icon,name,script,color in quick:
            f=tk.Frame(side,bg=BG3,cursor="hand2");f.pack(fill="x",padx=6,pady=1)
            tk.Label(f,text=icon,font=("Courier",10),bg=BG3,fg=color,width=3).pack(side="left",padx=5,pady=3)
            tk.Label(f,text=name,font=("Courier",7),bg=BG3,fg=WHITE).pack(side="left")
            for w in [f]+f.winfo_children():
                w.bind("<Button-1>",lambda e,s=script:self.launch(s))
                w.bind("<Enter>",lambda e,x=f:x.config(bg=PURPLE3))
                w.bind("<Leave>",lambda e,x=f:x.config(bg=BG3))

        # Stats
        tk.Frame(side,bg=PURPLE3,height=1).pack(fill="x",padx=6,pady=6)
        tk.Label(side,text=f"◈ {len(APPS)} APPS",font=("Courier",7,"bold"),bg=BG2,fg=PURPLE).pack(padx=6,anchor="w")
        tk.Label(side,text="GPL-3.0 License",font=("Courier",6),bg=BG2,fg=DIM).pack(padx=6,anchor="w")
        tk.Label(side,text="© 2026 Brayo 🇰🇪",font=("Courier",6),bg=BG2,fg=DIM).pack(padx=6,anchor="w",pady=(0,6))

    def _build_grid(self,parent):
        right=tk.Frame(parent,bg=BG);right.pack(side="left",fill="both",expand=True)
        self.canvas=tk.Canvas(right,bg=BG,highlightthickness=0)
        sb=tk.Scrollbar(right,orient="vertical",command=self.canvas.yview,
                       bg=BG2,troughcolor=BG,width=8)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=True)
        self.grid_frame=tk.Frame(self.canvas,bg=BG)
        self.grid_win=self.canvas.create_window((0,0),window=self.grid_frame,anchor="nw")
        self.grid_frame.bind("<Configure>",lambda e:self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",lambda e:self.canvas.itemconfig(
            self.grid_win,width=e.width))
        self.canvas.bind("<MouseWheel>",lambda e:self.canvas.yview_scroll(-1*(e.delta//120),"units"))
        self.canvas.bind("<Button-4>",lambda e:self.canvas.yview_scroll(-1,"units"))
        self.canvas.bind("<Button-5>",lambda e:self.canvas.yview_scroll(1,"units"))
        self.render_apps("ALL")

    def _make_card(self,parent,icon,name,script,color,row,col):
        gf=tk.Frame(parent,bg=color,padx=1,pady=1)
        gf.grid(row=row,column=col,padx=5,pady=5,sticky="nsew")
        card=tk.Frame(gf,bg=BG3,width=105,height=88,cursor="hand2")
        card.pack();card.pack_propagate(False)
        il=tk.Label(card,text=icon,font=("Courier",18,"bold"),bg=BG3,fg=color)
        il.pack(expand=True,pady=(10,2))
        nl=tk.Label(card,text=name[:10],font=("Courier",7),bg=BG3,fg=WHITE)
        nl.pack(pady=(0,6))
        def enter(e):
            gf.config(bg=NEON,padx=2,pady=2)
            for w in [card,il,nl]:w.config(bg=PURPLE4)
            nl.config(fg=NEON)
        def leave(e):
            gf.config(bg=color,padx=1,pady=1)
            for w in [card,il,nl]:w.config(bg=BG3)
            nl.config(fg=WHITE)
        def click(e):
            gf.config(bg=WHITE)
            self.root.after(100,lambda:gf.config(bg=color))
            self.launch(script)
        for w in [gf,card,il,nl]:
            w.bind("<Enter>",enter)
            w.bind("<Leave>",leave)
            w.bind("<Button-1>",click)

    def render_apps(self,cat,query=""):
        for w in self.grid_frame.winfo_children():w.destroy()
        if query:
            apps=[a for a in APPS if query.lower() in a[1].lower() or query.lower() in a[2].lower()]
        elif cat=="ALL" or CATS[cat] is None:
            apps=APPS
        else:
            apps=[a for a in APPS if a[2] in CATS[cat]]
        cols=5
        for c in range(cols):
            self.grid_frame.columnconfigure(c,weight=1)
        for i,(icon,name,script,color) in enumerate(apps):
            r,c=divmod(i,cols)
            self._make_card(self.grid_frame,icon,name,script,color,r,c)

    def switch_cat(self,cat):
        self.cat=cat
        self.search_var.set("")
        for c,b in self.cat_btns.items():b.config(bg=BG,fg=DIM)
        self.cat_btns[cat].config(bg=PURPLE3,fg=NEON)
        self.render_apps(cat)

    def _on_search(self):
        q=self.search_var.get()
        self.render_apps(self.cat,query=q)

    def launch(self,script):
        if script=="terminal":
            subprocess.Popen(["x-terminal-emulator"],env={**os.environ,"DISPLAY":":1"})
            return
        path=os.path.join(APPS_DIR,script)
        if os.path.exists(path):
            subprocess.Popen(["python3",path],env={**os.environ,"DISPLAY":":1"})
            self.aira_msg.config(text=f"Launching\n{script.replace('.py','')}...")
            self.wb.set_aira(f"Opening {script.replace('.py','')}")
            self.root.after(2500,lambda:self.aira_msg.config(text="Ready, Brayo."))
            self.root.after(2500,lambda:self.wb.set_aira("Watching over you"))
            # Stats
            self.stats["launches"]=self.stats.get("launches",0)+1
            most=self.stats.get("most_used",{})
            most[script]=most.get(script,0)+1
            self.stats["most_used"]=most
            save_stats(self.stats)
            self.wb.set_launches(self.stats["launches"])
            self.notif.add("App Launched",script.replace(".py",""),NEON)
            # Recent apps
            name=next((a[1] for a in APPS if a[2]==script),"App")
            icon=next((a[0] for a in APPS if a[2]==script),"▪")
            color=next((a[3] for a in APPS if a[2]==script),NEON)
            if script not in [r[2] for r in getattr(self,"recent",[])] :
                if not hasattr(self,"recent"):self.recent=[]
                self.recent.insert(0,(icon,name,script,color))
                self.recent=self.recent[:4]
                self._render_recent()
        else:
            self.aira_msg.config(text=f"Not found:\n{script[:20]}")
            self.root.after(2000,lambda:self.aira_msg.config(text="Ready, Brayo."))

    def _render_recent(self):
        for w in self.recent_frame.winfo_children():w.destroy()
        for icon,name,script,color in getattr(self,"recent",[]):
            f=tk.Frame(self.recent_frame,bg=BG3,cursor="hand2")
            f.pack(fill="x",pady=1)
            tk.Label(f,text=icon,font=("Courier",9),bg=BG3,fg=color,width=3).pack(side="left",padx=4,pady=3)
            tk.Label(f,text=name[:12],font=("Courier",7),bg=BG3,fg=WHITE).pack(side="left")
            for w in [f]+f.winfo_children():
                w.bind("<Button-1>",lambda e,s=script:self.launch(s))
                w.bind("<Enter>",lambda e,x=f:x.config(bg=PURPLE3))
                w.bind("<Leave>",lambda e,x=f:x.config(bg=BG3))

    def _quick_chat(self):
        msg=self.chat_entry.get().strip()
        if not msg:return
        self.chat_entry.delete(0,"end")
        self.aira_msg.config(text=f"Thinking...")
        # Check local commands
        msg_lower=msg.lower()
        app_map={
            "ghost":("ghost_mode.py","Ghost Mode"),
            "vault":("dna_vault.py","DNA Vault"),
            "dark web":("dark_web_monitor.py","Dark Web"),
            "osint":("osint_suite.py","OSINT"),
            "vpn":("vpn_engine.py","VPN"),
            "aira":("aria_voice.py","AIRA"),
            "hack":("hack_terminal.py","Hack Terminal"),
            "firewall":("firewall.py","Firewall"),
            "cloud":("brayos_cloud.py","Cloud"),
        }
        for key,(script,name) in app_map.items():
            if key in msg_lower:
                self.launch(script)
                self.aira_msg.config(text=f"Opening {name}!")
                return
        # Groq
        threading.Thread(target=self._aira_think,args=(msg,),daemon=True).start()

    def _aira_think(self,msg):
        groq=os.environ.get("GROQ_API_KEY","")
        if not groq:
            self.root.after(0,self.aira_msg.config,{"text":"Set GROQ key\nin ~/.bashrc"})
            return
        try:
            import httpx
            r=httpx.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {groq}","Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile",
                      "messages":[
                          {"role":"system","content":"You are AIRA, AI of BrayoOS. Reply in max 15 words."},
                          {"role":"user","content":msg}],
                      "max_tokens":50},timeout=8)
            reply=r.json()["choices"][0]["message"]["content"].strip()
            self.root.after(0,self.aira_msg.config,{"text":reply[:80]})
        except:
            self.root.after(0,self.aira_msg.config,{"text":"Offline mode.\nCheck internet."})

    def _build_dock(self):
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")
        dock=tk.Frame(self.root,bg=BG2,height=52)
        dock.pack(fill="x",side="bottom");dock.pack_propagate(False)
        docked=[
            ("⌨","Terminal","terminal",PURPLE),
            ("★","AIRA","aria_voice.py",NEON2),
            ("☠","Dark Web","dark_web_monitor.py",RED),
            ("◉","Ghost","ghost_mode.py",CYAN),
            ("🔍","OSINT","osint_suite.py",NEON),
            ("🌐","VPN","vpn_engine.py",GREEN),
            ("💀","Hack","hack_terminal.py",GREEN),
            ("☁","Cloud","brayos_cloud.py",CYAN),
            ("✦","Settings","settings.py","#CCCCFF"),
        ]
        for icon,name,script,color in docked:
            f=tk.Frame(dock,bg=BG2,cursor="hand2",padx=2)
            f.pack(side="left",padx=8,pady=4)
            li=tk.Label(f,text=icon,font=("Courier",15,"bold"),bg=BG2,fg=color)
            li.pack()
            ln=tk.Label(f,text=name,font=("Courier",6),bg=BG2,fg=DIM)
            ln.pack()
            def on_enter(e,fi=f):
                for w in [fi]+fi.winfo_children():w.config(bg=PURPLE3)
            def on_leave(e,fi=f):
                for w in [fi]+fi.winfo_children():w.config(bg=BG2)
            for w in [f,li,ln]:
                w.bind("<Button-1>",lambda e,s=script:self.launch(s))
                w.bind("<Enter>",on_enter)
                w.bind("<Leave>",on_leave)
        tk.Label(dock,text="© 2026 Brayo & AIRA 🇰🇪 — Two minds. One OS. Built Different.",
                font=("Courier",7),bg=BG2,fg=PURPLE3).pack(side="right",padx=12)

    def _pulse_loop(self):
        while True:
            self.pulse_state=not self.pulse_state
            col=NEON if self.pulse_state else PURPLE2
            self.root.after(0,self.pulse_lbl.config,{"fg":col})
            self.root.after(0,self.wb.aira_dot.config,{"fg":GREEN if self.pulse_state else PURPLE2})
            time.sleep(0.8)

    def _clock_loop(self):
        while True:
            now=datetime.now().strftime("%H:%M:%S")
            self.root.after(0,self.clock_top.config,{"text":now})
            time.sleep(1)

if __name__=="__main__":
    BrayoOS()
