import tkinter as tk
import threading,httpx,time,os
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class SpeedTest:
    def __init__(self,root):
        self.root=root
        self.root.title("🚀 Speed Test")
        self.root.geometry("600x500")
        self.root.configure(bg=BG)
        self.running=False
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🚀 BRAYOOS SPEED TEST",
                font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Test your internet speed",
                font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Big speed display
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("DOWNLOAD",GREEN),("UPLOAD","#FF6600"),
            ("PING",GOLD),("JITTER",NEON)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=5,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=2)
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",16,"bold"),bg=BG3,fg=color).pack()
            tk.Label(f,text="Mbps" if lbl!="PING" and lbl!="JITTER" else "ms",
                    font=("Courier",7),bg=BG3,fg=DIM).pack(pady=2)

        # Speed meter
        tk.Label(self.root,text="◈ SPEED METER",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.meter=tk.Canvas(self.root,width=560,height=30,
                            bg="#001100",highlightthickness=0)
        self.meter.pack(padx=15,pady=5)

        # Log
        tk.Label(self.root,text="◈ TEST LOG",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.log_box=tk.Text(self.root,height=10,bg=BG3,fg=WHITE,
                            font=("Courier",9),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=5)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("y",foreground=GOLD)

        self.test_btn=tk.Button(self.root,text="▶ START TEST",
                               font=("Courier",11,"bold"),bg=PURPLE,
                               fg=WHITE,relief="flat",padx=20,pady=8,
                               command=self.start)
        self.test_btn.pack(pady=8)
        tk.Label(self.root,text="BrayoOS Speed Test v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def log(self,msg,tag="g"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def draw_meter(self,speed,max_speed=100):
        self.meter.delete("all")
        pct=min(100,int(speed*100/max_speed))
        w=int(560*pct/100)
        color=RED if speed<5 else GOLD if speed<20 else GREEN
        if w>0:self.meter.create_rectangle(0,0,w,30,fill=color,outline="")
        self.meter.create_text(280,15,text=f"{speed:.1f} Mbps",
                              fill=WHITE,font=("Courier",10,"bold"))

    def start(self):
        if self.running:return
        self.running=True
        self.test_btn.config(text="Testing...",state="disabled",bg=DIM)
        for v in self.svars.values():v.set("--")
        threading.Thread(target=self._run_test,daemon=True).start()

    def _run_test(self):
        self.root.after(0,self.log,"Starting speed test...")

        # Ping test
        self.root.after(0,self.log,"Testing ping to 8.8.8.8...")
        import subprocess
        try:
            r=subprocess.check_output(
                "ping -c 4 8.8.8.8 2>/dev/null | tail -1",
                shell=True,timeout=10).decode()
            if "avg" in r:
                ping=float(r.split("/")[4])
                jitter=float(r.split("/")[5])
                self.root.after(0,self.svars["PING"].set,f"{ping:.0f}")
                self.root.after(0,self.svars["JITTER"].set,f"{jitter:.0f}")
                self.root.after(0,self.log,f"Ping: {ping:.0f}ms Jitter: {jitter:.0f}ms","g")
        except:
            self.root.after(0,self.svars["PING"].set,"?")
            self.root.after(0,self.log,"Ping test failed","r")

        # Download test
        self.root.after(0,self.log,"Testing download speed...")
        try:
            urls=["https://httpbin.org/bytes/1000000",
                  "https://speed.cloudflare.com/__down?bytes=1000000"]
            start=time.time()
            total=0
            for url in urls[:1]:
                r=httpx.get(url,timeout=15)
                total+=len(r.content)
            elapsed=time.time()-start
            dl=round((total*8/1024/1024)/elapsed,2)
            self.root.after(0,self.svars["DOWNLOAD"].set,str(dl))
            self.root.after(0,self.draw_meter,dl)
            self.root.after(0,self.log,f"Download: {dl} Mbps","g")
        except Exception as e:
            self.root.after(0,self.svars["DOWNLOAD"].set,"Err")
            self.root.after(0,self.log,f"Download failed: {e}","r")

        # Upload test
        self.root.after(0,self.log,"Testing upload speed...")
        try:
            data=b"x"*500000
            start=time.time()
            httpx.post("https://httpbin.org/post",content=data,timeout=15)
            elapsed=time.time()-start
            ul=round((len(data)*8/1024/1024)/elapsed,2)
            self.root.after(0,self.svars["UPLOAD"].set,str(ul))
            self.root.after(0,self.log,f"Upload: {ul} Mbps","g")
        except Exception as e:
            self.root.after(0,self.svars["UPLOAD"].set,"Err")
            self.root.after(0,self.log,f"Upload failed: {e}","r")

        self.root.after(0,self.log,"✅ Speed test complete!","g")
        self.running=False
        self.root.after(0,self.test_btn.config,
                       {"text":"▶ START TEST","state":"normal","bg":PURPLE})

if __name__=="__main__":
    root=tk.Tk();SpeedTest(root);root.mainloop()
