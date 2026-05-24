import tkinter as tk
import threading,httpx,subprocess,os,json
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

class IPGrabber:
    def __init__(self,root):
        self.root=root
        self.root.title("🎯 IP Grabber & Tracker")
        self.root.geometry("680x560")
        self.root.configure(bg=BG)
        self.build_ui()
        self.get_my_ip()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🎯 IP GRABBER & TRACKER",font=("Courier",14,"bold"),bg=BG2,fg=RED).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="Full IP intelligence",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Frame(self.root,bg=RED,height=2).pack(fill="x")

        # My IP card
        my_f=tk.Frame(self.root,bg=BG3);my_f.pack(fill="x",padx=15,pady=8)
        tk.Label(my_f,text="MY IP ADDRESS",font=("Courier",9,"bold"),bg=BG3,fg=DIM).pack(anchor="w",padx=10,pady=(8,2))
        self.my_ip=tk.Label(my_f,text="Loading...",font=("Courier",18,"bold"),bg=BG3,fg=CYAN)
        self.my_ip.pack(anchor="w",padx=10)
        self.my_info=tk.Label(my_f,text="",font=("Courier",8),bg=BG3,fg=DIM)
        self.my_info.pack(anchor="w",padx=10,pady=(0,8))

        # Target input
        tk.Label(self.root,text="◈ TRACK ANY IP / DOMAIN",font=("Courier",9,"bold"),bg=BG,fg=RED).pack(anchor="w",padx=15,pady=(5,2))
        inf=tk.Frame(self.root,bg=BG3);inf.pack(fill="x",padx=15,pady=3)
        tk.Label(inf,text="TARGET:",font=("Courier",9,"bold"),bg=BG3,fg=RED).pack(side="left",padx=10,pady=8)
        self.target=tk.Entry(inf,font=("Courier",11),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.target.pack(side="left",fill="x",expand=True,ipady=8)
        self.target.bind("<Return>",lambda e:self.track())
        self.target.insert(0,"8.8.8.8")
        tk.Button(inf,text="🎯 TRACK",font=("Courier",10,"bold"),bg=RED,fg=WHITE,
                 relief="flat",padx=15,command=self.track).pack(side="right",padx=8,pady=5)

        # Quick targets
        qf=tk.Frame(self.root,bg=BG);qf.pack(fill="x",padx=15,pady=3)
        for t in ["8.8.8.8","1.1.1.1","google.com","github.com","facebook.com"]:
            tk.Button(qf,text=t,font=("Courier",7),bg=BG3,fg=NEON,relief="flat",
                     padx=5,pady=3,command=lambda x=t:self.quick_track(x)).pack(side="left",padx=2)

        # Results
        tk.Label(self.root,text="◈ INTELLIGENCE REPORT",font=("Courier",9,"bold"),bg=BG,fg=RED).pack(anchor="w",padx=15,pady=(6,2))
        self.results=tk.Text(self.root,height=14,bg=BG3,fg=WHITE,font=("Courier",9),
                            relief="flat",state="disabled")
        self.results.pack(fill="both",expand=True,padx=15,pady=3)
        self.results.tag_config("r",foreground=RED)
        self.results.tag_config("g",foreground=GREEN)
        self.results.tag_config("y",foreground=GOLD)
        self.results.tag_config("c",foreground=CYAN)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=5)
        tk.Button(bf,text="📋 Copy Report",font=("Courier",10),bg=BG3,fg=GREEN,
                 relief="flat",padx=12,pady=5,command=self.copy).pack(side="left",padx=4)
        tk.Button(bf,text="🗑 Clear",font=("Courier",10),bg=BG3,fg=DIM,
                 relief="flat",padx=10,pady=5,command=self.clear).pack(side="left",padx=4)
        tk.Label(self.root,text="BrayoOS IP Grabber v4.5 • AIRA 🇰🇪 | Ethical use only",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def log(self,msg,tag="g"):
        self.results.config(state="normal")
        self.results.insert("end",f"{msg}\n",tag)
        self.results.see("end")
        self.results.config(state="disabled")

    def get_my_ip(self):
        threading.Thread(target=self._get_my_ip,daemon=True).start()

    def _get_my_ip(self):
        try:
            r=httpx.get("https://ipapi.co/json/",timeout=6)
            d=r.json()
            ip=d.get("ip","?")
            city=d.get("city","?")
            country=d.get("country_name","?")
            org=d.get("org","?")
            self.root.after(0,self.my_ip.config,{"text":ip})
            self.root.after(0,self.my_info.config,{"text":f"{city}, {country} | {org}"})
        except:
            self.root.after(0,self.my_ip.config,{"text":"No connection"})

    def quick_track(self,target):
        self.target.delete(0,"end")
        self.target.insert(0,target)
        self.track()

    def track(self):
        t=self.target.get().strip()
        if not t:return
        self.results.config(state="normal");self.results.delete("1.0","end");self.results.config(state="disabled")
        threading.Thread(target=self._track,args=(t,),daemon=True).start()

    def _track(self,target):
        self.root.after(0,self.log,f"◈ TRACKING: {target}\n","c")

        # IP Geolocation
        try:
            r=httpx.get(f"https://ipapi.co/{target}/json/",timeout=8)
            d=r.json()
            fields=[
                ("IP Address",d.get("ip","?"),"c"),
                ("City",d.get("city","?"),"g"),
                ("Region",d.get("region","?"),"g"),
                ("Country",d.get("country_name","?"),"g"),
                ("Continent",d.get("continent_code","?"),"g"),
                ("Timezone",d.get("timezone","?"),"y"),
                ("ISP/Org",d.get("org","?"),"y"),
                ("ASN",d.get("asn","?"),"y"),
                ("Latitude",str(d.get("latitude","?")),"r"),
                ("Longitude",str(d.get("longitude","?")),"r"),
                ("Postal",d.get("postal","?"),"g"),
                ("Currency",d.get("currency","?"),"g"),
                ("Languages",d.get("languages","?"),"g"),
                ("Mobile",str(d.get("mobile","?")),"y"),
                ("Proxy/VPN",str(d.get("proxy","?")),"r"),
            ]
            self.root.after(0,self.log,"  GEOLOCATION DATA:","c")
            for k,v,tag in fields:
                self.root.after(0,self.log,f"  {k:<15} {v}",tag)
        except Exception as e:
            self.root.after(0,self.log,f"  Geolocation failed: {e}","r")

        # DNS Lookup
        self.root.after(0,self.log,"\n  DNS LOOKUP:","c")
        try:
            result=subprocess.check_output(f"nslookup {target} 2>/dev/null",shell=True,timeout=5).decode()
            for line in result.split("\n")[:6]:
                if line.strip():self.root.after(0,self.log,f"  {line.strip()}","y")
        except:self.root.after(0,self.log,"  DNS lookup failed","r")

        # Port scan
        self.root.after(0,self.log,"\n  QUICK PORT SCAN:","c")
        common_ports=[80,443,22,21,25,3306,8080,8443]
        for port in common_ports:
            try:
                import socket
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(0.5)
                result=s.connect_ex((target,port))
                s.close()
                status="OPEN" if result==0 else "CLOSED"
                tag="r" if result==0 else "g"
                service={80:"HTTP",443:"HTTPS",22:"SSH",21:"FTP",25:"SMTP",3306:"MySQL",8080:"HTTP-ALT",8443:"HTTPS-ALT"}.get(port,"?")
                self.root.after(0,self.log,f"  Port {port:<6} {service:<10} {status}",tag)
            except:pass

        self.root.after(0,self.log,"\n✅ Intelligence report complete!","g")

    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.results.get("1.0","end"))

    def clear(self):
        self.results.config(state="normal");self.results.delete("1.0","end");self.results.config(state="disabled")

if __name__=="__main__":
    root=tk.Tk();IPGrabber(root);root.mainloop()
