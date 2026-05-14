import tkinter as tk
import threading
import time
import subprocess
import os
import json
import httpx
import math
from datetime import datetime

BG="#080810"; BG2="#0D0D1A"; BG3="#12122A"
PURPLE="#9D00FF"; NEON="#CC44FF"; WHITE="#E0E0FF"
RED="#FF0044"; GREEN="#44FF88"; GOLD="#FFD700"; DIM="#444466"
CONFIG=os.path.expanduser("~/BrayoOS/memory/prox_lock.json")
os.makedirs(os.path.dirname(CONFIG), exist_ok=True)

class ProximityLock:
    def __init__(self, root):
        self.root=root
        self.root.title("🔒 Proximity Lock")
        self.root.geometry("480x520")
        self.root.configure(bg=BG)
        self.armed=False
        self.base=None
        self.pin="1337"
        self.rng=20
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🔒 PROXIMITY LOCK",
                 font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Locks if phone moves beyond range",
                 font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        sf=tk.Frame(self.root,bg=BG2)
        sf.pack(fill="x",padx=15,pady=5)
        self.dot=tk.Label(sf,text="⬤",font=("Courier",22),bg=BG2,fg=RED)
        self.dot.pack(side="left",padx=12,pady=8)
        sr=tk.Frame(sf,bg=BG2)
        sr.pack(side="left")
        self.slbl=tk.Label(sr,text="DISARMED",font=("Courier",13,"bold"),bg=BG2,fg=RED)
        self.slbl.pack(anchor="w")
        self.dlbl=tk.Label(sr,text="Base: Not set",font=("Courier",8),bg=BG2,fg=DIM)
        self.dlbl.pack(anchor="w")

        rf=tk.Frame(self.root,bg=BG3)
        rf.pack(fill="x",padx=15,pady=4)
        tk.Label(rf,text="RANGE (m):",font=("Courier",9,"bold"),bg=BG3,fg=PURPLE).pack(side="left",padx=8,pady=6)
        self.rng_v=tk.StringVar(value="20")
        tk.Entry(rf,textvariable=self.rng_v,font=("Courier",11),bg=BG,fg=WHITE,
                 insertbackground=NEON,relief="flat",width=6).pack(side="left",ipady=5)
        tk.Label(rf,text="   PIN:",font=("Courier",9,"bold"),bg=BG3,fg=PURPLE).pack(side="left")
        self.pin_v=tk.StringVar(value="1337")
        tk.Entry(rf,textvariable=self.pin_v,font=("Courier",11),bg=BG,fg=WHITE,
                 insertbackground=NEON,relief="flat",width=6,show="*").pack(side="left",ipady=5,padx=5)

        self.log_box=tk.Text(self.root,height=12,bg=BG3,fg=WHITE,
                              font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",padx=15,pady=5)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("y",foreground=GOLD)

        bf=tk.Frame(self.root,bg=BG)
        bf.pack(pady=8)
        self.arm_btn=tk.Button(bf,text="🔒 ARM",font=("Courier",11,"bold"),
                                bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=7,
                                command=self.toggle)
        self.arm_btn.pack(side="left",padx=5)
        tk.Button(bf,text="📍 SET BASE",font=("Courier",10,"bold"),
                  bg=BG3,fg=GREEN,relief="flat",padx=12,pady=7,
                  command=self.set_base).pack(side="left",padx=5)

        tk.Label(self.root,text="BrayoOS Proximity Lock • AIRA 🇰🇪",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)
        self.log("Ready — Set base location then ARM","y")

    def log(self,msg,tag="g"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def get_loc(self):
        try:
            r=httpx.get("https://ipapi.co/json/",timeout=8)
            d=r.json()
            return {"lat":float(d["latitude"]),"lon":float(d["longitude"]),"city":d.get("city","?")}
        except:
            return None

    def dist(self,la1,lo1,la2,lo2):
        R=6371000
        p1,p2=math.radians(la1),math.radians(la2)
        dp=math.radians(la2-la1)
        dl=math.radians(lo2-lo1)
        a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
        return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

    def set_base(self):
        self.log("Getting location...","y")
        threading.Thread(target=self._set_base,daemon=True).start()

    def _set_base(self):
        loc=self.get_loc()
        if loc:
            self.base=loc
            self.root.after(0,self.log,f"✅ Base: {loc['city']} ({loc['lat']:.4f},{loc['lon']:.4f})","g")
            self.root.after(0,self.dlbl.config,{"text":f"Base: {loc['city']}"})
        else:
            self.root.after(0,self.log,"❌ Location failed","r")

    def toggle(self):
        if not self.armed:
            if not self.base:
                self.log("⚠️ Set base location first!","r")
                return
            self.armed=True
            self.rng=int(self.rng_v.get() or 20)
            self.pin=self.pin_v.get() or "1337"
            self.arm_btn.config(text="🔓 DISARM",bg=RED)
            self.dot.config(fg=GREEN)
            self.slbl.config(text="ARMED",fg=GREEN)
            self.log(f"🔒 ARMED! Range: {self.rng}m","g")
            threading.Thread(target=self.monitor,daemon=True).start()
        else:
            self.ask_pin()

    def monitor(self):
        while self.armed:
            loc=self.get_loc()
            if loc and self.base:
                d=self.dist(self.base["lat"],self.base["lon"],loc["lat"],loc["lon"])
                self.root.after(0,self.dlbl.config,{"text":f"Distance: {d:.0f}m"})
                if d>self.rng:
                    self.root.after(0,self.log,f"🚨 MOVED {d:.0f}m — LOCKING!","r")
                    self.root.after(0,self.lock_screen)
                else:
                    self.root.after(0,self.log,f"✅ Safe: {d:.0f}m from base","g")
            time.sleep(30)

    def lock_screen(self):
        lk=tk.Toplevel(self.root)
        lk.attributes("-fullscreen",True)
        lk.configure(bg=BG)
        lk.attributes("-topmost",True)
        tk.Label(lk,text="🚨",font=("Courier",60),bg=BG,fg=RED).pack(pady=30)
        tk.Label(lk,text="DEVICE LOCKED",font=("Courier",22,"bold"),bg=BG,fg=RED).pack()
        tk.Label(lk,text="Moved beyond allowed range!",font=("Courier",10),bg=BG,fg=GOLD).pack(pady=5)
        pv=tk.StringVar()
        tk.Entry(lk,textvariable=pv,font=("Courier",18),bg=BG3,fg=WHITE,
                 relief="flat",show="*",justify="center",width=10).pack(pady=15,ipady=10)
        ml=tk.Label(lk,text="",font=("Courier",9),bg=BG,fg=RED)
        ml.pack()
        def chk():
            if pv.get()==self.pin:
                lk.destroy()
                self.log("✅ Unlocked","g")
            else:
                ml.config(text="❌ Wrong PIN!")
                pv.set("")
        tk.Button(lk,text="UNLOCK",font=("Courier",12,"bold"),
                  bg=PURPLE,fg=WHITE,relief="flat",padx=20,pady=8,
                  command=chk).pack(pady=10)
        subprocess.Popen("termux-vibrate -d 3000 2>/dev/null",shell=True)
        subprocess.Popen("termux-notification --title '🚨 ALERT' --content 'Device moved!' 2>/dev/null",shell=True)

    def ask_pin(self):
        w=tk.Toplevel(self.root)
        w.configure(bg=BG)
        w.geometry("280x180")
        tk.Label(w,text="PIN to disarm:",font=("Courier",10),bg=BG,fg=WHITE).pack(pady=15)
        pv=tk.StringVar()
        tk.Entry(w,textvariable=pv,font=("Courier",14),bg=BG3,fg=WHITE,
                 relief="flat",show="*",justify="center").pack(ipady=8,padx=20,fill="x")
        def ok():
            if pv.get()==self.pin:
                self.armed=False
                self.arm_btn.config(text="🔒 ARM",bg=PURPLE)
                self.dot.config(fg=RED)
                self.slbl.config(text="DISARMED",fg=RED)
                self.log("🔓 Disarmed","y")
                w.destroy()
            else:
                tk.Label(w,text="Wrong PIN!",font=("Courier",9),bg=BG,fg=RED).pack()
        tk.Button(w,text="OK",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                  relief="flat",command=ok).pack(pady=10)

if __name__=="__main__":
    root=tk.Tk()
    ProximityLock(root)
    root.mainloop()
