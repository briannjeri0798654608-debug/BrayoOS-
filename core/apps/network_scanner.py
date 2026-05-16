import tkinter as tk
import threading,subprocess,socket,os,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class NetworkScanner:
    def __init__(self,root):
        self.root=root
        self.root.title("📡 Network Scanner")
        self.root.geometry("650x540")
        self.root.configure(bg=BG)
        self.scanning=False
        self.devices=[]
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="📡 NETWORK SCANNER",font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Real-time WiFi device discovery",font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=5)
        self.svars={}
        for col,(lbl,color) in enumerate([("DEVICES",GREEN),("OPEN PORTS","#FF6600"),("MY IP",NEON),("GATEWAY",GOLD)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",11,"bold"),bg=BG3,fg=color).pack(pady=1)

        # Device list
        tk.Label(self.root,text="◈ DISCOVERED DEVICES",font=("Courier",10,"bold"),bg=BG,fg=NEON).pack(anchor="w",padx=15,pady=(8,2))
        cols_frame=tk.Frame(self.root,bg=BG2)
        cols_frame.pack(fill="x",padx=15)
        for col,width in [("IP ADDRESS",14),("MAC ADDRESS",18),("HOSTNAME",16),("STATUS",8)]:
            tk.Label(cols_frame,text=col,font=("Courier",8,"bold"),bg=BG2,fg=PURPLE,width=width,anchor="w").pack(side="left",padx=2)

        self.device_list=tk.Text(self.root,height=10,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.device_list.pack(fill="both",padx=15,pady=3)
        self.device_list.tag_config("g",foreground=GREEN)
        self.device_list.tag_config("y",foreground=GOLD)

        # Log
        tk.Label(self.root,text="◈ SCAN LOG",font=("Courier",9,"bold"),bg=BG,fg=NEON).pack(anchor="w",padx=15)
        self.log_box=tk.Text(self.root,height=5,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="x",padx=15,pady=3)

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        self.scan_btn=tk.Button(bf,text="▶ START SCAN",font=("Courier",10,"bold"),
                                bg=PURPLE,fg=WHITE,relief="flat",padx=12,pady=6,command=self.toggle_scan)
        self.scan_btn.pack(side="left",padx=4)
        tk.Button(bf,text="📋 Copy Results",font=("Courier",10,"bold"),bg=BG3,fg=NEON,
                 relief="flat",padx=12,pady=6,command=self.copy_results).pack(side="left",padx=4)
        tk.Button(bf,text="🗑 Clear",font=("Courier",10,"bold"),bg=BG3,fg=RED,
                 relief="flat",padx=12,pady=6,command=self.clear).pack(side="left",padx=4)

        tk.Label(self.root,text="BrayoOS Network Scanner • AIRA 🇰🇪",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)
        self.get_my_ip()

    def log(self,msg,tag=None):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def add_device(self,ip,mac,hostname,status):
        self.device_list.config(state="normal")
        line=f"  {ip:<15} {mac:<18} {hostname:<16} {status}\n"
        tag="g" if status=="ONLINE" else "y"
        self.device_list.insert("end",line,tag)
        self.device_list.see("end")
        self.device_list.config(state="disabled")

    def get_my_ip(self):
        threading.Thread(target=self._get_ip,daemon=True).start()

    def _get_ip(self):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("8.8.8.8",80))
            ip=s.getsockname()[0];s.close()
            self.root.after(0,self.svars["MY IP"].set,ip)
            # Get gateway
            gw=".".join(ip.split(".")[:3])+".1"
            self.root.after(0,self.svars["GATEWAY"].set,gw)
            self.subnet=".".join(ip.split(".")[:3])
        except:
            self.root.after(0,self.svars["MY IP"].set,"No WiFi")
            self.subnet="192.168.1"

    def toggle_scan(self):
        if not self.scanning:
            self.scanning=True
            self.scan_btn.config(text="⏹ STOP",bg=RED)
            self.device_list.config(state="normal");self.device_list.delete("1.0","end");self.device_list.config(state="disabled")
            self.devices=[]
            threading.Thread(target=self.scan,daemon=True).start()
        else:
            self.scanning=False
            self.scan_btn.config(text="▶ START SCAN",bg=PURPLE)

    def scan(self):
        self.root.after(0,self.log,"Starting network scan...")
        # Read ARP table first
        try:
            with open("/proc/net/arp") as f:
                lines=f.read().strip().split("\n")[1:]
            for line in lines:
                parts=line.split()
                if len(parts)>=4 and parts[0]!="0.0.0.0":
                    ip=parts[0];mac=parts[3]
                    try:host=socket.getfqdn(ip)
                    except:host="unknown"
                    self.devices.append(ip)
                    self.root.after(0,self.add_device,ip,mac,host,"ONLINE")
                    self.root.after(0,self.log,f"Found: {ip} [{mac}]")
        except Exception as e:
            self.root.after(0,self.log,f"ARP: {e}")

        # Ping sweep
        self.root.after(0,self.log,f"Scanning {self.subnet}.0/24...")
        found=len(self.devices)
        for i in range(1,20):
            if not self.scanning:break
            ip=f"{self.subnet}.{i}"
            if ip not in self.devices:
                try:
                    r=subprocess.run(["ping","-c","1","-W","1",ip],
                                    capture_output=True,timeout=2)
                    if r.returncode==0:
                        try:host=socket.getfqdn(ip)
                        except:host="unknown"
                        self.devices.append(ip)
                        self.root.after(0,self.add_device,ip,"unknown",host,"ONLINE")
                        self.root.after(0,self.log,f"Ping alive: {ip}")
                        found+=1
                except:pass

        self.root.after(0,self.svars["DEVICES"].set,str(found))
        self.root.after(0,self.log,f"Scan complete. {found} devices found.")
        self.scanning=False
        self.root.after(0,self.scan_btn.config,{"text":"▶ START SCAN","bg":PURPLE})

    def copy_results(self):
        content=self.device_list.get("1.0","end")
        self.root.clipboard_clear();self.root.clipboard_append(content)
        self.log("Results copied!")

    def clear(self):
        self.device_list.config(state="normal");self.device_list.delete("1.0","end");self.device_list.config(state="disabled")
        self.log_box.config(state="normal");self.log_box.delete("1.0","end");self.log_box.config(state="disabled")

if __name__=="__main__":
    root=tk.Tk()
    NetworkScanner(root)
    root.mainloop()
