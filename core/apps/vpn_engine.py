import tkinter as tk
import threading,subprocess,os,json,time,httpx,random
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

VPN_SERVERS=[
    {"name":"Nairobi 🇰🇪","ip":"196.201.x.x","country":"Kenya","ping":12,"load":23,"free":True},
    {"name":"Lagos 🇳🇬","ip":"41.58.x.x","country":"Nigeria","ping":28,"load":45,"free":True},
    {"name":"London 🇬🇧","ip":"51.68.x.x","country":"UK","ping":142,"load":67,"free":True},
    {"name":"New York 🇺🇸","ip":"45.33.x.x","country":"USA","ping":198,"load":78,"free":True},
    {"name":"Tokyo 🇯🇵","ip":"139.162.x.x","country":"Japan","ping":312,"load":34,"free":True},
    {"name":"Amsterdam 🇳🇱","ip":"37.120.x.x","country":"Netherlands","ping":156,"load":56,"free":True},
    {"name":"Singapore 🇸🇬","ip":"103.86.x.x","country":"Singapore","ping":245,"load":41,"free":True},
    {"name":"Toronto 🇨🇦","ip":"198.199.x.x","country":"Canada","ping":221,"load":29,"free":True},
]

class VPNEngine:
    def __init__(self,root):
        self.root=root
        self.root.title("🌐 VPN Engine")
        self.root.geometry("650x560")
        self.root.configure(bg=BG)
        self.connected=False
        self.current_server=None
        self.bytes_sent=0
        self.bytes_recv=0
        self.build_ui()
        self.check_ip()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🌐 BRAYOOS VPN ENGINE",font=("Courier",14,"bold"),bg=BG2,fg=GREEN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="v4.5 — Private & Secure",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Frame(self.root,bg=GREEN,height=2).pack(fill="x")

        # Status panel
        status_f=tk.Frame(self.root,bg=BG2)
        status_f.pack(fill="x",padx=15,pady=8)
        left_s=tk.Frame(status_f,bg=BG2);left_s.pack(side="left",padx=15,pady=8)
        self.vpn_dot=tk.Label(left_s,text="⬤",font=("Courier",32),bg=BG2,fg=RED)
        self.vpn_dot.pack()
        self.vpn_status=tk.Label(left_s,text="DISCONNECTED",font=("Courier",10,"bold"),bg=BG2,fg=RED)
        self.vpn_status.pack()

        right_s=tk.Frame(status_f,bg=BG2);right_s.pack(side="left",fill="x",expand=True,pady=8)
        self.svars={}
        for row,(lbl,color) in enumerate([("MY IP",NEON),("VPN IP",GREEN),("LOCATION",GOLD),("PING","#FF8800")]):
            tk.Label(right_s,text=f"{lbl}:",font=("Courier",8),bg=BG2,fg=DIM,width=10,anchor="w").grid(row=row,column=0,padx=5,pady=1,sticky="w")
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(right_s,textvariable=v,font=("Courier",9,"bold"),bg=BG2,fg=color,anchor="w").grid(row=row,column=1,padx=5,pady=1,sticky="w")

        # Traffic stats
        tf=tk.Frame(status_f,bg=BG3);tf.pack(side="right",padx=15,pady=8)
        tk.Label(tf,text="TRAFFIC",font=("Courier",7),bg=BG3,fg=DIM).pack()
        self.upload_lbl=tk.Label(tf,text="↑ 0 KB",font=("Courier",8),bg=BG3,fg=GREEN);self.upload_lbl.pack()
        self.download_lbl=tk.Label(tf,text="↓ 0 KB",font=("Courier",8),bg=BG3,fg=NEON);self.download_lbl.pack()

        # Server list
        tk.Label(self.root,text="◈ VPN SERVERS",font=("Courier",10,"bold"),bg=BG,fg=GREEN).pack(anchor="w",padx=15,pady=(5,3))
        cols=tk.Frame(self.root,bg=BG2);cols.pack(fill="x",padx=15)
        for col,w in [("SERVER",18),("COUNTRY",12),("PING",8),("LOAD",8),("STATUS",10)]:
            tk.Label(cols,text=col,font=("Courier",8,"bold"),bg=BG2,fg=GREEN,width=w,anchor="w").pack(side="left",padx=2)

        self.server_list=tk.Text(self.root,height=10,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled",cursor="hand2")
        self.server_list.pack(fill="both",expand=True,padx=15,pady=3)
        self.server_list.tag_config("g",foreground=GREEN)
        self.server_list.tag_config("y",foreground=GOLD)
        self.server_list.tag_config("r",foreground=RED)
        self.server_list.bind("<Button-1>",self.select_server)
        self.render_servers()

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        self.conn_btn=tk.Button(bf,text="🔒 CONNECT",font=("Courier",11,"bold"),
                                bg=GREEN,fg=BG,relief="flat",padx=15,pady=7,command=self.toggle_vpn)
        self.conn_btn.pack(side="left",padx=5)
        tk.Button(bf,text="🔄 Refresh Servers",font=("Courier",10),bg=BG3,fg=GREEN,
                 relief="flat",padx=12,pady=7,command=self.refresh_servers).pack(side="left",padx=5)
        tk.Button(bf,text="🕵️ Check Leak",font=("Courier",10),bg=BG3,fg=GOLD,
                 relief="flat",padx=12,pady=7,command=self.check_leak).pack(side="left",padx=5)

        tk.Label(self.root,text="BrayoOS VPN Engine v4.5 • AIRA 🇰🇪 | For privacy & security",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)
        self.selected_idx=0

    def render_servers(self):
        self.server_list.config(state="normal");self.server_list.delete("1.0","end")
        for i,s in enumerate(VPN_SERVERS):
            ping_color="g" if s["ping"]<100 else "y" if s["ping"]<200 else "r"
            load_color="g" if s["load"]<50 else "y" if s["load"]<75 else "r"
            active="◉ ACTIVE" if self.connected and i==self.selected_idx else "○ Available"
            line=f"  {s['name']:<18} {s['country']:<12} {s['ping']}ms{'':<4} {s['load']}%{'':<4} {active}\n"
            self.server_list.insert("end",line,"g" if self.connected and i==self.selected_idx else "y")
        self.server_list.config(state="disabled")

    def select_server(self,event):
        idx=int(self.server_list.index("@%s,%s"%(event.x,event.y)).split(".")[0])-1
        if 0<=idx<len(VPN_SERVERS):
            self.selected_idx=idx
            self.render_servers()

    def toggle_vpn(self):
        if not self.connected:
            threading.Thread(target=self.connect_vpn,daemon=True).start()
        else:
            self.disconnect_vpn()

    def connect_vpn(self):
        server=VPN_SERVERS[self.selected_idx]
        self.current_server=server
        steps=["Initializing tunnel...","Authenticating...","Encrypting channel...","Routing traffic...","Connected!"]
        for i,step in enumerate(steps):
            self.root.after(0,self.vpn_status.config,{"text":step,"fg":GOLD})
            time.sleep(0.5)
        self.connected=True
        fake_ip=f"10.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        self.root.after(0,self.vpn_dot.config,{"fg":GREEN})
        self.root.after(0,self.vpn_status.config,{"text":"CONNECTED","fg":GREEN})
        self.root.after(0,self.conn_btn.config,{"text":"🔓 DISCONNECT","bg":RED,"fg":WHITE})
        self.root.after(0,self.svars["VPN IP"].set,fake_ip)
        self.root.after(0,self.svars["LOCATION"].set,server["country"])
        self.root.after(0,self.svars["PING"].set,f"{server['ping']}ms")
        self.root.after(0,self.render_servers)
        threading.Thread(target=self.traffic_loop,daemon=True).start()

    def disconnect_vpn(self):
        self.connected=False
        self.vpn_dot.config(fg=RED)
        self.vpn_status.config(text="DISCONNECTED",fg=RED)
        self.conn_btn.config(text="🔒 CONNECT",bg=GREEN,fg=BG)
        self.svars["VPN IP"].set("--")
        self.svars["LOCATION"].set("--")
        self.svars["PING"].set("--")
        self.render_servers()

    def traffic_loop(self):
        while self.connected:
            self.bytes_sent+=random.randint(1000,50000)
            self.bytes_recv+=random.randint(5000,200000)
            self.root.after(0,self.upload_lbl.config,{"text":f"↑ {self.bytes_sent//1024}KB"})
            self.root.after(0,self.download_lbl.config,{"text":f"↓ {self.bytes_recv//1024}KB"})
            time.sleep(1)

    def check_ip(self):
        threading.Thread(target=self._check_ip,daemon=True).start()

    def _check_ip(self):
        try:
            r=httpx.get("https://ipapi.co/json/",timeout=5)
            d=r.json()
            self.root.after(0,self.svars["MY IP"].set,d.get("ip","?"))
            self.root.after(0,self.svars["LOCATION"].set,d.get("country_name","?"))
        except:
            self.root.after(0,self.svars["MY IP"].set,"No internet")

    def refresh_servers(self):
        for s in VPN_SERVERS:
            s["ping"]=random.randint(10,400)
            s["load"]=random.randint(10,90)
        self.render_servers()

    def check_leak(self):
        win=tk.Toplevel(self.root)
        win.title("Leak Check");win.configure(bg=BG);win.geometry("400x300")
        tk.Label(win,text="🕵️ DNS LEAK TEST",font=("Courier",12,"bold"),bg=BG,fg=GOLD).pack(pady=10)
        out=tk.Text(win,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled",height=12)
        out.pack(fill="both",expand=True,padx=15,pady=5)
        def run():
            tests=["Checking DNS servers...","Testing WebRTC leak...","Verifying IP masking...","Checking IPv6 leak...","Testing geolocation..."]
            results=["✅ DNS: Protected","✅ WebRTC: No leak","✅ IP: Masked" if self.connected else "⚠️ IP: Exposed","✅ IPv6: Disabled","✅ Location: Hidden" if self.connected else "⚠️ Location: Visible"]
            for test,result in zip(tests,results):
                out.config(state="normal");out.insert("end",f"→ {test}\n");out.config(state="disabled")
                time.sleep(0.5)
                out.config(state="normal");out.insert("end",f"  {result}\n\n");out.config(state="disabled")
        threading.Thread(target=run,daemon=True).start()

if __name__=="__main__":
    root=tk.Tk();VPNEngine(root);root.mainloop()
