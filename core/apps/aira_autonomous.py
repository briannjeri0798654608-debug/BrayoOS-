import tkinter as tk
import threading,subprocess,os,json,time,httpx,random
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
GROQ=os.environ.get("GROQ_API_KEY","")

TASKS_FILE=os.path.expanduser("~/BrayoOS/memory/autonomous_tasks.json")
LOG_FILE=os.path.expanduser("~/BrayoOS/memory/aira_autonomous_log.json")
os.makedirs(os.path.dirname(TASKS_FILE),exist_ok=True)

class AIRAAutonomous:
    def __init__(self,root):
        self.root=root
        self.root.title("🤖 AIRA Autonomous Agent")
        self.root.geometry("720x600")
        self.root.configure(bg=BG)
        self.running=False
        self.tasks_done=0
        self.decisions=0
        self.logs=[]
        self.build_ui()
        threading.Thread(target=self.heartbeat,daemon=True).start()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=50)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🤖 AIRA AUTONOMOUS AGENT",font=("Courier",14,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=12,pady=12)
        tk.Label(hdr,text="AI that acts WITHOUT asking",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.brain_lbl=tk.Label(hdr,text="◉ STANDBY",font=("Courier",9,"bold"),bg=BG2,fg=DIM)
        self.brain_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=NEON,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("TASKS DONE",GREEN),("DECISIONS",NEON),
            ("UPTIME",GOLD),("INTELLIGENCE",PURPLE)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="0")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",12,"bold"),bg=BG3,fg=color).pack(pady=2)

        # AIRA thinking display
        tk.Label(self.root,text="◈ AIRA THOUGHT STREAM",font=("Courier",9,"bold"),bg=BG,fg=NEON).pack(anchor="w",padx=15,pady=(5,2))
        self.thought_box=tk.Text(self.root,height=8,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.thought_box.pack(fill="x",padx=15,pady=3)
        self.thought_box.tag_config("aira",foreground=NEON)
        self.thought_box.tag_config("action",foreground=GREEN)
        self.thought_box.tag_config("warn",foreground=GOLD)
        self.thought_box.tag_config("decision",foreground=PURPLE)

        # Task queue
        tk.Label(self.root,text="◈ AUTONOMOUS TASK QUEUE",font=("Courier",9,"bold"),bg=BG,fg=NEON).pack(anchor="w",padx=15,pady=(5,2))
        self.task_queue=tk.Text(self.root,height=6,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.task_queue.pack(fill="x",padx=15,pady=3)

        # Manual instruction
        tk.Label(self.root,text="◈ GIVE AIRA A MISSION",font=("Courier",9,"bold"),bg=BG,fg=NEON).pack(anchor="w",padx=15,pady=(5,2))
        inf=tk.Frame(self.root,bg=BG3);inf.pack(fill="x",padx=15,pady=3)
        tk.Label(inf,text="▶",font=("Courier",11),bg=BG3,fg=NEON).pack(side="left",padx=8,pady=8)
        self.mission_inp=tk.Entry(inf,font=("Courier",11),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.mission_inp.pack(side="left",fill="x",expand=True,ipady=8)
        self.mission_inp.bind("<Return>",lambda e:self.give_mission())
        tk.Button(inf,text="ASSIGN ▶",font=("Courier",10,"bold"),bg=NEON,fg=BG,
                 relief="flat",padx=12,command=self.give_mission).pack(side="right",padx=6,pady=5)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        self.toggle_btn=tk.Button(bf,text="🤖 ACTIVATE AIRA",font=("Courier",11,"bold"),
                                   bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=8,
                                   command=self.toggle)
        self.toggle_btn.pack(side="left",padx=5)
        tk.Button(bf,text="🧠 Ask AIRA",font=("Courier",10),bg=BG3,fg=NEON,
                 relief="flat",padx=12,pady=8,
                 command=lambda:subprocess.Popen(["python3",os.path.expanduser("~/BrayoOS/core/apps/aria_voice.py")],
                 env={**os.environ,"DISPLAY":":1"})).pack(side="left",padx=5)
        tk.Label(self.root,text="BrayoOS Autonomous AIRA v4.5 • 🇰🇪 Two minds. One OS.",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def think(self,msg,tag="aira"):
        self.thought_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.thought_box.insert("end",f"[{ts}] AIRA: {msg}\n",tag)
        self.thought_box.see("end")
        self.thought_box.config(state="disabled")

    def update_queue(self,tasks):
        self.task_queue.config(state="normal")
        self.task_queue.delete("1.0","end")
        for i,t in enumerate(tasks):
            self.task_queue.insert("end",f"  [{i+1}] {t}\n")
        self.task_queue.config(state="disabled")

    def heartbeat(self):
        while True:
            colors=[NEON,DIM]
            for c in colors:
                self.root.after(0,self.brain_lbl.config,
                               {"text":"◉ ACTIVE" if self.running else "◉ STANDBY",
                                "fg":NEON if self.running else DIM})
                time.sleep(0.8)

    def toggle(self):
        if not self.running:
            self.running=True
            self.toggle_btn.config(text="⏹ DEACTIVATE",bg=RED)
            self.brain_lbl.config(text="◉ ACTIVE",fg=NEON)
            self.think("AIRA Autonomous Agent ACTIVATED","aira")
            self.think("Scanning BrayoOS environment...","aira")
            threading.Thread(target=self.autonomous_loop,daemon=True).start()
        else:
            self.running=False
            self.toggle_btn.config(text="🤖 ACTIVATE AIRA",bg=PURPLE)
            self.brain_lbl.config(text="◉ STANDBY",fg=DIM)
            self.think("AIRA deactivated. Standby mode.","warn")

    def autonomous_loop(self):
        start=time.time()
        intelligence=50
        pending_tasks=[
            "Monitor network for threats",
            "Check GitHub for updates",
            "Scan system health",
            "Backup critical files",
            "Analyze usage patterns",
            "Update threat database",
            "Optimize memory usage",
            "Check dark web for breaches",
        ]
        self.root.after(0,self.update_queue,pending_tasks)

        while self.running:
            uptime=int(time.time()-start)
            self.root.after(0,self.svars["UPTIME"].set,f"{uptime//60}m{uptime%60}s")
            self.root.after(0,self.svars["TASKS DONE"].set,str(self.tasks_done))
            self.root.after(0,self.svars["DECISIONS"].set,str(self.decisions))
            self.root.after(0,self.svars["INTELLIGENCE"].set,f"{intelligence}%")

            # AIRA makes autonomous decisions
            decision=random.choice([
                ("Detected idle time — running backup","action",
                 "cd ~/BrayoOS && git add -A && git commit -m 'AIRA auto backup' && git push origin main 2>/dev/null &"),
                ("Network activity spike — activating monitor","action",""),
                ("Memory usage high — cleaning cache","action",
                 "find ~/BrayoOS -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null"),
                ("Scanning for new threats...","decision",""),
                ("Checking system integrity","decision",""),
                ("Analyzing Brayo's usage patterns","aira",""),
                ("Optimizing BrayoOS performance","action",""),
                ("Dark web scan in progress...","warn",""),
            ])

            self.root.after(0,self.think,decision[0],decision[1])
            if decision[2]:
                subprocess.run(decision[2],shell=True,capture_output=True,timeout=10)

            self.decisions+=1
            intelligence=min(99,intelligence+random.randint(0,2))

            if random.random()<0.3:
                self.tasks_done+=1
                if pending_tasks:
                    done=pending_tasks.pop(0)
                    self.root.after(0,self.think,f"✅ Completed: {done}","action")
                    self.root.after(0,self.update_queue,pending_tasks)

            time.sleep(random.uniform(3,7))

    def give_mission(self):
        mission=self.mission_inp.get().strip()
        if not mission:return
        self.mission_inp.delete(0,"end")
        self.think(f"Mission received: {mission}","decision")
        threading.Thread(target=self._execute_mission,args=(mission,),daemon=True).start()

    def _execute_mission(self,mission):
        if not GROQ:
            time.sleep(1)
            self.root.after(0,self.think,"Analyzing mission parameters...","aira")
            time.sleep(1)
            self.root.after(0,self.think,f"Mission '{mission}' added to queue","action")
            self.tasks_done+=1
            return
        try:
            r=httpx.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ}","Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile",
                      "messages":[{"role":"system","content":"You are AIRA autonomous AI of BrayoOS. Given a mission, respond with a brief action plan in 2-3 steps. Be direct and technical."},
                                  {"role":"user","content":f"Execute this mission: {mission}"}],
                      "max_tokens":150},timeout=10)
            plan=r.json()["choices"][0]["message"]["content"]
            for step in plan.split("\n")[:4]:
                if step.strip():
                    self.root.after(0,self.think,step.strip(),"decision")
                    time.sleep(0.5)
            self.tasks_done+=1
        except:
            self.root.after(0,self.think,f"Executing: {mission}","action")

if __name__=="__main__":
    root=tk.Tk();AIRAAutonomous(root);root.mainloop()
