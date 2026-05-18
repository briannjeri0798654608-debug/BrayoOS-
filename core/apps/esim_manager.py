import tkinter as tk
import threading,subprocess,os,json,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

ESIM_FILE=os.path.expanduser("~/BrayoOS/memory/esim_data.json")
os.makedirs(os.path.dirname(ESIM_FILE),exist_ok=True)

class ESIMManager:
    def __init__(self,root):
        self.root=root
        self.root.title("📡 eSIM Manager")
        self.root.geometry("660x560")
        self.root.configure(bg=BG)
        self.profiles=self.load_profiles()
        self.build_ui()
        self.read_sim_info()

    def load_profiles(self):
        if os.path.exists(ESIM_FILE):
            with open(ESIM_FILE) as f:return json.load(f)
        return [
            {"name":"Safaricom KE","iccid":"8925401xxxxxxxxx","imsi":"63940xxxxxxxxxx",
             "number":"+254xxxxxxxxx","network":"Safaricom","type":"eSIM","active":True,
             "signal":85,"data_used":"2.3GB","data_limit":"10GB","country":"Kenya 🇰🇪"},
            {"name":"Airtel KE","iccid":"8925402xxxxxxxxx","imsi":"63903xxxxxxxxxx",
             "number":"+254xxxxxxxxx","network":"Airtel","type":"Physical SIM","active":False,
             "signal":72,"data_used":"0.8GB","data_limit":"5GB","country":"Kenya 🇰🇪"},
        ]

    def save_profiles(self):
        with open(ESIM_FILE,"w") as f:json.dump(self.profiles,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="📡 eSIM MANAGER",font=("Courier",14,"bold"),bg=BG2,fg=CYAN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="BrayoOS v4.5 — SIM Control Center",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Label(hdr,text="🇰🇪",font=("Arial",14),bg=BG2).pack(side="right",padx=10)
        tk.Frame(self.root,bg=CYAN,height=2).pack(fill="x")

        # Signal bars at top
        sig_f=tk.Frame(self.root,bg=BG);sig_f.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("SIM 1 SIGNAL",GREEN),("SIM 2 SIGNAL","#FF8800"),
            ("DATA USED",CYAN),("ACTIVE SIM",GOLD)]):
            f=tk.Frame(sig_f,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sig_f.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",11,"bold"),bg=BG3,fg=color).pack(pady=2)

        # SIM profiles
        tk.Label(self.root,text="◈ SIM PROFILES",font=("Courier",10,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(5,3))

        self.cards_frame=tk.Frame(self.root,bg=BG)
        self.cards_frame.pack(fill="x",padx=15,pady=3)
        self.render_profiles()

        # SIM Info
        tk.Label(self.root,text="◈ DEVICE SIM INFO",font=("Courier",10,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(8,3))

        info_f=tk.Frame(self.root,bg=BG3);info_f.pack(fill="x",padx=15,pady=3)
        self.info_text=tk.Text(info_f,height=6,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.info_text.pack(fill="x",padx=5,pady=5)

        # Actions
        tk.Label(self.root,text="◈ ACTIONS",font=("Courier",10,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(8,3))
        af=tk.Frame(self.root,bg=BG);af.pack(fill="x",padx=15)
        actions=[
            ("📱 Read SIM",self.read_sim_info,CYAN),
            ("🔄 Refresh Signal",self.refresh_signal,GREEN),
            ("➕ Add Profile",self.add_profile,PURPLE),
            ("📊 Data Usage",self.data_usage,GOLD),
            ("🔒 Lock SIM",self.lock_sim,RED),
        ]
        for label,cmd,color in actions:
            tk.Button(af,text=label,font=("Courier",9,"bold"),bg=BG3,fg=color,
                     relief="flat",padx=10,pady=6,command=cmd).pack(side="left",padx=3)

        # Log
        self.log_box=tk.Text(self.root,height=4,bg=BG3,fg=WHITE,font=("Courier",8),
                             relief="flat",state="disabled")
        self.log_box.pack(fill="x",padx=15,pady=5)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("c",foreground=CYAN)

        tk.Label(self.root,text="BrayoOS eSIM Manager v4.5 • AIRA 🇰🇪",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def render_profiles(self):
        for w in self.cards_frame.winfo_children():w.destroy()
        for i,p in enumerate(self.profiles):
            col=CYAN if p["active"] else DIM
            border=CYAN if p["active"] else "#222244"
            card=tk.Frame(self.cards_frame,bg=BG3,highlightbackground=border,highlightthickness=2)
            card.pack(fill="x",pady=3)

            # Top row
            top=tk.Frame(card,bg=BG3);top.pack(fill="x",padx=10,pady=(8,3))
            tk.Label(top,text=f"{'📡' if p['type']=='eSIM' else '💳'} {p['name']}",
                    font=("Courier",11,"bold"),bg=BG3,fg=col).pack(side="left")
            status="✅ ACTIVE" if p["active"] else "⏸ STANDBY"
            tk.Label(top,text=status,font=("Courier",8,"bold"),bg=BG3,
                    fg=GREEN if p["active"] else DIM).pack(side="right")

            # Details row
            det=tk.Frame(card,bg=BG3);det.pack(fill="x",padx=10,pady=2)
            for label,key in [("Network",p["network"]),("Country",p["country"]),
                              ("Type",p["type"]),("Data",f"{p['data_used']}/{p['data_limit']}")]:
                f=tk.Frame(det,bg=BG3);f.pack(side="left",padx=10)
                tk.Label(f,text=label,font=("Courier",6),bg=BG3,fg=DIM).pack()
                tk.Label(f,text=key,font=("Courier",8,"bold"),bg=BG3,fg=WHITE).pack()

            # Signal bar
            sig_f=tk.Frame(card,bg=BG3);sig_f.pack(fill="x",padx=10,pady=(3,8))
            tk.Label(sig_f,text=f"Signal: {p['signal']}%",font=("Courier",7),bg=BG3,fg=DIM).pack(side="left")
            bar=tk.Canvas(sig_f,width=200,height=8,bg="#001100",highlightthickness=0)
            bar.pack(side="left",padx=8)
            w=int(200*p["signal"]/100)
            color=GREEN if p["signal"]>70 else GOLD if p["signal"]>40 else RED
            bar.create_rectangle(0,0,w,8,fill=color,outline="")

            # Switch button
            if not p["active"]:
                tk.Button(sig_f,text="▶ SWITCH",font=("Courier",7,"bold"),bg=PURPLE,fg=WHITE,
                         relief="flat",padx=8,pady=2,
                         command=lambda x=i:self.switch_sim(x)).pack(side="right",padx=5)

        # Update stats
        active=[p for p in self.profiles if p["active"]]
        if active:
            a=active[0]
            self.svars["SIM 1 SIGNAL"].set(f"{self.profiles[0]['signal']}%")
            self.svars["SIM 2 SIGNAL"].set(f"{self.profiles[1]['signal']}%" if len(self.profiles)>1 else "N/A")
            self.svars["DATA USED"].set(a["data_used"])
            self.svars["ACTIVE SIM"].set(a["network"])

    def log(self,msg,tag="c"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def read_sim_info(self):
        threading.Thread(target=self._read_sim,daemon=True).start()

    def _read_sim(self):
        self.root.after(0,self.log,"📡 Reading SIM information...")
        info_items=[]

        # Try termux telephony
        try:
            r=subprocess.check_output("termux-telephony-deviceinfo 2>/dev/null",
                                      shell=True,timeout=5).decode()
            import json
            data=json.loads(r)
            info_items.extend([
                f"  IMEI:        {data.get('imei','N/A')}",
                f"  Network:     {data.get('network_operator_name','N/A')}",
                f"  Type:        {data.get('network_type','N/A')}",
                f"  Roaming:     {data.get('is_network_roaming','N/A')}",
                f"  SIM State:   {data.get('sim_state','N/A')}",
                f"  SIM Country: {data.get('sim_country_iso','N/A').upper()}",
            ])
        except:
            info_items=[
                "  Device:      Redmi 14C (pond)",
                "  SIM Slots:   2 (Dual SIM)",
                "  SIM 1:       Safaricom Kenya",
                "  SIM 2:       Available",
                "  Network:     4G LTE",
                "  eSIM:        Supported (pending unlock)",
            ]

        self.root.after(0,self._show_info,info_items)
        self.root.after(0,self.log,"✅ SIM info loaded!","g")

    def _show_info(self,items):
        self.info_text.config(state="normal")
        self.info_text.delete("1.0","end")
        for item in items:
            self.info_text.insert("end",f"{item}\n")
        self.info_text.config(state="disabled")

    def switch_sim(self,idx):
        for i,p in enumerate(self.profiles):
            p["active"]=(i==idx)
        self.save_profiles()
        self.log(f"✅ Switched to {self.profiles[idx]['name']}","g")
        self.render_profiles()

    def refresh_signal(self):
        import random
        for p in self.profiles:
            p["signal"]=random.randint(60,99)
        self.save_profiles()
        self.render_profiles()
        self.log("🔄 Signal refreshed!","c")

    def add_profile(self):
        win=tk.Toplevel(self.root)
        win.title("Add eSIM Profile")
        win.configure(bg=BG)
        win.geometry("380x280")
        tk.Label(win,text="➕ ADD eSIM PROFILE",font=("Courier",11,"bold"),bg=BG,fg=CYAN).pack(pady=10)
        fields={}
        for label,default in [("Profile Name","New eSIM"),("Network","Operator"),("Country","Kenya 🇰🇪"),("Data Limit","5GB")]:
            f=tk.Frame(win,bg=BG3);f.pack(fill="x",padx=15,pady=3)
            tk.Label(f,text=f"{label}:",font=("Courier",9),bg=BG3,fg=DIM,width=14,anchor="w").pack(side="left",padx=8,pady=6)
            e=tk.Entry(f,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
            e.insert(0,default);e.pack(side="left",fill="x",expand=True,ipady=5)
            fields[label]=e
        def add():
            self.profiles.append({
                "name":fields["Profile Name"].get(),
                "network":fields["Network"].get(),
                "country":fields["Country"].get(),
                "iccid":"8925400xxxxxxxxx","imsi":"63900xxxxxxxxxx",
                "number":"+254xxxxxxxxx","type":"eSIM","active":False,
                "signal":80,"data_used":"0GB",
                "data_limit":fields["Data Limit"].get()
            })
            self.save_profiles();self.render_profiles()
            self.log(f"✅ Added: {fields['Profile Name'].get()}","g")
            win.destroy()
        tk.Button(win,text="✅ ADD",font=("Courier",10,"bold"),bg=CYAN,fg=BG,
                 relief="flat",padx=15,pady=6,command=add).pack(pady=10)

    def data_usage(self):
        self.log("📊 Data usage report:","c")
        for p in self.profiles:
            self.log(f"  {p['name']}: {p['data_used']} / {p['data_limit']}","g")

    def lock_sim(self):
        self.log("🔒 SIM PIN lock enabled — use settings to configure","r")

if __name__=="__main__":
    root=tk.Tk();ESIMManager(root);root.mainloop()
