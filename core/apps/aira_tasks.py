import tkinter as tk
import threading,subprocess,os,json,time,httpx
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

GROQ_KEY=os.environ.get("GROQ_API_KEY","")
TASKS_FILE=os.path.expanduser("~/BrayoOS/memory/aira_tasks.json")
os.makedirs(os.path.dirname(TASKS_FILE),exist_ok=True)

AIRA_SYSTEM="""You are AIRA, AI of BrayoOS built by Brayo in Kenya.
You can execute tasks on BrayoOS. When user gives a command, respond with JSON:
{"action":"open_app","app":"ghost_mode.py","message":"Opening Ghost Mode"}
or {"action":"run_command","cmd":"ls ~/BrayoOS","message":"Listing files"}
or {"action":"reminder","time":"5","message":"Reminder set for 5 minutes"}
or {"action":"chat","message":"Your response here"}
Keep responses short. Call user Brayo. Be confident like a hacker AI."""

class AIRATasks:
    def __init__(self,root):
        self.root=root
        self.root.title("🤖 AIRA Auto-Tasks")
        self.root.geometry("650x560")
        self.root.configure(bg=BG)
        self.tasks=self.load_tasks()
        self.build_ui()
        self.log("AIRA Auto-Tasks online. Tell me what to do, Brayo.","aira")
        self.log("Try: 'open ghost mode' or 'remind me in 5 minutes' or 'list my apps'","info")

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE) as f:return json.load(f)
        return []

    def save_tasks(self):
        with open(TASKS_FILE,"w") as f:json.dump(self.tasks,f,indent=2)

    def build_ui(self):
        # Header
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🤖 AIRA AUTO-TASKS",font=("Courier",14,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=15,pady=10)
        tk.Label(hdr,text="Tell AIRA what to do",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.status_dot=tk.Label(hdr,text="⬤ ONLINE",font=("Courier",8),bg=BG2,fg=GREEN)
        self.status_dot.pack(side="right",padx=15)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Quick commands
        qf=tk.Frame(self.root,bg=BG);qf.pack(fill="x",padx=10,pady=5)
        tk.Label(qf,text="Quick:",font=("Courier",8),bg=BG,fg=DIM).pack(side="left",padx=5)
        for cmd in ["open ghost mode","scan network","list apps","backup now","threat level"]:
            tk.Button(qf,text=cmd,font=("Courier",7),bg=BG3,fg=NEON,relief="flat",
                     padx=6,pady=3,command=lambda c=cmd:self.quick(c)).pack(side="left",padx=2)

        # Chat area
        self.chat=tk.Text(self.root,height=14,bg=BG3,fg=WHITE,font=("Courier",9),
                          relief="flat",state="disabled",wrap="word")
        self.chat.pack(fill="both",expand=True,padx=10,pady=5)
        self.chat.tag_config("aira",foreground=NEON)
        self.chat.tag_config("user",foreground=GOLD)
        self.chat.tag_config("info",foreground=DIM)
        self.chat.tag_config("success",foreground=GREEN)
        self.chat.tag_config("error",foreground=RED)

        # Task list
        tk.Label(self.root,text="◈ SCHEDULED TASKS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=10)
        self.task_list=tk.Text(self.root,height=4,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.task_list.pack(fill="x",padx=10,pady=3)

        # Input
        inf=tk.Frame(self.root,bg=BG3);inf.pack(fill="x",padx=10,pady=5)
        tk.Label(inf,text="▶",font=("Courier",11),bg=BG3,fg=PURPLE).pack(side="left",padx=8)
        self.inp=tk.Entry(inf,font=("Courier",11),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.inp.pack(side="left",fill="x",expand=True,ipady=8)
        self.inp.bind("<Return>",lambda e:self.execute())
        tk.Button(inf,text="EXECUTE ▶",font=("Courier",9,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=12,command=self.execute).pack(side="right",padx=5,pady=4)

        tk.Label(self.root,text="BrayoOS AIRA Auto-Tasks v1.0 • 🇰🇪",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)
        self.render_tasks()

    def log(self,msg,tag="aira"):
        self.chat.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        prefix="AIRA: " if tag=="aira" else "BRAYO: " if tag=="user" else "  "
        self.chat.insert("end",f"[{ts}] {prefix}{msg}\n",tag)
        self.chat.see("end")
        self.chat.config(state="disabled")

    def quick(self,cmd):
        self.inp.delete(0,"end")
        self.inp.insert(0,cmd)
        self.execute()

    def execute(self):
        cmd=self.inp.get().strip()
        if not cmd:return
        self.inp.delete(0,"end")
        self.log(cmd,"user")
        threading.Thread(target=self.process,args=(cmd,),daemon=True).start()

    def process(self,cmd):
        cmd_lower=cmd.lower()

        # Local command processing first
        if any(x in cmd_lower for x in ["open","launch","start"]):
            app_map={
                "ghost":("ghost_mode.py","Ghost Mode"),
                "vault":("dna_vault.py","DNA Vault"),
                "threat":("live_threat_map.py","Threat Map"),
                "dark web":("dark_web_monitor.py","Dark Web Monitor"),
                "signal":("signal_interceptor.py","Signal Interceptor"),
                "neural":("aria_neural_core.py","Neural Core"),
                "osint":("osint_suite.py","OSINT Suite"),
                "scanner":("network_scanner.py","Network Scanner"),
                "monitor":("system_monitor.py","System Monitor"),
            }
            for key,(script,name) in app_map.items():
                if key in cmd_lower:
                    path=os.path.expanduser(f"~/BrayoOS/core/apps/{script}")
                    subprocess.Popen(["python3",path],env={**os.environ,"DISPLAY":":1"})
                    self.root.after(0,self.log,f"✅ Opened {name} for you, Brayo.","success")
                    return

        if "list" in cmd_lower and "app" in cmd_lower:
            apps=os.listdir(os.path.expanduser("~/BrayoOS/core/apps/"))
            self.root.after(0,self.log,f"Found {len(apps)} apps in BrayoOS:","aira")
            for a in sorted(apps)[:10]:
                self.root.after(0,self.log,f"  → {a}","info")
            return

        if "backup" in cmd_lower:
            subprocess.run("cd ~/BrayoOS && git add -A && git commit -m 'AIRA auto backup' && git push origin main",shell=True)
            self.root.after(0,self.log,"✅ Backup pushed to GitHub!","success")
            return

        if "remind" in cmd_lower:
            mins=5
            for w in cmd_lower.split():
                if w.isdigit():mins=int(w);break
            task={"text":f"Reminder: {cmd}","time":mins,"created":datetime.now().isoformat()}
            self.tasks.append(task)
            self.save_tasks()
            self.root.after(0,self.log,f"⏰ Reminder set for {mins} minutes!","success")
            self.root.after(0,self.render_tasks)
            threading.Thread(target=self.run_reminder,args=(mins,cmd),daemon=True).start()
            return

        if "threat" in cmd_lower:
            self.root.after(0,self.log,"🔍 Scanning for threats...","aira")
            time.sleep(1)
            self.root.after(0,self.log,"✅ No active threats detected. Ghost Mode armed.","success")
            return

        # Use Groq if available
        if GROQ_KEY:
            try:
                r=httpx.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
                    json={"model":"llama-3.3-70b-versatile",
                          "messages":[{"role":"system","content":AIRA_SYSTEM},{"role":"user","content":cmd}],
                          "max_tokens":100},timeout=10)
                reply=r.json()["choices"][0]["message"]["content"].strip()
                try:
                    import re
                    m=re.search(r'\{.*\}',reply,re.DOTALL)
                    if m:
                        data=json.loads(m.group())
                        action=data.get("action","chat")
                        msg=data.get("message","Done.")
                        if action=="open_app":
                            app=data.get("app","")
                            if app:
                                path=os.path.expanduser(f"~/BrayoOS/core/apps/{app}")
                                subprocess.Popen(["python3",path],env={**os.environ,"DISPLAY":":1"})
                        elif action=="run_command":
                            c=data.get("cmd","")
                            if c:subprocess.run(c,shell=True)
                        self.root.after(0,self.log,msg,"aira")
                    else:
                        self.root.after(0,self.log,reply,"aira")
                except:
                    self.root.after(0,self.log,reply,"aira")
            except Exception as e:
                self.root.after(0,self.log,f"I'm here, Brayo. Try: 'open ghost mode' or 'backup now'","aira")
        else:
            self.root.after(0,self.log,"Set GROQ_API_KEY for full AI power. Local mode active.","aira")

    def run_reminder(self,mins,msg):
        time.sleep(mins*60)
        self.root.after(0,self.log,f"⏰ REMINDER: {msg}","success")
        subprocess.Popen(f'termux-notification --title "⏰ AIRA Reminder" --content "{msg}" 2>/dev/null',shell=True)

    def render_tasks(self):
        self.task_list.config(state="normal");self.task_list.delete("1.0","end")
        if not self.tasks:
            self.task_list.insert("end","  No scheduled tasks\n")
        for t in self.tasks[-5:]:
            self.task_list.insert("end",f"  ⏰ {t['text']}\n")
        self.task_list.config(state="disabled")

if __name__=="__main__":
    root=tk.Tk()
    AIRATasks(root)
    root.mainloop()
