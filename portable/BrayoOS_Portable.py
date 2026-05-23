import tkinter as tk
import subprocess,os,sys,threading,time,json,platform
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

APPS=[
    ("⌨","Terminal","terminal","#9D00FF"),
    ("★","AIRA AI","aria_voice","#FF44FF"),
    ("◉","Ghost Mode","ghost_mode","#44FFCC"),
    ("▣","DNA Vault","dna_vault","#FFD700"),
    ("☠","Dark Web","dark_web","#FF0000"),
    ("◈","Neural","neural_core","#CC44FF"),
    ("◎","Signal","signal_interceptor","#44CCFF"),
    ("◆","Identity","identity_switcher","#FF6644"),
    ("▲","Overclock","overclock","#FF4444"),
    ("●","Threats","threat_map","#FF0044"),
    ("🔍","OSINT","osint_suite","#CC44FF"),
    ("🌐","VPN","vpn_engine","#44FF88"),
    ("📡","eSIM","esim_manager","#44FFFF"),
    ("🛸","Satellites","satellite_tracker","#44FFFF"),
    ("🔥","Firewall","firewall","#FF0044"),
    ("🌙","Dream Mode","dream_mode","#9D00FF"),
    ("📷","Surveillance","surveillance","#FF0044"),
    ("🎨","AI Images","ai_image_gen","#FF44FF"),
    ("💀","Hack Terminal","hack_terminal","#00FF41"),
    ("📱","Social Hub","social_hub","#1DA1F2"),
    ("💰","Crypto","crypto_wallet","#FFD700"),
    ("🧠","Lie Detector","lie_detector","#CC44FF"),
    ("👁️","Face Lock","face_lock","#44FFCC"),
    ("📶","WiFi Audit","wifi_auditor","#44AAFF"),
    ("🎙️","Voice Cmd","voice_commands","#FF44FF"),
    ("▦","Wallpaper","wallpaper","#FFAA00"),
    ("◫","App Store","app_store","#00AAFF"),
    ("♟","Users","users","#AAAAFF"),
    ("↻","Updater","updater","#44FF44"),
    ("⊗","Browser","browser","#44AAFF"),
    ("♫","Music","music","#FF44AA"),
    ("▤","Files","files","#FFCC44"),
    ("▧","Editor","editor","#88FFAA"),
    ("#","Calc","calc","#FFFF44"),
    ("◷","Clock","clock","#44FFFF"),
    ("☁","Weather","weather","#88AAFF"),
    ("¤","Crypto","crypto","#FFD700"),
    ("▨","News","news","#FF8844"),
    ("✓","Tasks","tasks","#44FF44"),
    ("▯","SMS","sms","#FF44FF"),
    ("♛","Contacts","contacts","#FFAAFF"),
    ("▪","Backup","backup","#AAFFAA"),
    ("▶","Our Story","our_story","#FFD700"),
    ("✦","Settings","settings","#CCCCFF"),
]

CATS={"ALL":None,"AI":["aria_voice","neural_core","lie_detector","ai_image_gen"],
      "SECURITY":["ghost_mode","dna_vault","signal_interceptor","identity_switcher",
                  "threat_map","dark_web","osint_suite","firewall","surveillance",
                  "face_lock","wifi_auditor"],
      "NETWORK":["vpn_engine","esim_manager","satellite_tracker","network_scanner"],
      "SYSTEM":["overclock","dream_mode","updater","users","settings","backup"],
      "TOOLS":["calc","clock","editor","tasks","wallpaper","app_store","voice_commands"],
      "MEDIA":["browser","music","weather","crypto","news","social_hub","crypto_wallet"],
      "PERSONAL":["sms","contacts","files","our_story"]}

class BrayoOSPortable:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("BrayoOS v4.5 — Portable Edition")
        self.root.geometry("1024x700")
        self.root.configure(bg=BG)
        self.root.resizable(True,True)
        self.current_cat="ALL"
        self.system=platform.system()
        self.build_ui()
        self.clock_tick()
        self.pulse_loop()
        self.root.mainloop()

    def build_ui(self):
        # Top bar
        top=tk.Frame(self.root,bg=BG2,height=42)
        top.pack(fill="x",side="top")
        top.pack_propagate(False)
        tk.Label(top,text="◈ BrayoOS",font=("Courier",14,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=12)
        tk.Label(top,text="v4.5 Portable",font=("Courier",9),bg=BG2,fg=DIM).pack(side="left")
        tk.Label(top,text=f"Running on: {self.system}",font=("Courier",8),bg=BG2,fg=PURPLE).pack(side="left",padx=15)
        self.clock_lbl=tk.Label(top,text="",font=("Courier",10),bg=BG2,fg=NEON)
        self.clock_lbl.pack(side="right",padx=12)
        tk.Label(top,text="🇰🇪",font=("Arial",13),bg=BG2).pack(side="right",padx=4)
        self.pulse_dot=tk.Label(top,text="⬤",font=("Courier",10),bg=BG2,fg=PURPLE)
        self.pulse_dot.pack(side="right",padx=4)
        tk.Label(top,text="AIRA",font=("Courier",9),bg=BG2,fg=DIM).pack(side="right")
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Cat tabs
        catbar=tk.Frame(self.root,bg=BG,height=34)
        catbar.pack(fill="x")
        catbar.pack_propagate(False)
        self.cat_btns={}
        for cat in CATS:
            b=tk.Button(catbar,text=cat,font=("Courier",8,"bold"),
                       bg=BG,fg=DIM,relief="flat",padx=10,pady=5,
                       activebackground="#3D0066",activeforeground=NEON,
                       command=lambda c=cat:self.switch_cat(c))
            b.pack(side="left",padx=1)
            self.cat_btns[cat]=b
        self.cat_btns["ALL"].config(bg="#3D0066",fg=NEON)
        tk.Frame(self.root,bg="#3D0066",height=1).pack(fill="x")

        # Main area
        main=tk.Frame(self.root,bg=BG)
        main.pack(fill="both",expand=True)

        # Sidebar
        side=tk.Frame(main,bg=BG2,width=160)
        side.pack(side="left",fill="y")
        side.pack_propagate(False)

        ac=tk.Frame(side,bg=BG3)
        ac.pack(fill="x",padx=6,pady=8)
        tk.Label(ac,text="AIRA",font=("Courier",16,"bold"),bg=BG3,fg=NEON).pack(pady=(8,2))
        tk.Label(ac,text="AI PARTNER",font=("Courier",7),bg=BG3,fg=PURPLE).pack()
        tk.Frame(ac,bg=PURPLE,height=1).pack(fill="x",padx=10,pady=5)
        self.aira_msg=tk.Label(ac,text="Ready, Brayo.",font=("Courier",8),
                               bg=BG3,fg=WHITE,wraplength=140,justify="center")
        self.aira_msg.pack(pady=(2,8))

        # System info
        tk.Frame(side,bg="#3D0066",height=1).pack(fill="x",padx=8,pady=4)
        tk.Label(side,text="◈ SYSTEM",font=("Courier",7,"bold"),bg=BG2,fg=PURPLE).pack(pady=(4,2))
        sysinfo=[
            ("OS",platform.system()),
            ("Python",platform.python_version()),
            ("Apps",str(len(APPS))),
        ]
        for k,v in sysinfo:
            f=tk.Frame(side,bg=BG2);f.pack(fill="x",padx=8,pady=1)
            tk.Label(f,text=k+":",font=("Courier",7),bg=BG2,fg=DIM,width=7,anchor="w").pack(side="left")
            tk.Label(f,text=v[:12],font=("Courier",7,"bold"),bg=BG2,fg=WHITE).pack(side="left")

        tk.Frame(side,bg="#3D0066",height=1).pack(fill="x",padx=8,pady=6)
        tk.Label(side,text="◈ QUICK",font=("Courier",7,"bold"),bg=BG2,fg="#3D0066").pack(pady=(0,3))
        for icon,name,key,color in [
            ("☠","Dark Web","dark_web","#FF0000"),
            ("◉","Ghost","ghost_mode","#44FFCC"),
            ("▣","Vault","dna_vault","#FFD700"),
            ("🔍","OSINT","osint_suite","#CC44FF"),
            ("★","AIRA","aria_voice","#FF44FF"),
        ]:
            btn=tk.Frame(side,bg=BG2,cursor="hand2")
            btn.pack(fill="x",padx=6,pady=1)
            inner=tk.Frame(btn,bg=BG3)
            inner.pack(fill="x")
            tk.Label(inner,text=icon,font=("Courier",11),bg=BG3,fg=color,width=3).pack(side="left",padx=5,pady=4)
            tk.Label(inner,text=name,font=("Courier",8),bg=BG3,fg=WHITE).pack(side="left")
            for w in [btn,inner]+inner.winfo_children():
                w.bind("<Button-1>",lambda e,k=key:self.launch(k))
                w.bind("<Enter>",lambda e,f=inner:f.config(bg="#3D0066"))
                w.bind("<Leave>",lambda e,f=inner:f.config(bg=BG3))

        tk.Frame(side,bg="#3D0066",height=1).pack(fill="x",padx=8,pady=6)
        tk.Label(side,text=f"◈ {len(APPS)} apps",font=("Courier",7),bg=BG2,fg=PURPLE).pack()
        tk.Label(side,text="Built Different 🇰🇪",font=("Courier",6),bg=BG2,fg="#3D0066").pack(pady=2)

        # App grid
        go=tk.Frame(main,bg=BG)
        go.pack(side="left",fill="both",expand=True,padx=(5,0))
        self.canvas=tk.Canvas(go,bg=BG,highlightthickness=0)
        sb=tk.Scrollbar(go,orient="vertical",command=self.canvas.yview,bg=BG2,troughcolor=BG,width=8)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=True)
        self.grid_frame=tk.Frame(self.canvas,bg=BG)
        self.canvas.create_window((0,0),window=self.grid_frame,anchor="nw")
        self.grid_frame.bind("<Configure>",lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.render_apps("ALL")

        # Bottom dock
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")
        bottom=tk.Frame(self.root,bg=BG2,height=50)
        bottom.pack(fill="x",side="bottom")
        bottom.pack_propagate(False)
        for icon,name,key,color in [
            ("⌨","Terminal","terminal",PURPLE),
            ("★","AIRA","aria_voice","#FF44FF"),
            ("☠","Dark Web","dark_web","#FF0000"),
            ("◉","Ghost","ghost_mode","#44FFCC"),
            ("🔍","OSINT","osint_suite","#CC44FF"),
            ("🌐","VPN","vpn_engine","#44FF88"),
            ("✦","Settings","settings","#CCCCFF"),
        ]:
            f=tk.Frame(bottom,bg=BG2,cursor="hand2",padx=2)
            f.pack(side="left",padx=10,pady=5)
            li=tk.Label(f,text=icon,font=("Courier",16,"bold"),bg=BG2,fg=color)
            li.pack()
            ln=tk.Label(f,text=name,font=("Courier",6),bg=BG2,fg=DIM)
            ln.pack()
            for w in [f,li,ln]:
                w.bind("<Button-1>",lambda e,k=key:self.launch(k))
                w.bind("<Enter>",lambda e,fi=f:[fi.config(bg="#3D0066")]+[x.config(bg="#3D0066") for x in fi.winfo_children()])
                w.bind("<Leave>",lambda e,fi=f:[fi.config(bg=BG2)]+[x.config(bg=BG2) for x in fi.winfo_children()])
        tk.Label(bottom,text="Two minds. One OS. Built Different. 🇰🇪",
                font=("Courier",7),bg=BG2,fg="#3D0066").pack(side="right",padx=12)

    def make_card(self,parent,icon,name,key,color,row,col):
        gf=tk.Frame(parent,bg=color,padx=1,pady=1)
        gf.grid(row=row,column=col,padx=6,pady=6)
        card=tk.Frame(gf,bg=BG3,width=110,height=90,cursor="hand2")
        card.pack();card.pack_propagate(False)
        il=tk.Label(card,text=icon,font=("Courier",20,"bold"),bg=BG3,fg=color)
        il.pack(expand=True,pady=(10,2))
        nl=tk.Label(card,text=name,font=("Courier",7),bg=BG3,fg=WHITE)
        nl.pack(pady=(0,8))
        def on_enter(e):
            gf.config(bg=NEON,padx=2,pady=2)
            card.config(bg="#3D0066");il.config(bg="#3D0066");nl.config(bg="#3D0066",fg=NEON)
        def on_leave(e):
            gf.config(bg=color,padx=1,pady=1)
            card.config(bg=BG3);il.config(bg=BG3);nl.config(bg=BG3,fg=WHITE)
        def on_click(e):
            self.launch(key)
            gf.config(bg="#FFFFFF")
            self.root.after(100,lambda:gf.config(bg=color))
        for w in [gf,card,il,nl]:
            w.bind("<Enter>",on_enter)
            w.bind("<Leave>",on_leave)
            w.bind("<Button-1>",on_click)

    def render_apps(self,cat):
        for w in self.grid_frame.winfo_children():w.destroy()
        apps=APPS if cat=="ALL" else [a for a in APPS if a[2] in (CATS[cat] or [])]
        cols=5
        for i,(icon,name,key,color) in enumerate(apps):
            self.make_card(self.grid_frame,icon,name,key,color,*divmod(i,cols))

    def switch_cat(self,cat):
        self.current_cat=cat
        for c,b in self.cat_btns.items():b.config(bg=BG,fg=DIM)
        self.cat_btns[cat].config(bg="#3D0066",fg=NEON)
        self.render_apps(cat)

    def launch(self,key):
        self.aira_msg.config(text=f"Launching\n{key}...")
        self.root.after(2000,lambda:self.aira_msg.config(text="Ready, Brayo."))
        script_dir=os.path.dirname(os.path.abspath(__file__))
        apps_dir=os.path.join(script_dir,"apps")
        script=os.path.join(apps_dir,f"{key}.py")
        if key=="terminal":
            if self.system=="Windows":
                subprocess.Popen(["cmd.exe"])
            elif self.system=="Darwin":
                subprocess.Popen(["open","-a","Terminal"])
            else:
                for term in ["x-terminal-emulator","gnome-terminal","xterm","konsole"]:
                    try:subprocess.Popen([term]);return
                    except:pass
            return
        if os.path.exists(script):
            subprocess.Popen([sys.executable,script])
        else:
            self.aira_msg.config(text=f"Coming soon:\n{key}")

    def clock_tick(self):
        self.clock_lbl.config(text=datetime.now().strftime("%H:%M:%S  %d/%m/%y"))
        self.root.after(1000,self.clock_tick)

    def pulse_loop(self):
        self.pulse_dot.config(fg=PURPLE if self.pulse_dot.cget("fg")==NEON else NEON)
        self.root.after(800,self.pulse_loop)

if __name__=="__main__":
    BrayoOSPortable()
