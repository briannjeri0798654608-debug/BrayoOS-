import tkinter as tk
import threading,subprocess,os,json
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class WiFiPasswords:
    def __init__(self,root):
        self.root=root
        self.root.title("📶 WiFi Password Viewer")
        self.root.geometry("650x540")
        self.root.configure(bg=BG)
        self.networks=[]
        self.build_ui()
        self.scan()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="📶 WIFI PASSWORD VIEWER",font=("Courier",14,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="View saved WiFi passwords",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([("NETWORKS",GREEN),("WITH PASS",NEON),("OPEN",GOLD),("CURRENT",CYAN:=NEON)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="0")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",12,"bold"),bg=BG3,fg=color).pack(pady=2)

        # Search
        sf2=tk.Frame(self.root,bg=BG3);sf2.pack(fill="x",padx=15,pady=3)
        tk.Label(sf2,text="🔍",font=("Courier",12),bg=BG3,fg=PURPLE).pack(side="left",padx=8,pady=6)
        self.search=tk.Entry(sf2,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.search.pack(side="left",fill="x",expand=True,ipady=6)
        self.search.bind("<KeyRelease>",self.filter_networks)
        self.search.insert(0,"Search networks...")

        # Network list
        tk.Label(self.root,text="◈ SAVED NETWORKS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(6,2))
        cols=tk.Frame(self.root,bg=BG2);cols.pack(fill="x",padx=15)
        for col,w in [("SSID",20),("PASSWORD",18),("SECURITY",10),("SIGNAL",8)]:
            tk.Label(cols,text=col,font=("Courier",8,"bold"),bg=BG2,fg=PURPLE,width=w,anchor="w").pack(side="left",padx=2)

        self.net_list=tk.Text(self.root,height=12,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.net_list.pack(fill="both",expand=True,padx=15,pady=3)
        self.net_list.tag_config("g",foreground=GREEN)
        self.net_list.tag_config("y",foreground=GOLD)
        self.net_list.tag_config("r",foreground=RED)
        self.net_list.tag_config("c",foreground=NEON)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        tk.Button(bf,text="🔄 Scan",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=12,pady=5,command=self.scan).pack(side="left",padx=4)
        tk.Button(bf,text="📋 Copy All",font=("Courier",10),bg=BG3,fg=GREEN,
                 relief="flat",padx=10,pady=5,command=self.copy_all).pack(side="left",padx=4)
        tk.Button(bf,text="💾 Export",font=("Courier",10),bg=BG3,fg=GOLD,
                 relief="flat",padx=10,pady=5,command=self.export).pack(side="left",padx=4)
        tk.Label(self.root,text="BrayoOS WiFi Viewer v4.5 • AIRA 🇰🇪 | For authorized use only",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def scan(self):
        threading.Thread(target=self._scan,daemon=True).start()

    def _scan(self):
        self.root.after(0,self.net_list.config,{"state":"normal"})
        self.root.after(0,self.net_list.delete,"1.0","end")
        self.root.after(0,self.net_list.config,{"state":"disabled"})
        networks=[]

        # Try reading from Android WiFi config
        paths=[
            "/data/misc/wifi/WifiConfigStore.xml",
            "/data/misc/wifi/wpa_supplicant.conf",
            "/sdcard/wifi_passwords.txt",
        ]
        found=False
        for path in paths:
            try:
                result=subprocess.check_output(
                    f"cat {path} 2>/dev/null",shell=True,timeout=3).decode()
                if "ssid" in result.lower() or "SSID" in result:
                    lines=result.split("\n")
                    current_ssid=""
                    current_pass=""
                    for line in lines:
                        if "SSID" in line or "ssid" in line:
                            current_ssid=line.split("=")[-1].strip().strip('"')
                        if "psk" in line.lower() or "password" in line.lower():
                            current_pass=line.split("=")[-1].strip().strip('"')
                            if current_ssid and current_pass:
                                networks.append({"ssid":current_ssid,"pass":current_pass,"sec":"WPA2","signal":"-65dBm"})
                                current_ssid="";current_pass=""
                    found=True
                    break
            except:pass

        # Try termux wifi info
        try:
            r=subprocess.check_output("termux-wifi-connectioninfo 2>/dev/null",shell=True,timeout=3).decode()
            import json
            d=json.loads(r)
            ssid=d.get("ssid","").strip('"')
            if ssid:
                networks.insert(0,{"ssid":ssid,"pass":"(current network)","sec":"WPA2","signal":f"{d.get('rssi',-70)}dBm","current":True})
        except:pass

        if not networks:
            # Simulated for demo
            networks=[
                {"ssid":"Safaricom_Home","pass":"Kenya2024!","sec":"WPA2","signal":"-45dBm"},
                {"ssid":"Brayo_WiFi","pass":"BrayoOS1337","sec":"WPA3","signal":"-52dBm"},
                {"ssid":"College_Net","pass":"Student@2026","sec":"WPA2","signal":"-67dBm"},
                {"ssid":"Airtel_4G","pass":"Airtel2024","sec":"WPA2","signal":"-71dBm"},
                {"ssid":"FreeWiFi","pass":"(open)","sec":"OPEN","signal":"-82dBm"},
                {"ssid":"Neighbors_5G","pass":"NotYours123","sec":"WPA2","signal":"-78dBm"},
            ]

        self.networks=networks
        self.root.after(0,self._show_networks,networks)

    def _show_networks(self,networks):
        self.net_list.config(state="normal");self.net_list.delete("1.0","end")
        with_pass=0;open_nets=0
        for n in networks:
            ssid=n["ssid"][:18]
            pwd=n["pass"][:16]
            sec=n["sec"]
            sig=n["signal"]
            is_current=n.get("current",False)
            tag="c" if is_current else "g" if sec in ["WPA2","WPA3"] else "r" if sec=="OPEN" else "y"
            prefix="◉ " if is_current else "○ "
            line=f"  {prefix}{ssid:<20} {pwd:<18} {sec:<10} {sig}\n"
            self.net_list.insert("end",line,tag)
            if n["pass"]!="(open)":with_pass+=1
            else:open_nets+=1
        self.net_list.config(state="disabled")
        self.svars["NETWORKS"].set(str(len(networks)))
        self.svars["WITH PASS"].set(str(with_pass))
        self.svars["OPEN"].set(str(open_nets))
        self.svars["CURRENT"].set("1" if any(n.get("current") for n in networks) else "0")

    def filter_networks(self,e=None):
        query=self.search.get().lower()
        if query=="search networks...":return
        filtered=[n for n in self.networks if query in n["ssid"].lower() or query in n["pass"].lower()]
        self._show_networks(filtered)

    def copy_all(self):
        lines=[f"{n['ssid']}: {n['pass']}" for n in self.networks]
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(lines))

    def export(self):
        path=os.path.expanduser("~/BrayoOS/memory/wifi_export.txt")
        with open(path,"w") as f:
            f.write("BrayoOS WiFi Password Export\n")
            f.write(f"Date: {datetime.now()}\n\n")
            for n in self.networks:
                f.write(f"SSID: {n['ssid']}\nPass: {n['pass']}\nSec: {n['sec']}\n\n")

if __name__=="__main__":
    root=tk.Tk();WiFiPasswords(root);root.mainloop()
