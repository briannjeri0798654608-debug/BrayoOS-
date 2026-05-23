import tkinter as tk
import threading,subprocess,os,json,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class PhoneController:
    def __init__(self,root):
        self.root=root
        self.root.title("📱 Phone Controller")
        self.root.geometry("680x580")
        self.root.configure(bg=BG)
        self.build_ui()
        self.refresh_status()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="📱 PHONE CONTROLLER",font=("Courier",14,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="AIRA controls your hardware",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True,padx=10,pady=8)
        left=tk.Frame(main,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(0,8))
        right=tk.Frame(main,bg=BG);right.pack(side="left",fill="both",expand=True)

        # CAMERA
        self.section(left,"📸 CAMERA",GOLD)
        cf=tk.Frame(left,bg=BG3);cf.pack(fill="x",pady=3)
        tk.Button(cf,text="📸 Take Photo (Front)",font=("Courier",9),bg=BG3,fg=GOLD,relief="flat",
                 padx=8,pady=5,command=lambda:self.run("termux-camera-photo -c 1 ~/Pictures/photo_front.jpg 2>/dev/null","📸 Front photo taken!")).pack(fill="x",padx=8,pady=2)
        tk.Button(cf,text="📸 Take Photo (Back)",font=("Courier",9),bg=BG3,fg=GOLD,relief="flat",
                 padx=8,pady=5,command=lambda:self.run("termux-camera-photo -c 0 ~/Pictures/photo_back.jpg 2>/dev/null","📸 Back photo taken!")).pack(fill="x",padx=8,pady=2)
        tk.Button(cf,text="🔦 Flashlight ON",font=("Courier",9),bg=BG3,fg=GOLD,relief="flat",
                 padx=8,pady=5,command=lambda:self.run("termux-torch on 2>/dev/null","🔦 Torch ON!")).pack(fill="x",padx=8,pady=2)
        tk.Button(cf,text="🔦 Flashlight OFF",font=("Courier",9),bg=BG3,fg=DIM,relief="flat",
                 padx=8,pady=5,command=lambda:self.run("termux-torch off 2>/dev/null","🔦 Torch OFF")).pack(fill="x",padx=8,pady=2)

        # COMMUNICATION
        self.section(left,"📞 COMMUNICATION",GREEN)
        phone_f=tk.Frame(left,bg=BG3);phone_f.pack(fill="x",pady=3)
        tk.Label(phone_f,text="Number:",font=("Courier",8),bg=BG3,fg=DIM).pack(anchor="w",padx=8,pady=(8,2))
        self.phone_e=tk.Entry(phone_f,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.phone_e.pack(fill="x",padx=8,ipady=5);self.phone_e.insert(0,"+254")
        tk.Label(phone_f,text="Message:",font=("Courier",8),bg=BG3,fg=DIM).pack(anchor="w",padx=8,pady=(5,2))
        self.sms_e=tk.Entry(phone_f,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.sms_e.pack(fill="x",padx=8,ipady=5);self.sms_e.insert(0,"Sent from BrayoOS!")
        bf2=tk.Frame(phone_f,bg=BG3);bf2.pack(fill="x",padx=8,pady=6)
        tk.Button(bf2,text="📞 Call",font=("Courier",9),bg=BG3,fg=GREEN,relief="flat",padx=10,pady=5,
                 command=self.make_call).pack(side="left",padx=3)
        tk.Button(bf2,text="💬 SMS",font=("Courier",9),bg=BG3,fg=NEON,relief="flat",padx=10,pady=5,
                 command=self.send_sms).pack(side="left",padx=3)

        # SENSORS
        self.section(right,"📊 SENSORS",CYAN)
        sf=tk.Frame(right,bg=BG3);sf.pack(fill="x",pady=3)
        self.sensor_vars={}
        for sensor in ["Battery","Location","Brightness","Network","Clipboard"]:
            row=tk.Frame(sf,bg=BG3);row.pack(fill="x",padx=8,pady=2)
            tk.Label(row,text=f"{sensor}:",font=("Courier",8),bg=BG3,fg=DIM,width=12,anchor="w").pack(side="left")
            v=tk.StringVar(value="Reading...")
            self.sensor_vars[sensor]=v
            tk.Label(row,text="",textvariable=v,font=("Courier",8,"bold"),bg=BG3,fg=CYAN).pack(side="left")
        tk.Button(sf,text="🔄 Refresh Sensors",font=("Courier",9),bg=BG3,fg=CYAN,
                 relief="flat",padx=8,pady=5,command=self.refresh_status).pack(fill="x",padx=8,pady=5)

        # CONTROLS
        self.section(right,"⚙️ DEVICE CONTROLS",PURPLE)
        ctrl_f=tk.Frame(right,bg=BG3);ctrl_f.pack(fill="x",pady=3)
        controls=[
            ("🔆 Brightness Max","termux-brightness 255 2>/dev/null","Max brightness!"),
            ("🔅 Brightness Min","termux-brightness 0 2>/dev/null","Min brightness!"),
            ("🔊 Volume Max","termux-volume music 15 2>/dev/null","Volume max!"),
            ("🔇 Volume Mute","termux-volume music 0 2>/dev/null","Muted!"),
            ("📳 Vibrate","termux-vibrate -d 500 2>/dev/null","Vibrating!"),
            ("🌐 Open Browser","termux-open-url https://github.com/briannjeri0798654608-debug/BrayoOS- 2>/dev/null","Opening BrayoOS GitHub!"),
        ]
        for label,cmd,msg in controls:
            tk.Button(ctrl_f,text=label,font=("Courier",8),bg=BG3,fg=PURPLE,relief="flat",
                     anchor="w",padx=8,pady=4,command=lambda c=cmd,m=msg:self.run(c,m)).pack(fill="x",padx=5,pady=1)

        # Log
        self.log_box=tk.Text(self.root,height=4,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="x",padx=10,pady=5)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        tk.Label(self.root,text="BrayoOS Phone Controller v4.5 • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def section(self,parent,title,color):
        tk.Label(parent,text=title,font=("Courier",9,"bold"),bg=BG,fg=color).pack(anchor="w",pady=(8,2))

    def log(self,msg,tag="g"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def run(self,cmd,msg):
        threading.Thread(target=lambda:subprocess.run(cmd,shell=True),daemon=True).start()
        self.log(msg)

    def make_call(self):
        phone=self.phone_e.get().strip()
        if phone:
            subprocess.Popen(f'termux-telephony-call {phone} 2>/dev/null',shell=True)
            self.log(f"📞 Calling {phone}...")

    def send_sms(self):
        phone=self.phone_e.get().strip()
        msg=self.sms_e.get().strip()
        if phone and msg:
            subprocess.Popen(f'termux-sms-send -n "{phone}" "{msg}" 2>/dev/null',shell=True)
            self.log(f"💬 SMS sent to {phone}")

    def refresh_status(self):
        threading.Thread(target=self._refresh,daemon=True).start()

    def _refresh(self):
        # Battery
        try:
            import json
            r=subprocess.check_output("termux-battery-status 2>/dev/null",shell=True,timeout=3).decode()
            d=json.loads(r)
            self.root.after(0,self.sensor_vars["Battery"].set,f"{d.get('percentage',0)}% {d.get('status','')}")
        except:self.root.after(0,self.sensor_vars["Battery"].set,"N/A")
        # Location
        try:
            r=subprocess.check_output("termux-location 2>/dev/null",shell=True,timeout=5).decode()
            d=json.loads(r)
            lat=d.get("latitude",0);lon=d.get("longitude",0)
            self.root.after(0,self.sensor_vars["Location"].set,f"{lat:.3f},{lon:.3f}")
        except:self.root.after(0,self.sensor_vars["Location"].set,"GPS off")
        # Clipboard
        try:
            r=subprocess.check_output("termux-clipboard-get 2>/dev/null",shell=True,timeout=2).decode()[:20]
            self.root.after(0,self.sensor_vars["Clipboard"].set,r or "Empty")
        except:self.root.after(0,self.sensor_vars["Clipboard"].set,"N/A")
        self.root.after(0,self.sensor_vars["Brightness"].set,"Controlled")
        self.root.after(0,self.sensor_vars["Network"].set,"Connected")

if __name__=="__main__":
    root=tk.Tk();PhoneController(root);root.mainloop()
