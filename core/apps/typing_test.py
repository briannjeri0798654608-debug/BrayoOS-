import tkinter as tk
import time,random,os,json
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

TEXTS=[
    "BrayoOS is a complete operating system built on a phone in Kenya by Brayo and AIRA working together.",
    "Two minds one OS built different this is the motto of BrayoOS the most powerful mobile operating system.",
    "The quick brown fox jumps over the lazy dog and the hacker types faster than the speed of light.",
    "Python is the language of BrayoOS and tkinter builds the graphical interface running on TigerVNC.",
    "AIRA is the artificial intelligence brain of BrayoOS powered by LLaMA three three seventy billion parameters.",
]

FILE=os.path.expanduser("~/BrayoOS/memory/typing_scores.json")
os.makedirs(os.path.dirname(FILE),exist_ok=True)

class TypingTest:
    def __init__(self,root):
        self.root=root
        self.root.title("⌨️ Typing Speed Test")
        self.root.geometry("680x520")
        self.root.configure(bg=BG)
        self.start_time=None
        self.running=False
        self.scores=self.load_scores()
        self.build_ui()
        self.new_test()

    def load_scores(self):
        if os.path.exists(FILE):
            with open(FILE) as f:return json.load(f)
        return []

    def save_score(self,wpm,accuracy):
        self.scores.append({"wpm":wpm,"accuracy":accuracy,
                           "date":datetime.now().strftime("%Y-%m-%d %H:%M")})
        self.scores=self.scores[-20:]
        with open(FILE,"w") as f:json.dump(self.scores,f,indent=2)

    def build_ui(self):
        tk.Label(self.root,text="⌨️ TYPING SPEED TEST",
                font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=5)

        # Stats bar
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=5)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("WPM",GREEN),("ACCURACY",NEON),
            ("TIME",GOLD),("BEST WPM",PURPLE)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",14,"bold"),
                    bg=BG3,fg=color).pack(pady=2)
        best=max((s["wpm"] for s in self.scores),default=0)
        self.svars["BEST WPM"].set(str(best))

        # Target text
        tk.Label(self.root,text="◈ TYPE THIS TEXT",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.target=tk.Text(self.root,height=4,bg=BG3,fg=WHITE,
                           font=("Courier",11),relief="flat",
                           state="disabled",wrap="word")
        self.target.pack(fill="x",padx=15,pady=5)
        self.target.tag_config("correct",foreground=GREEN,background="#003300")
        self.target.tag_config("wrong",foreground=RED,background="#330000")
        self.target.tag_config("current",foreground=NEON,underline=True)

        # Input
        tk.Label(self.root,text="◈ START TYPING",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.inp=tk.Text(self.root,height=4,bg=BG3,fg=WHITE,
                        font=("Courier",11),relief="flat",
                        insertbackground=NEON,wrap="word")
        self.inp.pack(fill="x",padx=15,pady=5)
        self.inp.bind("<KeyRelease>",self.on_type)

        # History
        tk.Label(self.root,text="◈ SCORE HISTORY",
                font=("Courier",8,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.history_box=tk.Text(self.root,height=4,bg=BG3,fg=WHITE,
                                font=("Courier",8),relief="flat",
                                state="disabled")
        self.history_box.pack(fill="x",padx=15,pady=3)
        self.render_history()

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=5)
        tk.Button(bf,text="🔄 New Test",font=("Courier",10,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=12,pady=6,
                 command=self.new_test).pack(side="left",padx=5)
        tk.Label(self.root,text="BrayoOS Typing Test v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def new_test(self):
        self.text=random.choice(TEXTS)
        self.start_time=None
        self.running=False
        self.target.config(state="normal")
        self.target.delete("1.0","end")
        self.target.insert("end",self.text)
        self.target.config(state="disabled")
        self.inp.delete("1.0","end")
        self.inp.focus_set()
        for k in ["WPM","ACCURACY","TIME"]:
            self.svars[k].set("--")

    def on_type(self,e=None):
        typed=self.inp.get("1.0","end-1c")
        if not typed:return
        if not self.running:
            self.running=True
            self.start_time=time.time()
            self._update_time()
        # Calculate stats
        correct=sum(1 for a,b in zip(typed,self.text) if a==b)
        total=len(typed)
        accuracy=int(correct*100/total) if total>0 else 100
        elapsed=time.time()-self.start_time
        words=len(typed.split())
        wpm=int(words*60/elapsed) if elapsed>0 else 0
        self.svars["WPM"].set(str(wpm))
        self.svars["ACCURACY"].set(f"{accuracy}%")
        # Color the target text
        self.target.config(state="normal")
        self.target.tag_remove("correct","1.0","end")
        self.target.tag_remove("wrong","1.0","end")
        self.target.tag_remove("current","1.0","end")
        for i,(tc,tt) in enumerate(zip(typed,self.text)):
            pos=f"1.{i}"
            npos=f"1.{i+1}"
            tag="correct" if tc==tt else "wrong"
            self.target.tag_add(tag,pos,npos)
        if len(typed)<len(self.text):
            pos=f"1.{len(typed)}"
            self.target.tag_add("current",pos,f"1.{len(typed)+1}")
        self.target.config(state="disabled")
        # Check completion
        if typed==self.text:
            self.save_score(wpm,accuracy)
            self.render_history()
            best=max((s["wpm"] for s in self.scores),default=0)
            self.svars["BEST WPM"].set(str(best))

    def _update_time(self):
        if self.running and self.start_time:
            elapsed=int(time.time()-self.start_time)
            self.svars["TIME"].set(f"{elapsed}s")
            self.root.after(1000,self._update_time)

    def render_history(self):
        self.history_box.config(state="normal")
        self.history_box.delete("1.0","end")
        for s in reversed(self.scores[-5:]):
            self.history_box.insert("end",
                f"  {s['date']} — {s['wpm']} WPM — {s['accuracy']}% accuracy\n")
        self.history_box.config(state="disabled")

if __name__=="__main__":
    root=tk.Tk();TypingTest(root);root.mainloop()
