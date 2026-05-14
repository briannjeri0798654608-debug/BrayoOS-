import tkinter as tk
import subprocess
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GOLD="#FFD700"
class Settings:
    def __init__(self,r):
        r.title("Settings");r.geometry("500x480");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS SETTINGS",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        for section,items in [
            ("🖥️ DISPLAY",["VNC: 1280x800","Depth: 24bit","DPI: 96"]),
            ("🤖 AIRA",["Model: LLaMA 3.3 70B","Provider: Groq","Memory: 50 chats"]),
            ("🔒 SECURITY",["DNA Vault PIN: ****","Ghost Mode: OFF","OSINT: READY"]),
            ("📊 SYSTEM",["Version: BrayoOS v3.5","Apps: 33","Built: Kenya 🇰🇪"]),
        ]:
            tk.Label(r,text=section,font=("Courier",10,"bold"),bg=BG,fg=GOLD).pack(anchor="w",padx=15,pady=(10,3))
            for item in items:
                f=tk.Frame(r,bg=BG3);f.pack(fill="x",padx=15,pady=1)
                tk.Label(f,text=f"  {item}",font=("Courier",9),bg=BG3,fg=WHITE).pack(anchor="w",padx=5,pady=4)
        bf=tk.Frame(r,bg=BG);bf.pack(pady=10)
        tk.Button(bf,text="🔄 Restart",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,relief="flat",padx=12,pady=6,
            command=lambda:subprocess.Popen("pkill -f desktop.py;sleep 1;DISPLAY=:1 python3 ~/BrayoOS/core/desktop.py &",shell=True)
        ).pack(side="left",padx=5)
        tk.Button(bf,text="⏹ Stop All",font=("Courier",10,"bold"),bg=BG3,fg="#FF0044",relief="flat",padx=12,pady=6,
            command=lambda:subprocess.Popen("pkill -f python3",shell=True)).pack(side="left",padx=5)
if __name__=="__main__":
    r=tk.Tk();Settings(r);r.mainloop()
