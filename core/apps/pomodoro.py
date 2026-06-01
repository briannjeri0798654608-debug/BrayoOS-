import tkinter as tk
import threading,time,subprocess,os

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class Pomodoro:
    def __init__(self,root):
        self.root=root
        self.root.title("🍅 Pomodoro Timer")
        self.root.geometry("500x480")
        self.root.configure(bg=BG)
        self.work_mins=25
        self.break_mins=5
        self.long_break=15
        self.sessions=0
        self.running=False
        self.paused=False
        self.mode="WORK"
        self.secs_left=self.work_mins*60
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🍅 POMODORO TIMER",
                font=("Courier",16,"bold"),bg=BG,fg=RED).pack(pady=8)
        tk.Label(self.root,text="Focus • Work • Achieve",
                font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=RED,height=2).pack(fill="x",pady=6)

        # Mode indicator
        self.mode_lbl=tk.Label(self.root,text="◈ WORK SESSION",
                              font=("Courier",12,"bold"),bg=BG,fg=RED)
        self.mode_lbl.pack(pady=5)

        # Big timer
        self.timer_canvas=tk.Canvas(self.root,width=250,height=250,
                                   bg=BG,highlightthickness=0)
        self.timer_canvas.pack(pady=5)
        self.draw_timer(100)

        self.time_lbl=tk.Label(self.root,text="25:00",
                              font=("Courier",36,"bold"),bg=BG,fg=RED)
        self.time_lbl.place(x=250,y=250,anchor="center")

        # Sessions
        self.sess_lbl=tk.Label(self.root,
                              text="🍅 Session 1 | Completed: 0",
                              font=("Courier",9),bg=BG,fg=GOLD)
        self.sess_lbl.pack(pady=5)

        # Settings
        sf=tk.Frame(self.root,bg=BG3);sf.pack(fill="x",padx=30,pady=5)
        for label,var_name,default in [
            ("Work (min)","work_mins",25),
            ("Break (min)","break_mins",5),
            ("Long Break","long_break",15)]:
            f=tk.Frame(sf,bg=BG3);f.pack(side="left",expand=True)
            tk.Label(f,text=label,font=("Courier",7),bg=BG3,fg=DIM).pack()
            v=tk.StringVar(value=str(default))
            e=tk.Entry(f,textvariable=v,font=("Courier",10),
                      bg=BG,fg=WHITE,insertbackground=NEON,
                      relief="flat",width=4,justify="center")
            e.pack(ipady=4)
            setattr(self,f"{var_name}_var",v)

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=10)
        self.start_btn=tk.Button(bf,text="▶ START",
                                font=("Courier",12,"bold"),
                                bg=RED,fg=WHITE,relief="flat",
                                padx=15,pady=8,command=self.toggle)
        self.start_btn.pack(side="left",padx=5)
        tk.Button(bf,text="↺ RESET",font=("Courier",10),
                 bg=BG3,fg=GOLD,relief="flat",padx=12,pady=8,
                 command=self.reset).pack(side="left",padx=5)
        tk.Button(bf,text="⏭ SKIP",font=("Courier",10),
                 bg=BG3,fg=DIM,relief="flat",padx=12,pady=8,
                 command=self.skip).pack(side="left",padx=5)

        tk.Label(self.root,text="BrayoOS Pomodoro v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def draw_timer(self,pct):
        self.timer_canvas.delete("all")
        cx,cy,r=125,125,100
        self.timer_canvas.create_oval(cx-r,cy-r,cx+r,cy+r,
                                     outline=BG3,width=8)
        if pct>0:
            import math
            angle=360*pct/100
            color=RED if self.mode=="WORK" else GREEN
            self.timer_canvas.create_arc(
                cx-r,cy-r,cx+r,cy+r,
                start=90,extent=-angle,
                outline=color,width=8,style="arc")

    def toggle(self):
        if not self.running:
            try:
                self.work_mins=int(self.work_mins_var.get())
                self.break_mins=int(self.break_mins_var.get())
                self.long_break=int(self.long_break_var.get())
            except:pass
            if not self.paused:
                self.secs_left=self.work_mins*60
            self.running=True
            self.paused=False
            self.start_btn.config(text="⏸ PAUSE",bg=GOLD)
            threading.Thread(target=self.countdown,daemon=True).start()
        else:
            self.running=False
            self.paused=True
            self.start_btn.config(text="▶ RESUME",bg=RED)

    def countdown(self):
        total=self.secs_left
        while self.running and self.secs_left>0:
            mins,secs=divmod(self.secs_left,60)
            self.root.after(0,self.time_lbl.config,
                           {"text":f"{mins:02}:{secs:02}"})
            pct=int(self.secs_left*100/total) if total>0 else 0
            self.root.after(0,self.draw_timer,pct)
            self.secs_left-=1
            time.sleep(1)
        if self.secs_left<=0 and self.running:
            self.root.after(0,self.session_done)

    def session_done(self):
        self.running=False
        subprocess.Popen("termux-vibrate -d 1000 2>/dev/null",shell=True)
        if self.mode=="WORK":
            self.sessions+=1
            self.mode="BREAK" if self.sessions%4!=0 else "LONG BREAK"
            secs=(self.long_break if self.sessions%4==0 else self.break_mins)*60
            subprocess.Popen('termux-tts-speak "Work session done! Take a break." 2>/dev/null',shell=True)
            self.mode_lbl.config(text=f"◈ BREAK TIME!",fg=GREEN)
            self.start_btn.config(bg=GREEN)
        else:
            self.mode="WORK"
            secs=self.work_mins*60
            subprocess.Popen('termux-tts-speak "Break done! Back to work." 2>/dev/null',shell=True)
            self.mode_lbl.config(text="◈ WORK SESSION",fg=RED)
            self.start_btn.config(bg=RED)
        self.secs_left=secs
        self.start_btn.config(text="▶ START")
        self.sess_lbl.config(
            text=f"🍅 Session {self.sessions+1} | Completed: {self.sessions}")
        mins,s=divmod(secs,60)
        self.time_lbl.config(text=f"{mins:02}:{s:02}")
        self.draw_timer(100)

    def reset(self):
        self.running=False
        self.paused=False
        self.mode="WORK"
        self.secs_left=self.work_mins*60
        mins,s=divmod(self.secs_left,60)
        self.time_lbl.config(text=f"{mins:02}:{s:02}",fg=RED)
        self.mode_lbl.config(text="◈ WORK SESSION",fg=RED)
        self.start_btn.config(text="▶ START",bg=RED)
        self.draw_timer(100)

    def skip(self):
        self.running=False
        self.session_done()

if __name__=="__main__":
    root=tk.Tk();Pomodoro(root);root.mainloop()
