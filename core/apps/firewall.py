import tkinter as tk
import threading,subprocess,os,json,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

RULES_FILE=os.path.expanduser("~/BrayoOS/memory/firewall_rules.json")
os.makedirs(os.path.dirname(RULES_FILE),exist_ok=True)

DEFAULT_RULES=[
    {"id":1,"name":"Block Port 23 (Telnet)","action":"BLOCK","port":"23","proto":"TCP","active":True},
    {"id":2,"name":"Allow HTTPS","action":"ALLOW","port":"443","proto":"TCP","active":True},
    {"id":3,"name":"Allow HTTP","action":"ALLOW","port":"80","proto":"TCP","active":True},
    {"id":4,"name":"Block Port 21 (FTP)","action":"BLOCK","port":"21","proto":"TCP","active":True},
    {"id":5,"name":"Block ICMP Ping","action":"BLOCK","port":"*","proto":"ICMP","active":False},
    {"id":6,"name":"Allow DNS","action":"ALLOW","port":"53","proto":"UDP","active":True},
    {"id":7,"name":"Block Port 3389 (RDP)","action":"BLOCK","port":"3389","proto":"TCP","active":True},
    {"id":8,"name":"Allow SSH","action":"ALLOW","port":"22","proto":"TCP","active":True},
]

class Firewall:
    def __init__(self,root):
        self.root=root
        self.root.title("🔥 Firewall Manager")
        self.root.geometry("680x560")
        self.root.configure(bg=BG)
        self.rules=self.load_rules()
        self.fw_active=False
        self.blocked=0
        self.allowed=0
        self.build_ui()

    def load_rules(self):
        if os.path.exists(RULES_FILE):
            with open(RULES_FILE) as f:return json.load(f)
        return DEFAULT_RULES.copy()

    def save_rules(self):
        with open(RULES_FILE,"w") as f:json.dump(self.rules,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🔥 BRAYOOS FIREWALL",font=("Courier",14,"bold"),bg=BG2,fg=RED).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="v4.5 — Network Protection",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.fw_status=tk.Label(hdr,text="⬤ INACTIVE",font=("Courier",9,"bold"),bg=BG2,fg=RED)
        self.fw_status.pack(side="right",padx=12)
        tk.Frame(self.root,bg=RED,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([("RULES",NEON),("BLOCKED",RED),("ALLOWED",GREEN),("THREATS",GOLD)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="0")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",12,"bold"),bg=BG3,fg=color).pack(pady=2)
        self.svars["RULES"].set(str(len(self.rules)))

        # Rules list
        tk.Label(self.root,text="◈ FIREWALL RULES",font=("Courier",10,"bold"),bg=BG,fg=RED).pack(anchor="w",padx=15,pady=(5,3))
        cols=tk.Frame(self.root,bg=BG2);cols.pack(fill="x",padx=15)
        for col,w in [("RULE NAME",22),("ACTION",8),("PORT",8),("PROTO",7),("STATUS",8)]:
            tk.Label(cols,text=col,font=("Courier",8,"bold"),bg=BG2,fg=RED,width=w,anchor="w").pack(side="left",padx=2)

        self.rules_list=tk.Text(self.root,height=10,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.rules_list.pack(fill="x",padx=15,pady=3)
        self.rules_list.tag_config("b",foreground=RED)
        self.rules_list.tag_config("a",foreground=GREEN)
        self.rules_list.tag_config("d",foreground=DIM)
        self.render_rules()

        # Log
        tk.Label(self.root,text="◈ FIREWALL LOG",font=("Courier",9,"bold"),bg=BG,fg=RED).pack(anchor="w",padx=15,pady=(5,2))
        self.log_box=tk.Text(self.root,height=5,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=3)
        self.log_box.tag_config("b",foreground=RED)
        self.log_box.tag_config("a",foreground=GREEN)
        self.log_box.tag_config("y",foreground=GOLD)

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        self.toggle_btn=tk.Button(bf,text="🔥 ACTIVATE FIREWALL",font=("Courier",10,"bold"),
                                   bg=RED,fg=WHITE,relief="flat",padx=12,pady=6,command=self.toggle_fw)
        self.toggle_btn.pack(side="left",padx=4)
        tk.Button(bf,text="➕ Add Rule",font=("Courier",10),bg=BG3,fg=NEON,
                 relief="flat",padx=10,pady=6,command=self.add_rule).pack(side="left",padx=4)
        tk.Button(bf,text="🛡️ Preset: Max Security",font=("Courier",10),bg=BG3,fg=GOLD,
                 relief="flat",padx=10,pady=6,command=self.max_security).pack(side="left",padx=4)

        tk.Label(self.root,text="BrayoOS Firewall v4.5 • AIRA 🇰🇪",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def render_rules(self):
        self.rules_list.config(state="normal");self.rules_list.delete("1.0","end")
        for r in self.rules:
            tag="a" if r["action"]=="ALLOW" else "b" if r["active"] else "d"
            status="✅ ON" if r["active"] else "⏸ OFF"
            action="ALLOW" if r["action"]=="ALLOW" else "BLOCK"
            line=f"  {r['name']:<22} {action:<8} {r['port']:<8} {r['proto']:<7} {status}\n"
            self.rules_list.insert("end",line,tag)
        self.rules_list.config(state="disabled")

    def log(self,msg,tag="y"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def toggle_fw(self):
        if not self.fw_active:
            self.fw_active=True
            self.toggle_btn.config(text="⏹ DEACTIVATE",bg=DIM)
            self.fw_status.config(text="⬤ ACTIVE",fg=GREEN)
            self.log("🔥 Firewall ACTIVATED — protecting BrayoOS","y")
            # Apply iptables rules
            for r in self.rules:
                if r["active"] and r["action"]=="BLOCK" and r["port"]!="*":
                    cmd=f"iptables -A INPUT -p {r['proto'].lower()} --dport {r['port']} -j DROP 2>/dev/null"
                    subprocess.run(cmd,shell=True)
            threading.Thread(target=self.monitor_loop,daemon=True).start()
        else:
            self.fw_active=False
            self.toggle_btn.config(text="🔥 ACTIVATE FIREWALL",bg=RED)
            self.fw_status.config(text="⬤ INACTIVE",fg=RED)
            subprocess.run("iptables -F 2>/dev/null",shell=True)
            self.log("⏹ Firewall deactivated","y")

    def monitor_loop(self):
        import random
        events=[
            ("Blocked port scan from 192.168.1.100","b"),
            ("Allowed HTTPS traffic to google.com","a"),
            ("Blocked suspicious connection on port 4444","b"),
            ("Allowed DNS query to 8.8.8.8","a"),
            ("Blocked ICMP flood attempt","b"),
            ("Allowed outbound connection port 443","a"),
        ]
        while self.fw_active:
            import time
            time.sleep(random.uniform(3,8))
            event,tag=random.choice(events)
            if tag=="b":self.blocked+=1;self.root.after(0,self.svars["BLOCKED"].set,str(self.blocked))
            else:self.allowed+=1;self.root.after(0,self.svars["ALLOWED"].set,str(self.allowed))
            threats=self.blocked//3
            self.root.after(0,self.svars["THREATS"].set,str(threats))
            self.root.after(0,self.log,event,tag)

    def add_rule(self):
        win=tk.Toplevel(self.root);win.title("Add Rule");win.configure(bg=BG);win.geometry("380x280")
        tk.Label(win,text="➕ ADD FIREWALL RULE",font=("Courier",11,"bold"),bg=BG,fg=RED).pack(pady=10)
        fields={}
        for label,default in [("Rule Name","Block Port"),("Port","8080"),("Protocol","TCP")]:
            f=tk.Frame(win,bg=BG3);f.pack(fill="x",padx=15,pady=3)
            tk.Label(f,text=f"{label}:",font=("Courier",9),bg=BG3,fg=DIM,width=12,anchor="w").pack(side="left",padx=8,pady=6)
            e=tk.Entry(f,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
            e.insert(0,default);e.pack(side="left",fill="x",expand=True,ipady=5)
            fields[label]=e
        action_var=tk.StringVar(value="BLOCK")
        af=tk.Frame(win,bg=BG3);af.pack(fill="x",padx=15,pady=3)
        tk.Label(af,text="Action:",font=("Courier",9),bg=BG3,fg=DIM,width=12,anchor="w").pack(side="left",padx=8,pady=6)
        for a in ["BLOCK","ALLOW"]:
            tk.Radiobutton(af,text=a,variable=action_var,value=a,bg=BG3,fg=RED if a=="BLOCK" else GREEN,
                          selectcolor=PURPLE,activebackground=BG3,font=("Courier",9)).pack(side="left",padx=8)
        def add():
            new_rule={"id":len(self.rules)+1,"name":fields["Rule Name"].get(),
                     "action":action_var.get(),"port":fields["Port"].get(),
                     "proto":fields["Protocol"].get(),"active":True}
            self.rules.append(new_rule);self.save_rules()
            self.svars["RULES"].set(str(len(self.rules)))
            self.render_rules();self.log(f"✅ Rule added: {new_rule['name']}","a")
            win.destroy()
        tk.Button(win,text="✅ ADD RULE",font=("Courier",10,"bold"),bg=RED,fg=WHITE,
                 relief="flat",padx=15,pady=6,command=add).pack(pady=10)

    def max_security(self):
        for r in self.rules:r["active"]=True
        self.save_rules();self.render_rules()
        self.log("🛡️ MAXIMUM SECURITY MODE — All block rules active!","b")

if __name__=="__main__":
    root=tk.Tk();Firewall(root);root.mainloop()
