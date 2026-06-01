import tkinter as tk
import os,json,hashlib
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

LOCK_FILE=os.path.expanduser("~/BrayoOS/memory/app_locks.json")
os.makedirs(os.path.dirname(LOCK_FILE),exist_ok=True)

class AppLock:
    def __init__(self,root):
        self.root=root
        self.root.title("🔒 App Lock")
        self.root.geometry("580x520")
        self.root.configure(bg=BG)
        self.locks=self.load()
        self.build_ui()

    def load(self):
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE) as f:return json.load(f)
        return {"pin":hashlib.sha256("1337".encode()).hexdigest(),"locked":[]}

    def save(self):
        with open(LOCK_FILE,"w") as f:json.dump(self.locks,f,indent=2)

    def build_ui(self):
        tk.Label(self.root,text="🔒 APP LOCK",font=("Courier",16,"bold"),
                bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="PIN-protect any BrayoOS app",
                font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Apps to lock
        tk.Label(self.root,text="◈ SELECT APPS TO LOCK",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        apps=["aria_voice.py","dna_vault.py","ghost_mode.py",
              "dark_web_monitor.py","osint_suite.py","hack_terminal.py",
              "wifi_passwords.py","ip_grabber.py","surveillance.py",
              "quantum_vault.py","password_manager.py","file_encryptor.py"]
        self.app_vars={}
        af=tk.Frame(self.root,bg=BG3);af.pack(fill="x",padx=15,pady=5)
        for i,app in enumerate(apps):
            v=tk.BooleanVar(value=app in self.locks.get("locked",[]))
            self.app_vars[app]=v
            row,col=divmod(i,2)
            tk.Checkbutton(af,text=app.replace(".py",""),
                          variable=v,bg=BG3,fg=NEON,
                          selectcolor=PURPLE,activebackground=BG3,
                          font=("Courier",8)).grid(row=row,column=col,
                          padx=10,pady=3,sticky="w")

        # PIN change
        tk.Label(self.root,text="◈ CHANGE PIN",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(8,3))
        pf=tk.Frame(self.root,bg=BG3);pf.pack(fill="x",padx=15,pady=3)
        tk.Label(pf,text="New PIN:",font=("Courier",9),bg=BG3,fg=DIM).pack(side="left",padx=10,pady=8)
        self.pin_e=tk.Entry(pf,font=("Courier",11),bg=BG,fg=NEON,
                           insertbackground=NEON,relief="flat",show="*",width=10)
        self.pin_e.pack(side="left",ipady=6)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=10)
        tk.Button(bf,text="💾 SAVE LOCKS",font=("Courier",11,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=7,
                 command=self.save_locks).pack(side="left",padx=5)
        tk.Button(bf,text="🔓 UNLOCK ALL",font=("Courier",10),
                 bg=BG3,fg=GREEN,relief="flat",padx=12,pady=7,
                 command=self.unlock_all).pack(side="left",padx=5)

        self.status=tk.Label(self.root,text="",font=("Courier",9),bg=BG,fg=GREEN)
        self.status.pack()
        tk.Label(self.root,text="BrayoOS App Lock v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def save_locks(self):
        locked=[app for app,v in self.app_vars.items() if v.get()]
        self.locks["locked"]=locked
        pin=self.pin_e.get()
        if pin:self.locks["pin"]=hashlib.sha256(pin.encode()).hexdigest()
        self.save()
        self.status.config(text=f"✅ {len(locked)} apps locked!",fg=GREEN)

    def unlock_all(self):
        for v in self.app_vars.values():v.set(False)
        self.locks["locked"]=[]
        self.save()
        self.status.config(text="✅ All apps unlocked!",fg=GREEN)

if __name__=="__main__":
    root=tk.Tk();AppLock(root);root.mainloop()
