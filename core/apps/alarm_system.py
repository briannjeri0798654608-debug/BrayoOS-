import tkinter as tk
import threading,time,os,json,subprocess
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

ALARMS_FILE=os.path.expanduser("~/BrayoOS/memory/alarms.json")
os.makedirs(os.path.dirname(ALARMS_FILE),exist_ok=True)

class AlarmSystem:
    def __init__(self,root):
        self.root=root
        self.root.title("⏰ Alarm System")
        self.root.geometry("600x520")
        self.root.configure(bg=BG)
        self.alarms=self.load()
        self.build_ui()
        threading.Thread(target=self.check_loop,daemon=True).start()

    def load(self):
        if os.path.exists(ALARMS_FILE):
            with open(ALARMS_FILE) as f:return json.load(f)
        return []

    def save(self):
        with open(ALARMS_FILE,"w") as f:json.dump(self.alarms,f,indent=2)

    def build_ui(self):
        tk.Label(self.root,text="⏰ ALARM & REMINDER SYSTEM",
                font=("Courier",14,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=5)

        # Clock display
        self.clock=tk.Label(self.root,text="",
                           font=("Courier",28,"bold"),bg=BG,fg=NEON)
        self.clock.pack(pady=5)
        self.date_lbl=tk.Label(self.root,text="",
                              font=("Courier",10),bg=BG,fg=DIM)
        self.date_lbl.pack()
        self._tick()

        # Add alarm form
        af=tk.Frame(self.root,bg=BG3);af.pack(fill="x",padx=15,pady=8)
        tk.Label(af,text="◈ NEW ALARM",font=("Courier",9,"bold"),
                bg=BG3,fg=PURPLE).pack(anchor="w",padx=8,pady=(8,4))

        row1=tk.Frame(af,bg=BG3);row1.pack(fill="x",padx=8,pady=3)
        tk.Label(row1,text="Time (HH:MM):",font=("Courier",9),
                bg=BG3,fg=DIM,width=14,anchor="w").pack(side="left")
        self.time_e=tk.Entry(row1,font=("Courier",11),bg=BG,fg=NEON,
                            insertbackground=NEON,relief="flat",width=8)
        self.time_e.pack(side="left",ipady=5)
        self.time_e.insert(0,datetime.now().strftime("%H:%M"))

        row2=tk.Frame(af,bg=BG3);row2.pack(fill="x",padx=8,pady=3)
        tk.Label(row2,text="Label:",font=("Courier",9),
                bg=BG3,fg=DIM,width=14,anchor="w").pack(side="left")
        self.label_e=tk.Entry(row2,font=("Courier",11),bg=BG,fg=WHITE,
                             insertbackground=NEON,relief="flat")
        self.label_e.pack(side="left",fill="x",expand=True,ipady=5)
        self.label_e.insert(0,"BrayoOS Reminder")

        row3=tk.Frame(af,bg=BG3);row3.pack(fill="x",padx=8,pady=3)
        tk.Label(row3,text="Type:",font=("Courier",9),
                bg=BG3,fg=DIM,width=14,anchor="w").pack(side="left")
        self.type_var=tk.StringVar(value="Once")
        for t in ["Once","Daily","Weekdays"]:
            tk.Radiobutton(row3,text=t,variable=self.type_var,value=t,
                          bg=BG3,fg=NEON,selectcolor=PURPLE,
                          activebackground=BG3,
                          font=("Courier",8)).pack(side="left",padx=8)

        tk.Button(af,text="➕ ADD ALARM",font=("Courier",10,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=12,pady=5,
                 command=self.add_alarm).pack(pady=8)

        # Alarm list
        tk.Label(self.root,text="◈ ACTIVE ALARMS",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.alarm_list=tk.Text(self.root,height=8,bg=BG3,fg=WHITE,
                               font=("Courier",9),relief="flat",state="disabled")
        self.alarm_list.pack(fill="both",expand=True,padx=15,pady=5)
        self.alarm_list.tag_config("a",foreground=GREEN)
        self.alarm_list.tag_config("r",foreground=RED)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=5)
        tk.Button(bf,text="🗑 Delete Selected",font=("Courier",9),
                 bg=BG3,fg=RED,relief="flat",padx=10,pady=5,
                 command=self.delete_alarm).pack(side="left",padx=5)
        tk.Button(bf,text="🔕 Dismiss All",font=("Courier",9),
                 bg=BG3,fg=GOLD,relief="flat",padx=10,pady=5,
                 command=self.dismiss_all).pack(side="left",padx=5)
        tk.Label(self.root,text="BrayoOS Alarm v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)
        self.render_alarms()

    def _tick(self):
        now=datetime.now()
        self.clock.config(text=now.strftime("%H:%M:%S"))
        self.date_lbl.config(text=now.strftime("%A, %d %B %Y"))
        self.root.after(1000,self._tick)

    def add_alarm(self):
        t=self.time_e.get().strip()
        label=self.label_e.get().strip() or "Alarm"
        atype=self.type_var.get()
        if len(t)==5 and ":" in t:
            alarm={"time":t,"label":label,"type":atype,"active":True}
            self.alarms.append(alarm)
            self.save();self.render_alarms()

    def render_alarms(self):
        self.alarm_list.config(state="normal")
        self.alarm_list.delete("1.0","end")
        if not self.alarms:
            self.alarm_list.insert("end","  No alarms set\n")
        for i,a in enumerate(self.alarms):
            tag="a" if a["active"] else "r"
            status="✅ ON" if a["active"] else "⏸ OFF"
            self.alarm_list.insert("end",
                f"  [{i+1}] ⏰ {a['time']} — {a['label']} ({a['type']}) {status}\n",tag)
        self.alarm_list.config(state="disabled")

    def check_loop(self):
        while True:
            now=datetime.now().strftime("%H:%M")
            for a in self.alarms:
                if a["active"] and a["time"]==now:
                    self.root.after(0,self.fire_alarm,a)
                    if a["type"]=="Once":a["active"]=False
                    self.save()
            time.sleep(30)

    def fire_alarm(self,alarm):
        subprocess.Popen(
            f'termux-notification --title "⏰ {alarm["label"]}" '
            f'--content "BrayoOS Alarm fired!" 2>/dev/null',shell=True)
        subprocess.Popen("termux-vibrate -d 1000 2>/dev/null",shell=True)
        subprocess.Popen(
            f'termux-tts-speak "Alarm: {alarm["label"]}" 2>/dev/null',shell=True)
        win=tk.Toplevel(self.root)
        win.configure(bg=RED);win.geometry("400x200")
        win.attributes("-topmost",True)
        tk.Label(win,text="⏰ ALARM!",font=("Courier",20,"bold"),
                bg=RED,fg=WHITE).pack(pady=20)
        tk.Label(win,text=alarm["label"],font=("Courier",14),
                bg=RED,fg=WHITE).pack()
        tk.Button(win,text="DISMISS",font=("Courier",12,"bold"),
                 bg=BG,fg=RED,relief="flat",padx=20,pady=8,
                 command=win.destroy).pack(pady=15)

    def delete_alarm(self):
        if self.alarms:
            self.alarms.pop()
            self.save();self.render_alarms()

    def dismiss_all(self):
        for a in self.alarms:a["active"]=False
        self.save();self.render_alarms()

if __name__=="__main__":
    root=tk.Tk();AlarmSystem(root);root.mainloop()
