import tkinter as tk
import json,os
from datetime import datetime
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GREEN="#44FF88"
F=os.path.expanduser("~/BrayoOS/memory/tasks.json")
os.makedirs(os.path.dirname(F),exist_ok=True)
class Tasks:
    def __init__(self,r):
        r.title("Tasks");r.geometry("500x500");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS TASKS",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        af=tk.Frame(r,bg=BG3);af.pack(fill="x",padx=15,pady=8)
        self.inp=tk.Entry(af,font=("Courier",11),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.inp.pack(side="left",fill="x",expand=True,ipady=7,padx=8)
        self.inp.bind("<Return>",lambda e:self.add())
        tk.Button(af,text="+ ADD",font=("Courier",9,"bold"),bg=PURPLE,fg=WHITE,
            relief="flat",padx=10,command=self.add).pack(side="right",padx=5,pady=4)
        self.tf=tk.Frame(r,bg=BG);self.tf.pack(fill="both",expand=True,padx=15)
        tk.Button(r,text="✅ Clear Done",font=("Courier",9),bg=BG3,fg=GREEN,
            relief="flat",padx=10,pady=4,command=self.clear_done).pack(pady=6)
        self.tasks=json.load(open(F)) if os.path.exists(F) else []
        self.render()
    def save(self):json.dump(self.tasks,open(F,"w"),indent=2)
    def add(self):
        t=self.inp.get().strip()
        if t:self.tasks.append({"text":t,"done":False});self.inp.delete(0,"end");self.save();self.render()
    def toggle(self,i):self.tasks[i]["done"]=not self.tasks[i]["done"];self.save();self.render()
    def clear_done(self):self.tasks=[t for t in self.tasks if not t["done"]];self.save();self.render()
    def render(self):
        for w in self.tf.winfo_children():w.destroy()
        for i,t in enumerate(self.tasks):
            f=tk.Frame(self.tf,bg=BG3);f.pack(fill="x",pady=2)
            c=GREEN if t["done"] else WHITE
            tk.Label(f,text=("✅ " if t["done"] else "○ ")+t["text"],font=("Courier",9),
                bg=BG3,fg=c,anchor="w").pack(side="left",padx=8,pady=6,fill="x",expand=True)
            tk.Button(f,text="✓",font=("Courier",9),bg=PURPLE,fg=WHITE,relief="flat",
                command=lambda x=i:self.toggle(x)).pack(side="right",padx=5,pady=4)
if __name__=="__main__":
    r=tk.Tk();Tasks(r);r.mainloop()
