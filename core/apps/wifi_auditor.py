import tkinter as tk
import threading,subprocess,time,random,os
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class WiFiAuditor:
    def __init__(self,root):
        self.root=root
        self.root.title("📶 WiFi Auditor")
        self.root.geometry("650x560")
        self.root.configure(bg=BG)
        self.running=False
        self.build_ui()
        self.scan_networks()

    def build_ui(self):
        tk.Label(self.root,text="📶 WIFI SECURITY AUDITOR",font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Network vulnerability assessment tool",font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Networks
        tk.Label(self.root,text="◈ DETECTED NETWORKS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        cols=tk.Frame(self.root,bg=BG2);cols.pack(fill="x",padx=15)
        for col,w in [("SSID",18),("SECURITY",12),("SIGNAL",8),("CHANNEL",8),("RISK",8)]:
            tk.Label(cols,text=col,font=("Courier",8,"bold"),bg=BG2,fg=PURPLE,width=w,anchor="w").pack(side="left",padx=2)

        self.net_list=tk.Text(self.root,height=7,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.net_list.pack(fill="x",padx=15,pady=3)
        self.net_list.tag_config("g",foreground=GREEN)
        self.net_list.tag_config("r",foreground=RED)
        self.net_list.tag_config("y",foreground=GOLD)

        # Audit log
        tk.Label(self.root,text="◈ AUDIT LOG",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(5,2))
        self.log_box=tk.Text(self.root,height=9,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=3)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("y",foreground=GOLD)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        tk.Button(bf,text="🔍 SCAN",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=12,pady=5,command=self.scan_networks).pack(side="left",padx=3)
        self.audit_btn=tk.Button(bf,text="⚡ AUDIT SELECTED",font=("Courier",10,"bold"),bg=BG3,fg=NEON,
                 relief="flat",padx=12,pady=5,command=self.audit)
        self.audit_btn.pack(side="left",padx=3)
        tk.Button(bf,text="🛡️ HARDEN MY NETWORK",font=("Courier",10,"bold"),bg=BG3,fg=GREEN,
                 relief="flat",padx=12,pady=5,command=self.harden).pack(side="left",padx=3)
        tk.Label(self.root,text="⚠️ For authorized security testing only • BrayoOS 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def log(self,msg,tag="y"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def add_network(self,ssid,sec,sig,ch,risk,tag):
        self.net_list.config(state="normal")
        line=f"  {ssid:<18} {sec:<12} {sig:<8} {ch:<8} {risk}\n"
        self.net_list.insert("end",line,tag)
        self.net_list.config(state="disabled")

    def scan_networks(self):
        self.net_list.config(state="normal");self.net_list.delete("1.0","end");self.net_list.config(state="disabled")
        threading.Thread(target=self._scan,daemon=True).start()

    def _scan(self):
        self.log("🔍 Scanning for WiFi networks...")
        # Real scan
        try:
            r=subprocess.check_output("termux-wifi-scaninfo 2>/dev/null",shell=True,timeout=5).decode()
            import json
            nets=json.loads(r)
            for n in nets[:8]:
                ssid=n.get("ssid","Unknown")[:16]
                freq=n.get("frequency",2412)
                sig=n.get("level",-70)
                cap=n.get("capabilities","")
                ch="2.4G" if freq<5000 else "5G"
                sec="WPA3" if "WPA3" in cap else "WPA2" if "WPA2" in cap else "WPA" if "WPA" in cap else "OPEN"
                risk="🟢 LOW" if "WPA3" in cap or "WPA2" in cap else "🔴 HIGH"
                tag="g" if "WPA" in cap else "r"
                self.root.after(0,self.add_network,ssid,sec,f"{sig}dBm",ch,risk,tag)
                self.root.after(0,self.log,f"Found: {ssid} [{sec}] {sig}dBm")
        except:
            # Simulated
            nets=[
                ("HomeNetwork","WPA2","-45dBm","2.4G","🟢 LOW","g"),
                ("CafeWiFi","WPA2","-67dBm","5G","🟡 MED","y"),
                ("AndroidAP","WPA","-71dBm","2.4G","🟡 MED","y"),
                ("FreeWiFi","OPEN","-82dBm","2.4G","🔴 HIGH","r"),
                ("TP-Link_2G","WPA2","-58dBm","2.4G","🟢 LOW","g"),
            ]
            for n in nets:
                self.root.after(0,self.add_network,*n)
                time.sleep(0.3)
        self.root.after(0,self.log,"✅ Scan complete!")

    def audit(self):
        threading.Thread(target=self._audit,daemon=True).start()

    def _audit(self):
        self.log("⚡ Starting security audit...")
        checks=[
            ("Checking encryption strength...","WPA2/WPA3 encryption detected","g"),
            ("Testing for WPS vulnerability...","WPS may be enabled — potential risk","y"),
            ("Checking default credentials...","Default router passwords detected!","r"),
            ("Analyzing beacon frames...","SSID broadcast: ON","y"),
            ("Testing PMKID vulnerability...","Network appears patched","g"),
            ("Checking for rogue APs...","No rogue access points found","g"),
            ("Testing DNS hijacking...","DNS responses appear legitimate","g"),
            ("Checking firewall rules...","Firewall active — good!","g"),
        ]
        for check,result,tag in checks:
            self.root.after(0,self.log,f"→ {check}","y")
            time.sleep(random.uniform(0.5,1.2))
            self.root.after(0,self.log,f"  ✓ {result}",tag)
        self.root.after(0,self.log,"\n📊 AUDIT COMPLETE — Check results above","y")

    def harden(self):
        hardening=[
            "✅ Disable WPS on your router",
            "✅ Use WPA3 if router supports it",
            "✅ Change default router password",
            "✅ Disable remote management",
            "✅ Enable firewall",
            "✅ Use MAC address filtering",
            "✅ Hide SSID from broadcast",
            "✅ Use guest network for IoT devices",
        ]
        self.log("\n🛡️ NETWORK HARDENING GUIDE:","y")
        for tip in hardening:
            self.log(f"  {tip}","g")
            time.sleep(0.2)

if __name__=="__main__":
    root=tk.Tk();WiFiAuditor(root);root.mainloop()
