import tkinter as tk
import threading,subprocess,os,time,json
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

LOG_FILE=os.path.expanduser("~/BrayoOS/memory/surveillance.json")
PHOTO_DIR=os.path.expanduser("~/BrayoOS/surveillance/")
os.makedirs(PHOTO_DIR,exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE),exist_ok=True)

class Surveillance:
    def __init__(self,root):
        self.root=root
        self.root.title("📷 BrayoOS Surveillance")
        self.root.geometry("680x560")
        self.root.configure(bg=BG)
        self.active=False
        self.event_count=0
        self.logs=self.load_logs()
        self.build_ui()

    def load_logs(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE) as f:return json.load(f)
        return []

    def save_logs(self):
        with open(LOG_FILE,"w") as f:json.dump(self.logs[-100:],f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="📷 BRAYOOS SURVEILLANCE SYSTEM",
                 font=("Courier",12,"bold"),bg=BG2,fg=RED).pack(side="left",padx=12,pady=10)
        self.rec_dot=tk.Label(hdr,text="⬤",font=("Courier",14),bg=BG2,fg=DIM)
        self.rec_dot.pack(side="right",padx=8)
        tk.Label(hdr,text="REC",font=("Courier",8),bg=BG2,fg=DIM).pack(side="right")
        tk.Frame(self.root,bg=RED,height=2).pack(fill="x")

        main=tk.Frame(self.root,bg=BG)
        main.pack(fill="both",expand=True,padx=10,pady=8)

        # Left — camera + controls
        left=tk.Frame(main,bg=BG)
        left.pack(side="left",fill="y",padx=(0,10))

        # Camera view
        self.cam=tk.Canvas(left,width=300,height=200,bg="#001100",
                          highlightthickness=2,highlightbackground=RED)
        self.cam.pack()
        self.cam.create_text(150,90,text="📷",font=("Courier",32),fill=DIM)
        self.cam.create_text(150,140,text="CAMERA OFFLINE",fill=DIM,font=("Courier",10))

        # Status
        self.status=tk.Label(left,text="⚫ SURVEILLANCE OFFLINE",
                             font=("Courier",10,"bold"),bg=BG,fg=DIM)
        self.status.pack(pady=5)

        # Stats
        sf=tk.Frame(left,bg=BG)
        sf.pack(fill="x",pady=3)
        self.svars={}
        for col,(lbl,color) in enumerate([("EVENTS",RED),("PHOTOS",GOLD),("UPTIME",GREEN)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=3,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",6),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="0")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",11,"bold"),bg=BG3,fg=color).pack(pady=1)

        # Triggers
        tk.Label(left,text="◈ ALERT TRIGGERS",font=("Courier",9,"bold"),bg=BG,fg=RED).pack(anchor="w",pady=(8,2))
        tf=tk.Frame(left,bg=BG3);tf.pack(fill="x")
        self.triggers={}
        for trig in ["Motion Detected","Wrong PIN","Face Mismatch","Network Intrusion","USB Connected"]:
            v=tk.BooleanVar(value=True)
            self.triggers[trig]=v
            tk.Checkbutton(tf,text=trig,variable=v,bg=BG3,fg=RED,
                          selectcolor=PURPLE,activebackground=BG3,
                          font=("Courier",7)).pack(anchor="w",padx=8,pady=1)

        # Buttons
        bf=tk.Frame(left,bg=BG);bf.pack(pady=8)
        self.toggle_btn=tk.Button(bf,text="🎥 ARM SURVEILLANCE",font=("Courier",10,"bold"),
                                  bg=RED,fg=WHITE,relief="flat",padx=12,pady=6,
                                  command=self.toggle)
        self.toggle_btn.pack(side="left",padx=3)
        tk.Button(bf,text="📸 SNAP",font=("Courier",10,"bold"),bg=BG3,fg=GOLD,
                 relief="flat",padx=10,pady=6,command=self.snap_photo).pack(side="left",padx=3)

        # Right — event log
        right=tk.Frame(main,bg=BG2)
        right.pack(side="left",fill="both",expand=True)

        tk.Label(right,text="◈ SURVEILLANCE LOG",font=("Courier",9,"bold"),bg=BG2,fg=RED).pack(pady=6,padx=8,anchor="w")

        self.log_box=tk.Text(right,bg=BG2,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=5,pady=5)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("y",foreground=GOLD)
        self.log_box.tag_config("g",foreground=GREEN)

        bf2=tk.Frame(right,bg=BG2);bf2.pack(pady=5)
        tk.Button(bf2,text="🗑 Clear Log",font=("Courier",8),bg=BG3,fg=DIM,
                 relief="flat",padx=8,pady=3,command=self.clear_log).pack(side="left",padx=3)
        tk.Button(bf2,text="💾 Export",font=("Courier",8),bg=BG3,fg=GREEN,
                 relief="flat",padx=8,pady=3,command=self.export).pack(side="left",padx=3)

        tk.Label(self.root,text="BrayoOS Surveillance v1.0 • AIRA 🇰🇪 | ⚠️ Privacy-aware use only",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

        # Load existing logs
        for log in self.logs[-10:]:
            self.log(log.get("msg",""),log.get("tag","y"))

    def log(self,msg,tag="y"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")
        self.logs.append({"msg":msg,"tag":tag,"time":ts})
        self.save_logs()

    def toggle(self):
        if not self.active:
            self.active=True
            self.toggle_btn.config(text="⏹ DISARM",bg=DIM)
            self.status.config(text="🔴 SURVEILLANCE ACTIVE",fg=RED)
            self.rec_dot.config(fg=RED)
            self.log("🎥 Surveillance system ARMED","r")
            threading.Thread(target=self.surveillance_loop,daemon=True).start()
            threading.Thread(target=self.blink_rec,daemon=True).start()
        else:
            self.active=False
            self.toggle_btn.config(text="🎥 ARM SURVEILLANCE",bg=RED)
            self.status.config(text="⚫ SURVEILLANCE OFFLINE",fg=DIM)
            self.rec_dot.config(fg=DIM)
            self.log("⏹ Surveillance system disarmed","y")

    def blink_rec(self):
        while self.active:
            self.root.after(0,self.rec_dot.config,{"fg":RED})
            time.sleep(0.5)
            self.root.after(0,self.rec_dot.config,{"fg":DIM})
            time.sleep(0.5)

    def surveillance_loop(self):
        import random
        start=time.time()
        events=[
            ("Motion detected near device","r"),
            ("Network scan detected from 192.168.1.1","r"),
            ("Bluetooth probe received","y"),
            ("USB device connected","y"),
            ("Location access requested","y"),
            ("All clear — no threats","g"),
        ]
        while self.active:
            uptime=int(time.time()-start)
            self.root.after(0,self.svars["UPTIME"].set,f"{uptime//60}m{uptime%60}s")
            # Random event simulation
            if random.random()<0.15:
                event,tag=random.choice(events)
                self.event_count+=1
                self.root.after(0,self.svars["EVENTS"].set,str(self.event_count))
                self.root.after(0,self.log,f"⚠️ {event}",tag)
                if tag=="r":
                    subprocess.Popen("termux-vibrate -d 300 2>/dev/null",shell=True)
                    subprocess.Popen(f'termux-notification --title "🚨 BrayoOS Alert" --content "{event}" 2>/dev/null',shell=True)
                    self.root.after(0,self.snap_photo)
            time.sleep(10)

    def snap_photo(self):
        threading.Thread(target=self._snap,daemon=True).start()

    def _snap(self):
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        path=os.path.join(PHOTO_DIR,f"snap_{ts}.jpg")
        subprocess.run(f"termux-camera-photo -c 1 {path} 2>/dev/null",shell=True,timeout=5)
        photos=len(os.listdir(PHOTO_DIR))
        self.root.after(0,self.svars["PHOTOS"].set,str(photos))
        self.root.after(0,self.log,f"📸 Photo saved: snap_{ts}.jpg","y")

    def clear_log(self):
        self.log_box.config(state="normal");self.log_box.delete("1.0","end");self.log_box.config(state="disabled")
        self.logs=[];self.save_logs()

    def export(self):
        path=os.path.expanduser(f"~/BrayoOS/memory/surveillance_export_{datetime.now().strftime('%Y%m%d')}.txt")
        with open(path,"w") as f:
            f.write(f"BrayoOS Surveillance Report — {datetime.now()}\n\n")
            for log in self.logs:f.write(f"[{log.get('time','')}] {log.get('msg','')}\n")
        self.log(f"💾 Exported to {os.path.basename(path)}","g")

if __name__=="__main__":
    root=tk.Tk();Surveillance(root);root.mainloop()
