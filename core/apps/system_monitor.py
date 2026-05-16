import tkinter as tk
import threading
import time
import os
import subprocess
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class SystemMonitor:
    def __init__(self,root):
        self.root=root
        self.root.title("📊 System Monitor")
        self.root.geometry("680x120+0+0")
        self.root.configure(bg=BG2)
        self.root.resizable(False,False)
        self.root.attributes("-topmost",True)
        self.running=True
        self.build_ui()
        threading.Thread(target=self.update_loop,daemon=True).start()

    def build_ui(self):
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")
        main=tk.Frame(self.root,bg=BG2)
        main.pack(fill="both",expand=True,padx=8,pady=4)

        # Title
        left=tk.Frame(main,bg=BG2)
        left.pack(side="left",padx=8)
        tk.Label(left,text="◈ BRAYOOS",font=("Courier",9,"bold"),bg=BG2,fg=NEON).pack(anchor="w")
        tk.Label(left,text="SYSTEM MONITOR",font=("Courier",7),bg=BG2,fg=DIM).pack(anchor="w")
        self.time_lbl=tk.Label(left,text="",font=("Courier",8),bg=BG2,fg=GOLD)
        self.time_lbl.pack(anchor="w",pady=2)

        tk.Frame(main,bg=PURPLE,width=1).pack(side="left",fill="y",padx=6)

        # Stats
        stats=tk.Frame(main,bg=BG2)
        stats.pack(side="left",fill="both",expand=True)

        row1=tk.Frame(stats,bg=BG2)
        row1.pack(fill="x",pady=1)
        row2=tk.Frame(stats,bg=BG2)
        row2.pack(fill="x",pady=1)

        self.widgets={}
        items=[
            ("CPU","%","#FF4444",row1),
            ("RAM","%","#FF6600",row1),
            ("TEMP","°C","#FF0044",row1),
            ("FREQ","MHz","#44FFFF",row1),
            ("STORAGE","%","#FFAA00",row2),
            ("UPTIME","","#44FF88",row2),
            ("PROCS","","#AAAAFF",row2),
            ("BATTERY","%","#FFD700",row2),
        ]
        for name,unit,color,parent in items:
            f=tk.Frame(parent,bg=BG3,padx=6,pady=3)
            f.pack(side="left",padx=3)
            tk.Label(f,text=name,font=("Courier",6),bg=BG3,fg=DIM).pack()
            v=tk.Label(f,text="--",font=("Courier",11,"bold"),bg=BG3,fg=color)
            v.pack()
            tk.Label(f,text=unit,font=("Courier",6),bg=BG3,fg=DIM).pack()
            self.widgets[name]=v

        tk.Frame(main,bg=PURPLE,width=1).pack(side="left",fill="y",padx=6)

        # Right — bar graphs
        bars=tk.Frame(main,bg=BG2)
        bars.pack(side="left",padx=8)
        tk.Label(bars,text="LOAD",font=("Courier",7),bg=BG2,fg=DIM).pack()
        self.cpu_canvas=tk.Canvas(bars,width=80,height=12,bg="#001100",highlightthickness=0)
        self.cpu_canvas.pack(pady=1)
        self.ram_canvas=tk.Canvas(bars,width=80,height=12,bg="#001100",highlightthickness=0)
        self.ram_canvas.pack(pady=1)
        self.bat_canvas=tk.Canvas(bars,width=80,height=12,bg="#001100",highlightthickness=0)
        self.bat_canvas.pack(pady=1)

        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",side="bottom")

    def draw_bar(self,canvas,pct,color):
        canvas.delete("all")
        w=int(80*pct/100)
        if w>0:canvas.create_rectangle(0,0,w,12,fill=color,outline="")

    def get_cpu(self):
        try:
            with open("/proc/stat") as f:line=f.readline().split()
            idle=int(line[4]);total=sum(int(x) for x in line[1:])
            return max(0,min(100,100-(idle*100//total)))
        except:return 0

    def get_ram(self):
        try:
            info={}
            with open("/proc/meminfo") as f:
                for line in f:
                    k,v=line.split()[0].rstrip(":"),int(line.split()[1])
                    info[k]=v
            used=info["MemTotal"]-info["MemAvailable"]
            return int(used*100/info["MemTotal"]),used//1024,info["MemTotal"]//1024
        except:return 0,0,0

    def get_temp(self):
        for p in ["/sys/class/thermal/thermal_zone0/temp","/sys/class/thermal/thermal_zone1/temp"]:
            try:
                with open(p) as f:return int(f.read().strip())//1000
            except:pass
        return 0

    def get_freq(self):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as f:
                return int(f.read().strip())//1000
        except:return 0

    def get_storage(self):
        try:
            s=os.statvfs(os.path.expanduser("~"))
            total=s.f_blocks*s.f_frsize
            free=s.f_bfree*s.f_frsize
            used=total-free
            return int(used*100/total) if total>0 else 0
        except:return 0

    def get_battery(self):
        paths=["/sys/class/power_supply/battery/capacity",
               "/sys/class/power_supply/BAT0/capacity"]
        for p in paths:
            try:
                with open(p) as f:return int(f.read().strip())
            except:pass
        return 0

    def get_procs(self):
        try:return len([p for p in os.listdir("/proc") if p.isdigit()])
        except:return 0

    def get_uptime(self):
        try:
            with open("/proc/uptime") as f:secs=float(f.read().split()[0])
            h=int(secs//3600);m=int((secs%3600)//60)
            return f"{h}h{m}m"
        except:return "?"

    def update_loop(self):
        while self.running:
            cpu=self.get_cpu()
            ram_pct,ram_used,ram_total=self.get_ram()
            temp=self.get_temp()
            freq=self.get_freq()
            storage=self.get_storage()
            uptime=self.get_uptime()
            procs=self.get_procs()
            battery=self.get_battery()
            now=datetime.now().strftime("%H:%M:%S %d/%m/%y")

            self.root.after(0,self.update_ui,cpu,ram_pct,ram_used,
                           ram_total,temp,freq,storage,uptime,procs,battery,now)
            time.sleep(2)

    def update_ui(self,cpu,ram_pct,ram_used,ram_total,temp,freq,
                  storage,uptime,procs,battery,now):
        cpu_col="#FF4444" if cpu>80 else "#FF6600" if cpu>50 else GREEN
        ram_col="#FF0044" if ram_pct>85 else "#FF6600" if ram_pct>60 else "#FF6600"
        bat_col=RED if battery<20 else GOLD if battery<50 else GREEN

        self.widgets["CPU"].config(text=str(cpu),fg=cpu_col)
        self.widgets["RAM"].config(text=str(ram_pct),fg=ram_col)
        self.widgets["TEMP"].config(text=str(temp),fg=RED if temp>45 else GOLD)
        self.widgets["FREQ"].config(text=str(freq),fg="#44FFFF")
        self.widgets["STORAGE"].config(text=str(storage))
        self.widgets["UPTIME"].config(text=uptime)
        self.widgets["PROCS"].config(text=str(procs))
        self.widgets["BATTERY"].config(text=str(battery),fg=bat_col)
        self.time_lbl.config(text=now)
        self.draw_bar(self.cpu_canvas,cpu,cpu_col)
        self.draw_bar(self.ram_canvas,ram_pct,ram_col)
        self.draw_bar(self.bat_canvas,battery,bat_col)

if __name__=="__main__":
    root=tk.Tk()
    SystemMonitor(root)
    root.mainloop()
