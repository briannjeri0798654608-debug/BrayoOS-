import tkinter as tk
from datetime import datetime
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";GOLD="#FFD700"
class Clock:
    def __init__(self,r):
        r.title("Clock");r.geometry("400x300");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS CLOCK",font=("Courier",12,"bold"),bg=BG,fg=NEON).pack(pady=10)
        self.t=tk.Label(r,text="",font=("Courier",42,"bold"),bg=BG,fg=NEON)
        self.t.pack(pady=10)
        self.d=tk.Label(r,text="",font=("Courier",14),bg=BG,fg=GOLD)
        self.d.pack()
        self.w=tk.Label(r,text="",font=("Courier",11),bg=BG,fg="#444466")
        self.w.pack(pady=5)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x",padx=20,pady=10)
        tk.Label(r,text="BrayoOS • AIRA 🇰🇪",font=("Courier",8),bg=BG,fg="#333355").pack()
        self.tick()
    def tick(self):
        n=datetime.now()
        self.t.config(text=n.strftime("%H:%M:%S"))
        self.d.config(text=n.strftime("%B %d, %Y"))
        self.w.config(text=n.strftime("%A"))
        self.t.after(1000,self.tick)
if __name__=="__main__":
    r=tk.Tk();Clock(r);r.mainloop()
