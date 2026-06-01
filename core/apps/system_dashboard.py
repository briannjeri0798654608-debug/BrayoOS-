import tkinter as tk
import threading,subprocess,os,time,json
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

class SystemDashboard:
    def __init__(self,root):
        self.root=root
        self.root.title("📊 System Dashboard")
        self.root.geometry("780x600")
        self.root.configure(bg=BG)
        self.running=True
        self.cpu_history=[0]*60
        self.ram_history=[0]*60
        self.build_ui()
        threading.Thread(target=self.update_loop,daemon=True).start()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="📊 SYSTEM DASHBOARD",font=("Courier",14,"bold"),bg=BG2,fg=GREEN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="BrayoOS v5.0 Live Monitor",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.time_lbl=tk.Label(hdr,text="",font=("Courier",9),bg=BG2,fg=NEON)
        self.time_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=GREEN,height=2).pack(fill="x")

        # Big stats
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=10,pady=8)
        self.big_stats={}
        for col,(lbl,color,icon) in enumerate([
            ("CPU %",RED,"⚡"),("RAM %","#FF6600","💾"),
            ("TEMP °C",GOLD,"🌡"),("BATTERY %",GREEN,"🔋"),
            ("STORAGE %","#AAAAFF","💿"),("PROCESSES",CYAN,"⚙")]):
            f=tk.Frame(sf,bg=BG3,highlightbackground=color,highlightthickness=1)
            f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=icon,font=("Arial",16),bg=BG3).pack(pady=(5,0))
            tk.Label(f,text=lbl,font=("Courier",6),bg=BG3,fg=DIM).pack()
            v=tk.StringVar(value="--")
            self.big_stats[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",14,"bold"),bg=BG3,fg=color).pack(pady=(0,5))

        # CPU graph
        graphs=tk.Frame(self.root,bg=BG);graphs.pack(fill="x",padx=10,pady=5)
        left=tk.Frame(graphs,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(0,5))
        tk.Label(left,text="◈ CPU USAGE (60s)",font=("Courier",8,"bold"),bg=BG,fg=RED).pack(anchor="w")
        self.cpu_canvas=tk.Canvas(left,width=370,height=80,bg=BG3,highlightthickness=1,highlightbackground=RED)
        self.cpu_canvas.pack(fill="x",pady=2)

        right=tk.Frame(graphs,bg=BG);right.pack(side="left",fill="both",expand=True)
        tk.Label(right,text="◈ RAM USAGE (60s)",font=("Courier",8,"bold"),bg=BG,fg="#FF6600").pack(anchor="w")
        self.ram_canvas=tk.Canvas(right,width=370,height=80,bg=BG3,highlightthickness=1,highlightbackground="#FF6600")
        self.ram_canvas.pack(fill="x",pady=2)

        # Process list
        tk.Label(self.root,text="◈ TOP PROCESSES",font=("Courier",8,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=10,pady=(5,2))
        self.proc_box=tk.Text(self.root,height=6,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.proc_box.pack(fill="x",padx=10,pady=2)
        self.proc_box.tag_config("h",foreground=CYAN)

        # Quick actions
        tk.Label(self.root,text="◈ QUICK ACTIONS",font=("Courier",8,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=10,pady=(5,2))
        af=tk.Frame(self.root,bg=BG);af.pack(fill="x",padx=10)
        actions=[
            ("🔄 Restart BrayoOS","pkill -f desktop.py; sleep 1; DISPLAY=:1 python3 ~/BrayoOS/core/desktop.py &",GREEN),
            ("🗑 Clear Cache","find ~/BrayoOS -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null",GOLD),
            ("☁️ Backup Now","cd ~/BrayoOS && git add -A && git commit -m 'Auto backup' && git push origin main &",CYAN),
            ("💀 Kill All Python","pkill -f python3 2>/dev/null",RED),
        ]
        for label,cmd,color in actions:
            tk.Button(af,text=label,font=("Courier",8),bg=BG3,fg=color,
                     relief="flat",padx=8,pady=5,
                     command=lambda c=cmd:subprocess.Popen(c,shell=True)).pack(side="left",padx=3)

        tk.Label(self.root,text="BrayoOS System Dashboard v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

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
                    parts=line.split()
                    if len(parts)>=2:info[parts[0].rstrip(":")]=int(parts[1])
            used=info.get("MemTotal",0)-info.get("MemAvailable",0)
            total=info.get("MemTotal",1)
            return int(used*100/total)
        except:return 0

    def get_temp(self):
        for p in ["/sys/class/thermal/thermal_zone0/temp",
                  "/sys/class/thermal/thermal_zone1/temp"]:
            try:
                with open(p) as f:return int(f.read().strip())//1000
            except:pass
        return 0

    def get_battery(self):
        try:
            r=subprocess.check_output("termux-battery-status 2>/dev/null",
                                     shell=True,timeout=2).decode()
            d=json.loads(r)
            return d.get("percentage",0)
        except:return 0

    def get_storage(self):
        try:
            s=os.statvfs(os.path.expanduser("~"))
            total=s.f_blocks*s.f_frsize
            free=s.f_bfree*s.f_frsize
            return int((total-free)*100/total) if total>0 else 0
        except:return 0

    def draw_graph(self,canvas,history,color,width=370):
        canvas.delete("all")
        canvas.create_rectangle(0,0,width,80,fill=BG3,outline="")
        # Grid lines
        for y in [20,40,60]:
            canvas.create_line(0,y,width,y,fill="#111122",width=1)
        for x in range(0,width,30):
            canvas.create_line(x,0,x,80,fill="#111122",width=1)
        # Line graph
        if len(history)>1:
            points=[]
            for i,val in enumerate(history):
                x=int(i*(width/len(history)))
                y=int(80-(val*80/100))
                points.extend([x,y])
            if len(points)>=4:
                canvas.create_line(points,fill=color,width=2,smooth=True)
            # Fill area
            fill_points=[0,80]+points+[width,80]
            canvas.create_polygon(fill_points,fill=color+"33",outline="")
        # Current value
        if history:
            canvas.create_text(width-30,10,text=f"{history[-1]}%",
                             fill=color,font=("Courier",8,"bold"))

    def update_procs(self):
        try:
            result=subprocess.check_output(
                "ps aux --sort=-%cpu 2>/dev/null | head -8",
                shell=True,timeout=3).decode()
            self.proc_box.config(state="normal")
            self.proc_box.delete("1.0","end")
            lines=result.strip().split("\n")
            if lines:
                self.proc_box.insert("end",lines[0][:80]+"\n","h")
                for line in lines[1:6]:
                    self.proc_box.insert("end",line[:80]+"\n")
            self.proc_box.config(state="disabled")
        except:pass

    def update_loop(self):
        while self.running:
            cpu=self.get_cpu()
            ram=self.get_ram()
            temp=self.get_temp()
            bat=self.get_battery()
            stor=self.get_storage()
            procs=len([p for p in os.listdir("/proc") if p.isdigit()])
            self.cpu_history.append(cpu);self.cpu_history=self.cpu_history[-60:]
            self.ram_history.append(ram);self.ram_history=self.ram_history[-60:]
            cpu_col=RED if cpu>80 else GOLD if cpu>50 else GREEN
            ram_col=RED if ram>85 else GOLD if ram>60 else "#FF6600"
            bat_col=RED if bat<20 else GOLD if bat<50 else GREEN
            self.root.after(0,self.big_stats["CPU %"].set,str(cpu))
            self.root.after(0,self.big_stats["RAM %"].set,str(ram))
            self.root.after(0,self.big_stats["TEMP °C"].set,str(temp))
            self.root.after(0,self.big_stats["BATTERY %"].set,str(bat))
            self.root.after(0,self.big_stats["STORAGE %"].set,str(stor))
            self.root.after(0,self.big_stats["PROCESSES"].set,str(procs))
            self.root.after(0,self.draw_graph,self.cpu_canvas,self.cpu_history,RED)
            self.root.after(0,self.draw_graph,self.ram_canvas,self.ram_history,"#FF6600")
            self.root.after(0,self.time_lbl.config,
                           {"text":datetime.now().strftime("%H:%M:%S")})
            if self.running:self.root.after(0,self.update_procs)
            time.sleep(2)

if __name__=="__main__":
    root=tk.Tk();SystemDashboard(root);root.mainloop()
