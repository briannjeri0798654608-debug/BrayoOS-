import tkinter as tk
import os,json
from datetime import datetime,timedelta

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

FILE=os.path.expanduser("~/BrayoOS/memory/habit_tracker.json")
os.makedirs(os.path.dirname(FILE),exist_ok=True)

class HabitTracker:
    def __init__(self,root):
        self.root=root
        self.root.title("📅 Habit Tracker")
        self.root.geometry("660x540")
        self.root.configure(bg=BG)
        self.data=self.load()
        self.build_ui()

    def load(self):
        if os.path.exists(FILE):
            with open(FILE) as f:return json.load(f)
        return {"habits":[
            {"name":"Study IT","emoji":"📚","streak":0,"done_today":False},
            {"name":"Code BrayoOS","emoji":"💻","streak":0,"done_today":False},
            {"name":"Exercise","emoji":"💪","streak":0,"done_today":False},
            {"name":"Read Book","emoji":"📖","streak":0,"done_today":False},
            {"name":"Drink Water","emoji":"💧","streak":0,"done_today":False},
        ],"last_date":str(datetime.now().date())}

    def save(self):
        with open(FILE,"w") as f:json.dump(self.data,f,indent=2)

    def check_new_day(self):
        today=str(datetime.now().date())
        if self.data.get("last_date")!=today:
            for h in self.data["habits"]:
                if not h.get("done_today",False):
                    h["streak"]=0
                h["done_today"]=False
            self.data["last_date"]=today
            self.save()

    def build_ui(self):
        self.check_new_day()
        tk.Label(self.root,text="📅 HABIT TRACKER",
                font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        today=datetime.now().strftime("%A, %d %B %Y")
        tk.Label(self.root,text=today,font=("Courier",9),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Stats
        total=len(self.data["habits"])
        done=sum(1 for h in self.data["habits"] if h.get("done_today"))
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=5)
        for col,(lbl,val,color) in enumerate([
            ("TODAY",f"{done}/{total}",GREEN),
            ("STREAK",f"{max((h['streak'] for h in self.data['habits']),default=0)}d",GOLD),
            ("TOTAL HABITS",str(total),NEON),
            ("COMPLETION",f"{int(done*100/total) if total else 0}%",PURPLE)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            tk.Label(f,text=val,font=("Courier",14,"bold"),bg=BG3,fg=color).pack(pady=2)

        # Progress bar
        prog_f=tk.Frame(self.root,bg=BG3);prog_f.pack(fill="x",padx=15,pady=5)
        self.prog=tk.Canvas(prog_f,width=620,height=10,
                           bg="#001100",highlightthickness=0)
        self.prog.pack(padx=5,pady=5)
        self.draw_progress(done,total)

        # Habits list
        tk.Label(self.root,text="◈ MY HABITS",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.habits_frame=tk.Frame(self.root,bg=BG)
        self.habits_frame.pack(fill="both",expand=True,padx=15,pady=5)
        self.render_habits()

        # Add habit
        add_f=tk.Frame(self.root,bg=BG3);add_f.pack(fill="x",padx=15,pady=5)
        tk.Label(add_f,text="New habit:",font=("Courier",9),
                bg=BG3,fg=DIM).pack(side="left",padx=8,pady=8)
        self.new_habit=tk.Entry(add_f,font=("Courier",10),bg=BG,fg=WHITE,
                               insertbackground=NEON,relief="flat")
        self.new_habit.pack(side="left",fill="x",expand=True,ipady=6)
        tk.Button(add_f,text="➕",font=("Courier",11),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=10,
                 command=self.add_habit).pack(side="right",padx=6,pady=4)

        tk.Label(self.root,text="BrayoOS Habit Tracker v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def draw_progress(self,done,total):
        self.prog.delete("all")
        if total>0:
            w=int(620*done/total)
            if w>0:self.prog.create_rectangle(0,0,w,10,fill=GREEN,outline="")

    def render_habits(self):
        for w in self.habits_frame.winfo_children():w.destroy()
        for i,h in enumerate(self.data["habits"]):
            f=tk.Frame(self.habits_frame,bg=BG3)
            f.pack(fill="x",pady=2)
            done=h.get("done_today",False)
            color=GREEN if done else DIM
            tk.Label(f,text=h.get("emoji","📌"),
                    font=("Arial",14),bg=BG3).pack(side="left",padx=8,pady=6)
            tk.Label(f,text=h["name"],font=("Courier",11,"bold"),
                    bg=BG3,fg=GREEN if done else WHITE).pack(side="left")
            streak=h.get("streak",0)
            tk.Label(f,text=f"🔥 {streak} days",font=("Courier",8),
                    bg=BG3,fg=GOLD).pack(side="left",padx=10)
            done_txt="✅ DONE" if done else "⭕ TODO"
            tk.Button(f,text=done_txt,font=("Courier",9,"bold"),
                     bg=PURPLE if not done else BG3,
                     fg=WHITE,relief="flat",padx=10,pady=4,
                     command=lambda x=i:self.toggle(x)).pack(side="right",padx=8,pady=4)
            tk.Button(f,text="🗑",font=("Courier",9),bg=BG3,fg=RED,
                     relief="flat",padx=6,
                     command=lambda x=i:self.delete(x)).pack(side="right",pady=4)

    def toggle(self,idx):
        h=self.data["habits"][idx]
        h["done_today"]=not h.get("done_today",False)
        if h["done_today"]:h["streak"]=h.get("streak",0)+1
        else:h["streak"]=max(0,h.get("streak",0)-1)
        self.save()
        for w in self.root.winfo_children():w.destroy()
        self.build_ui()

    def delete(self,idx):
        del self.data["habits"][idx]
        self.save();self.render_habits()

    def add_habit(self):
        name=self.new_habit.get().strip()
        if name:
            self.data["habits"].append(
                {"name":name,"emoji":"⭐","streak":0,"done_today":False})
            self.save()
            self.new_habit.delete(0,"end")
            self.render_habits()

if __name__=="__main__":
    root=tk.Tk();HabitTracker(root);root.mainloop()
