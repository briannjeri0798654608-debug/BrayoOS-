import tkinter as tk
import subprocess,os,glob
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GOLD="#FFD700"
class Music:
    def __init__(self,r):
        r.title("Music");r.geometry("500x400");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS MUSIC",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        self.now=tk.Label(r,text="♫ No track playing",font=("Courier",11),bg=BG,fg=GOLD)
        self.now.pack(pady=10)
        self.pl=tk.Listbox(r,bg=BG3,fg=WHITE,font=("Courier",9),selectbackground=PURPLE,relief="flat",height=12)
        self.pl.pack(fill="both",expand=True,padx=15,pady=5)
        bf=tk.Frame(r,bg=BG);bf.pack(pady=8)
        for t,c in [("▶ PLAY","play"),("⏸ PAUSE","pause"),("⏹ STOP","stop")]:
            tk.Button(bf,text=t,font=("Courier",10,"bold"),bg=BG3,fg=NEON,relief="flat",
                padx=10,pady=6,command=lambda x=c:self.ctrl(x)).pack(side="left",padx=3)
        self.load()
    def load(self):
        paths=glob.glob(os.path.expanduser("~/Music/*"))+glob.glob("/sdcard/Music/*")
        for p in paths:
            if p.endswith((".mp3",".wav",".ogg",".m4a")):self.pl.insert("end",os.path.basename(p))
        if not self.pl.size():self.pl.insert("end","Add music to ~/Music/")
    def ctrl(self,cmd):
        if cmd=="play":
            sel=self.pl.curselection()
            if sel:
                t=self.pl.get(sel[0]);self.now.config(text=f"♫ {t}")
                subprocess.Popen(f'termux-media-player play ~/Music/"{t}" 2>/dev/null',shell=True)
        elif cmd=="pause":subprocess.Popen("termux-media-player pause 2>/dev/null",shell=True)
        elif cmd=="stop":subprocess.Popen("termux-media-player stop 2>/dev/null",shell=True)
if __name__=="__main__":
    r=tk.Tk();Music(r);r.mainloop()
