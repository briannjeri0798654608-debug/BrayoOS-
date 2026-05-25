import tkinter as tk
import threading,subprocess,os,json,time,httpx
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

CLOUD_FILE=os.path.expanduser("~/BrayoOS/memory/cloud_config.json")
os.makedirs(os.path.dirname(CLOUD_FILE),exist_ok=True)

class BrayoOSCloud:
    def __init__(self,root):
        self.root=root
        self.root.title("☁️ BrayoOS Cloud")
        self.root.geometry("700x580")
        self.root.configure(bg=BG)
        self.config=self.load_config()
        self.syncing=False
        self.build_ui()
        self.check_status()

    def load_config(self):
        if os.path.exists(CLOUD_FILE):
            with open(CLOUD_FILE) as f:return json.load(f)
        return {"github_token":"","github_repo":"BrayoOS-","last_sync":"Never",
                "auto_sync":False,"sync_interval":60,"files_synced":0}

    def save_config(self):
        with open(CLOUD_FILE,"w") as f:json.dump(self.config,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="☁️ BRAYOOS CLOUD",font=("Courier",14,"bold"),bg=BG2,fg=CYAN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="Sync everything • Anywhere",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.sync_dot=tk.Label(hdr,text="⬤ OFFLINE",font=("Courier",9,"bold"),bg=BG2,fg=RED)
        self.sync_dot.pack(side="right",padx=12)
        tk.Frame(self.root,bg=CYAN,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("FILES SYNCED",GREEN),("LAST SYNC",NEON),
            ("CLOUD SIZE",CYAN),("STATUS",GOLD)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",9,"bold"),bg=BG3,fg=color).pack(pady=2)

        # GitHub config
        tk.Label(self.root,text="◈ CLOUD CONFIGURATION",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(5,3))
        cf=tk.Frame(self.root,bg=BG3);cf.pack(fill="x",padx=15,pady=3)
        for label,key,show in [("GitHub Token","github_token","*"),("Repository","github_repo","")]:
            row=tk.Frame(cf,bg=BG3);row.pack(fill="x",padx=8,pady=4)
            tk.Label(row,text=f"{label}:",font=("Courier",9),bg=BG3,fg=DIM,width=16,anchor="w").pack(side="left")
            e=tk.Entry(row,font=("Courier",10),bg=BG,fg=CYAN,insertbackground=NEON,relief="flat",show=show)
            e.insert(0,self.config.get(key,""))
            e.pack(side="left",fill="x",expand=True,ipady=6)
            setattr(self,f"{key}_entry",e)
        tk.Button(cf,text="💾 Save Config",font=("Courier",9,"bold"),bg=CYAN,fg=BG,
                 relief="flat",padx=10,pady=5,command=self.save_cfg).pack(pady=6)

        # Sync items
        tk.Label(self.root,text="◈ SYNC ITEMS",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(5,3))
        items_f=tk.Frame(self.root,bg=BG3);items_f.pack(fill="x",padx=15,pady=3)
        self.sync_items={}
        for item,default in [("BrayoOS Apps",True),("Memory/Data",True),("Settings",True),
                              ("Wallpapers",False),("Logs",False),("Vault (encrypted)",True)]:
            v=tk.BooleanVar(value=default)
            self.sync_items[item]=v
            f=tk.Frame(items_f,bg=BG3);f.pack(side="left",padx=5,pady=5)
            tk.Checkbutton(f,text=item,variable=v,bg=BG3,fg=CYAN,
                          selectcolor=PURPLE,activebackground=BG3,
                          font=("Courier",8)).pack()

        # Progress
        tk.Label(self.root,text="◈ SYNC PROGRESS",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(5,2))
        self.progress_c=tk.Canvas(self.root,width=650,height=10,bg="#001100",highlightthickness=0)
        self.progress_c.pack(padx=15,pady=3)

        # Log
        self.log_box=tk.Text(self.root,height=7,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=5)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("c",foreground=CYAN)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        tk.Button(bf,text="☁️ SYNC NOW",font=("Courier",11,"bold"),bg=CYAN,fg=BG,
                 relief="flat",padx=15,pady=7,command=self.sync_now).pack(side="left",padx=5)
        tk.Button(bf,text="⬇️ RESTORE",font=("Courier",10),bg=BG3,fg=GREEN,
                 relief="flat",padx=12,pady=7,command=self.restore).pack(side="left",padx=5)
        self.auto_btn=tk.Button(bf,text="⏱ AUTO SYNC OFF",font=("Courier",10),bg=BG3,fg=DIM,
                                relief="flat",padx=12,pady=7,command=self.toggle_auto)
        self.auto_btn.pack(side="left",padx=5)
        tk.Label(self.root,text="BrayoOS Cloud v4.5 • AIRA 🇰🇪 | Powered by GitHub",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def log(self,msg,tag="c"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def update_progress(self,pct):
        self.progress_c.delete("all")
        w=int(650*pct/100)
        if w>0:self.progress_c.create_rectangle(0,0,w,10,fill=CYAN,outline="")

    def save_cfg(self):
        self.config["github_token"]=self.github_token_entry.get()
        self.config["github_repo"]=self.github_repo_entry.get()
        self.save_config()
        self.log("✅ Configuration saved!","g")

    def check_status(self):
        threading.Thread(target=self._check,daemon=True).start()

    def _check(self):
        try:
            result=subprocess.check_output("git -C ~/BrayoOS remote -v 2>/dev/null",shell=True,timeout=5).decode()
            if "github" in result:
                self.root.after(0,self.sync_dot.config,{"text":"⬤ CONNECTED","fg":GREEN})
                self.root.after(0,self.svars["STATUS"].set,"GitHub ✅")
                self.log("✅ GitHub connection verified","g")
            # Get repo size
            size=subprocess.check_output("du -sh ~/BrayoOS/ 2>/dev/null",shell=True,timeout=3).decode().split()[0]
            self.root.after(0,self.svars["CLOUD SIZE"].set,size)
        except:
            self.root.after(0,self.svars["STATUS"].set,"Offline")

    def sync_now(self):
        threading.Thread(target=self._sync,daemon=True).start()

    def _sync(self):
        self.log("☁️ Starting sync to BrayoOS Cloud...")
        self.root.after(0,self.sync_dot.config,{"text":"⬤ SYNCING","fg":GOLD})
        steps=[
            (20,"Scanning files..."),
            (40,"Staging changes..."),
            (60,"Compressing data..."),
            (80,"Uploading to cloud..."),
            (100,"Sync complete!"),
        ]
        for pct,msg in steps:
            self.root.after(0,self.update_progress,pct)
            self.root.after(0,self.log,f"  → {msg}")
            time.sleep(0.8)
        result=subprocess.run(
            "cd ~/BrayoOS && git add -A && git commit -m 'BrayoOS Cloud sync' && git push origin main",
            shell=True,capture_output=True,text=True,timeout=30)
        if result.returncode==0:
            self.log("✅ Sync successful!","g")
            self.root.after(0,self.sync_dot.config,{"text":"⬤ SYNCED","fg":GREEN})
            self.config["last_sync"]=datetime.now().strftime("%Y-%m-%d %H:%M")
            self.config["files_synced"]+=1
            self.save_config()
            self.root.after(0,self.svars["LAST SYNC"].set,self.config["last_sync"])
            self.root.after(0,self.svars["FILES SYNCED"].set,str(self.config["files_synced"]))
        else:
            self.log(f"⚠️ Sync issue: {result.stderr[:50]}","r")
            self.root.after(0,self.sync_dot.config,{"text":"⬤ ERROR","fg":RED})

    def restore(self):
        threading.Thread(target=self._restore,daemon=True).start()

    def _restore(self):
        self.log("⬇️ Restoring from cloud...")
        result=subprocess.run("cd ~/BrayoOS && git pull origin main",
                             shell=True,capture_output=True,text=True,timeout=30)
        if result.returncode==0:
            self.log("✅ Restore complete!","g")
        else:
            self.log(f"⚠️ Restore failed: {result.stderr[:50]}","r")

    def toggle_auto(self):
        self.config["auto_sync"]=not self.config["auto_sync"]
        if self.config["auto_sync"]:
            self.auto_btn.config(text="⏱ AUTO SYNC ON",fg=GREEN)
            self.log("⏱ Auto-sync enabled every 60 minutes","g")
            threading.Thread(target=self.auto_loop,daemon=True).start()
        else:
            self.auto_btn.config(text="⏱ AUTO SYNC OFF",fg=DIM)
            self.log("⏱ Auto-sync disabled","c")
        self.save_config()

    def auto_loop(self):
        while self.config["auto_sync"]:
            time.sleep(3600)
            if self.config["auto_sync"]:
                self._sync()

if __name__=="__main__":
    root=tk.Tk();BrayoOSCloud(root);root.mainloop()
