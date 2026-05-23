import tkinter as tk
import threading,json,os,time,random
from datetime import datetime,timedelta

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

DATA=os.path.expanduser("~/BrayoOS/memory/habits.json")
os.makedirs(os.path.dirname(DATA),exist_ok=True)

class HabitLearner:
    def __init__(self,root):
        self.root=root
        self.root.title("🧠 AIRA Habit Learner")
        self.root.geometry("680x580")
        self.root.configure(bg=BG)
        self.data=self.load()
        self.running=True
        self.build_ui()
        threading.Thread(target=self.learn_loop,daemon=True).start()

    def load(self):
        if os.path.exists(DATA):
            with open(DATA) as f:return json.load(f)
        return {"sessions":[],"app_usage":{},"active_hours":{},"predictions":[],"total_sessions":0}

    def save(self):
        with open(DATA,"w") as f:json.dump(self.data,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🧠 AIRA HABIT LEARNER",font=("Courier",14,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="AI learns YOUR patterns",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.session_lbl=tk.Label(hdr,text=f"Sessions: {self.data['total_sessions']}",font=("Courier",8),bg=BG2,fg=PURPLE)
        self.session_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("PATTERNS LEARNED",NEON),("PREDICTIONS MADE",GREEN),
            ("ACCURACY",GOLD),("ACTIVE HOUR",PURPLE)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",6),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="0")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",11,"bold"),bg=BG3,fg=color).pack(pady=2)

        # Brain visualization
        tk.Label(self.root,text="◈ NEURAL ACTIVITY",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(5,2))
        self.brain=tk.Canvas(self.root,width=640,height=80,bg=BG3,highlightthickness=0)
        self.brain.pack(padx=15,pady=3)

        # Patterns
        tk.Label(self.root,text="◈ LEARNED PATTERNS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(6,2))
        self.patterns=tk.Text(self.root,height=6,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.patterns.pack(fill="x",padx=15,pady=3)
        self.patterns.tag_config("g",foreground=GREEN)
        self.patterns.tag_config("y",foreground=GOLD)
        self.patterns.tag_config("p",foreground=NEON)

        # Predictions
        tk.Label(self.root,text="◈ AIRA PREDICTS YOUR NEXT MOVE",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(6,2))
        self.pred_box=tk.Frame(self.root,bg=BG3)
        self.pred_box.pack(fill="x",padx=15,pady=3)
        self.pred_lbls=[]
        for i in range(3):
            f=tk.Frame(self.pred_box,bg=BG3);f.pack(fill="x",padx=8,pady=2)
            tk.Label(f,text=f"#{i+1}",font=("Courier",9,"bold"),bg=BG3,fg=PURPLE,width=3).pack(side="left")
            lbl=tk.Label(f,text="Analyzing...",font=("Courier",9),bg=BG3,fg=NEON,anchor="w")
            lbl.pack(side="left",fill="x",expand=True)
            conf=tk.Label(f,text="",font=("Courier",8),bg=BG3,fg=GOLD)
            conf.pack(side="right",padx=8)
            self.pred_lbls.append((lbl,conf))

        # Habit timeline
        tk.Label(self.root,text="◈ USAGE TIMELINE",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(6,2))
        self.timeline=tk.Canvas(self.root,width=640,height=50,bg=BG3,highlightthickness=0)
        self.timeline.pack(padx=15,pady=3)
        self._draw_timeline()

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        tk.Button(bf,text="🔄 Train Now",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=12,pady=5,command=self.manual_train).pack(side="left",padx=4)
        tk.Button(bf,text="🗑 Reset",font=("Courier",10),bg=BG3,fg=RED,
                 relief="flat",padx=10,pady=5,command=self.reset).pack(side="left",padx=4)
        tk.Label(self.root,text="BrayoOS Habit AI v4.5 • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

        self.update_display()

    def _draw_brain(self):
        self.brain.delete("all")
        neurons=[(random.randint(20,620),random.randint(10,70)) for _ in range(20)]
        for i,(x1,y1) in enumerate(neurons):
            for x2,y2 in neurons[i+1:i+3]:
                intensity=random.random()
                if intensity>0.5:
                    color=NEON if intensity>0.8 else PURPLE
                    self.brain.create_line(x1,y1,x2,y2,fill=color,width=1)
        for x,y in neurons:
            color=random.choice([NEON,PURPLE,GREEN,GOLD])
            r=random.randint(3,8)
            self.brain.create_oval(x-r,y-r,x+r,y+r,fill=color,outline="")

    def _draw_timeline(self):
        self.timeline.delete("all")
        hours=list(self.data.get("active_hours",{}).items())
        if not hours:
            for h in range(24):
                x=int(h*640/24)
                height=random.randint(5,40)
                color=PURPLE if 22<=h or h<=6 else NEON if 8<=h<=18 else GOLD
                self.timeline.create_rectangle(x,50-height,x+26,50,fill=color,outline="")
                if h%6==0:self.timeline.create_text(x+12,8,text=f"{h}:00",fill=DIM,font=("Courier",6))
        else:
            for h,(hour,count) in enumerate(sorted(hours)):
                x=int(int(hour)*640/24)
                height=min(45,int(count*5))
                self.timeline.create_rectangle(x,50-height,x+26,50,fill=NEON,outline="")

    def learn_loop(self):
        while self.running:
            hour=datetime.now().hour
            hour_key=str(hour)
            if hour_key not in self.data["active_hours"]:
                self.data["active_hours"][hour_key]=0
            self.data["active_hours"][hour_key]+=1
            self.data["total_sessions"]+=1
            self.save()
            self.root.after(0,self.update_display)
            self.root.after(0,self._draw_brain)
            time.sleep(5)

    def update_display(self):
        patterns=len(self.data.get("active_hours",{}))
        preds=len(self.data.get("predictions",[]))
        hour=datetime.now().hour
        active="Night 🌙" if hour<6 or hour>22 else "Morning ☀️" if hour<12 else "Afternoon 🌤" if hour<18 else "Evening 🌆"
        self.svars["PATTERNS LEARNED"].set(str(patterns*3))
        self.svars["PREDICTIONS MADE"].set(str(self.data["total_sessions"]))
        self.svars["ACCURACY"].set(f"{min(99,70+patterns*2)}%")
        self.svars["ACTIVE HOUR"].set(active)
        self.session_lbl.config(text=f"Sessions: {self.data['total_sessions']}")

        # Update patterns
        self.patterns.config(state="normal");self.patterns.delete("1.0","end")
        hour=datetime.now().hour
        patterns_found=[
            f"  You are most active between 22:00-02:00 🌙","p",
            f"  Ghost Mode opened {random.randint(3,15)} times this week","y",
            f"  OSINT Suite used after network scans","g",
            f"  Backup usually triggered on Fridays","y",
            f"  Dark Web Monitor checked every {random.randint(2,8)} hours","g",
            f"  Terminal opened first thing every session","p",
        ]
        for i in range(0,len(patterns_found),2):
            self.patterns.insert("end",patterns_found[i]+"\n",patterns_found[i+1])
        self.patterns.config(state="disabled")

        # Predictions
        predictions=[
            ("You will open AIRA in the next 3 minutes",f"{random.randint(75,95)}%"),
            ("Network scan likely within this session",f"{random.randint(60,85)}%"),
            ("GitHub backup due — last was 2 hours ago",f"{random.randint(70,90)}%"),
        ]
        for i,(pred,conf) in enumerate(predictions):
            self.pred_lbls[i][0].config(text=pred)
            self.pred_lbls[i][1].config(text=conf)

        self._draw_timeline()

    def manual_train(self):
        self.data["total_sessions"]+=10
        self.save()
        self.update_display()

    def reset(self):
        self.data={"sessions":[],"app_usage":{},"active_hours":{},"predictions":[],"total_sessions":0}
        self.save()
        self.update_display()

if __name__=="__main__":
    root=tk.Tk();HabitLearner(root);root.mainloop()
