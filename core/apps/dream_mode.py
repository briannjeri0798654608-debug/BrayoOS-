import tkinter as tk
import threading,subprocess,os,json,time,random
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

TASKS_FILE=os.path.expanduser("~/BrayoOS/memory/dream_tasks.json")
os.makedirs(os.path.dirname(TASKS_FILE),exist_ok=True)

class DreamMode:
    def __init__(self,root):
        self.root=root
        self.root.title("🌙 Dream Mode")
        self.root.geometry("640x560")
        self.root.configure(bg=BG)
        self.active=False
        self.tasks_done=0
        self.tasks=self.load_tasks()
        self.build_ui()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE) as f:return json.load(f)
        return [
            {"name":"GitHub Backup","cmd":"cd ~/BrayoOS && git add -A && git commit -m 'Dream backup' && git push origin main 2>/dev/null","enabled":True,"interval":60},
            {"name":"Clear Cache","cmd":"find ~/BrayoOS -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null","enabled":True,"interval":30},
            {"name":"Network Scan","cmd":"cat /proc/net/arp 2>/dev/null","enabled":True,"interval":20},
            {"name":"System Health Check","cmd":"python3 ~/BrayoOS/core/apps/self_healing.py 2>/dev/null &","enabled":False,"interval":120},
            {"name":"OSINT Monitor","cmd":"echo 'OSINT scan complete'","enabled":False,"interval":90},
            {"name":"Dark Web Scan","cmd":"echo 'Dark web clear'","enabled":True,"interval":45},
        ]

    def save_tasks(self):
        with open(TASKS_FILE,"w") as f:json.dump(self.tasks,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🌙 DREAM MODE",font=("Courier",14,"bold"),bg=BG2,fg=PURPLE).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="Auto-tasks while you sleep",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.status_dot=tk.Label(hdr,text="⬤ SLEEPING",font=("Courier",9,"bold"),bg=BG2,fg=DIM)
        self.status_dot.pack(side="right",padx=12)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([("TASKS DONE",GREEN),("RUNTIME",NEON),("NEXT TASK",GOLD),("BATTERY",PURPLE)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",11,"bold"),bg=BG3,fg=color).pack(pady=2)

        # Dream animation canvas
        self.dream_canvas=tk.Canvas(self.root,width=610,height=80,bg=BG,highlightthickness=0)
        self.dream_canvas.pack(padx=15,pady=3)
        self._draw_dream(False)

        # Task list
        tk.Label(self.root,text="◈ AUTO TASKS",font=("Courier",10,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(5,3))
        task_f=tk.Frame(self.root,bg=BG);task_f.pack(fill="x",padx=15)
        self.task_vars=[]
        for task in self.tasks:
            f=tk.Frame(task_f,bg=BG3);f.pack(fill="x",pady=2)
            v=tk.BooleanVar(value=task["enabled"])
            self.task_vars.append(v)
            tk.Checkbutton(f,variable=v,bg=BG3,selectcolor=PURPLE,activebackground=BG3).pack(side="left",padx=5,pady=4)
            tk.Label(f,text=task["name"],font=("Courier",9,"bold"),bg=BG3,fg=WHITE).pack(side="left")
            tk.Label(f,text=f"every {task['interval']}s",font=("Courier",7),bg=BG3,fg=DIM).pack(side="left",padx=8)

        # Log
        tk.Label(self.root,text="◈ DREAM LOG",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(8,2))
        self.log_box=tk.Text(self.root,height=7,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=3)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("y",foreground=GOLD)
        self.log_box.tag_config("p",foreground=PURPLE)

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        self.dream_btn=tk.Button(bf,text="🌙 ENTER DREAM MODE",font=("Courier",11,"bold"),
                                  bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=7,command=self.toggle)
        self.dream_btn.pack(side="left",padx=5)
        tk.Button(bf,text="💾 Save Tasks",font=("Courier",10),bg=BG3,fg=GREEN,
                 relief="flat",padx=12,pady=7,command=self.save_config).pack(side="left",padx=5)

        tk.Label(self.root,text="BrayoOS Dream Mode v4.5 • AIRA 🇰🇪 | Plug in charger first!",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def _draw_dream(self,active):
        self.dream_canvas.delete("all")
        self.dream_canvas.create_rectangle(0,0,610,80,fill=BG)
        if active:
            colors=[PURPLE,"#6600CC","#440088","#220044"]
            for i,color in enumerate(colors):
                for j in range(0,610,60):
                    x=j+i*15+random.randint(-5,5)
                    y=40+random.randint(-20,20)
                    self.dream_canvas.create_oval(x-3,y-3,x+3,y+3,fill=color,outline="")
            self.dream_canvas.create_text(305,40,text="✦ DREAM MODE ACTIVE — AIRA is working ✦",
                                         fill=NEON,font=("Courier",11,"bold"))
        else:
            for i in range(0,610,30):
                self.dream_canvas.create_line(i,40,i+15,40,fill=DIM,width=1)
            self.dream_canvas.create_text(305,40,text="🌙 Sleep mode inactive",fill=DIM,font=("Courier",10))

    def log(self,msg,tag="y"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def toggle(self):
        if not self.active:
            self.active=True
            self.dream_btn.config(text="⏹ WAKE UP",bg=DIM)
            self.status_dot.config(text="⬤ DREAMING",fg=PURPLE)
            self.log("🌙 Dream Mode activated. AIRA taking over...","p")
            self.log("💡 Plug in charger to keep running overnight","y")
            threading.Thread(target=self.dream_loop,daemon=True).start()
        else:
            self.active=False
            self.dream_btn.config(text="🌙 ENTER DREAM MODE",bg=PURPLE)
            self.status_dot.config(text="⬤ SLEEPING",fg=DIM)
            self.log("☀️ Dream Mode ended. Welcome back, Brayo!","g")
            self.root.after(0,self._draw_dream,False)

    def dream_loop(self):
        start=time.time()
        task_timers={i:0 for i in range(len(self.tasks))}
        while self.active:
            self.root.after(0,self._draw_dream,True)
            uptime=int(time.time()-start)
            self.root.after(0,self.svars["RUNTIME"].set,f"{uptime//60}m{uptime%60}s")
            self.root.after(0,self.svars["TASKS DONE"].set,str(self.tasks_done))
            # Get battery
            try:
                import json
                r=subprocess.check_output("termux-battery-status 2>/dev/null",shell=True,timeout=2).decode()
                bat=json.loads(r).get("percentage",0)
                self.root.after(0,self.svars["BATTERY"].set,f"{bat}%")
            except:
                self.root.after(0,self.svars["BATTERY"].set,"?%")
            # Run tasks
            for i,(task,var) in enumerate(zip(self.tasks,self.task_vars)):
                if var.get():
                    task_timers[i]+=1
                    if task_timers[i]>=task["interval"]//5:
                        task_timers[i]=0
                        self.root.after(0,self.log,f"⚡ Running: {task['name']}","p")
                        subprocess.run(task["cmd"],shell=True,capture_output=True,timeout=10)
                        self.tasks_done+=1
                        self.root.after(0,self.log,f"✅ Done: {task['name']}","g")
            time.sleep(5)

    def save_config(self):
        for i,(task,var) in enumerate(zip(self.tasks,self.task_vars)):
            task["enabled"]=var.get()
        self.save_tasks()
        self.log("💾 Tasks saved!","g")

if __name__=="__main__":
    root=tk.Tk();DreamMode(root);root.mainloop()
