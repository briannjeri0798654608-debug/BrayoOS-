import tkinter as tk
import subprocess,os,threading
from datetime import datetime
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GREEN="#44FF88"
class Backup:
    def __init__(self,r):
        r.title("Backup");r.geometry("500x400");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS BACKUP",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        self.log_box=tk.Text(r,height=14,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=8)
        bf=tk.Frame(r,bg=BG);bf.pack(pady=8)
        tk.Button(bf,text="💾 Local Backup",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,relief="flat",
            padx=12,pady=6,command=lambda:threading.Thread(target=self.local,daemon=True).start()).pack(side="left",padx=5)
        tk.Button(bf,text="☁️ GitHub Push",font=("Courier",10,"bold"),bg=BG3,fg=GREEN,relief="flat",
            padx=12,pady=6,command=lambda:threading.Thread(target=self.github,daemon=True).start()).pack(side="left",padx=5)
    def log(self,msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end",f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see("end");self.log_box.config(state="disabled")
    def local(self):
        ts=datetime.now().strftime("%Y%m%d_%H%M")
        dest=os.path.expanduser(f"~/BrayoOS/backups/backup_{ts}")
        self.log(f"Backing up to {dest}...")
        os.makedirs(dest,exist_ok=True)
        subprocess.run(f"cp -r ~/BrayoOS/core {dest}/ && cp -r ~/BrayoOS/memory {dest}/",shell=True)
        self.log("✅ Backup done!")
    def github(self):
        self.log("Pushing to GitHub...")
        r=subprocess.run('cd ~/BrayoOS && git add -A && git commit -m "Auto backup" && git push origin main',
            shell=True,capture_output=True,text=True)
        self.log("✅ Pushed!" if r.returncode==0 else f"⚠️ {r.stderr[:40]}")
if __name__=="__main__":
    r=tk.Tk();Backup(r);r.mainloop()
