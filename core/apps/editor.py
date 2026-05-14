import tkinter as tk
from tkinter import filedialog
import os,subprocess
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A"
class Editor:
    def __init__(self,r):
        r.title("Editor");r.geometry("700x550");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS EDITOR",font=("Courier",12,"bold"),bg=BG,fg=NEON).pack(pady=5)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        bf=tk.Frame(r,bg=BG);bf.pack(fill="x",padx=10,pady=5)
        for txt,cmd in [("📂 Open","open"),("💾 Save","save"),("🆕 New","new"),("▶ Run","run")]:
            tk.Button(bf,text=txt,font=("Courier",9,"bold"),bg=BG3,fg=NEON,relief="flat",
                padx=10,pady=4,command=lambda c=cmd:self.action(c)).pack(side="left",padx=3)
        self.fl=tk.Label(bf,text="untitled.py",font=("Courier",8),bg=BG,fg="#444466")
        self.fl.pack(side="right",padx=10)
        self.text=tk.Text(r,bg=BG3,fg=WHITE,font=("Courier",11),insertbackground=NEON,relief="flat",undo=True)
        self.text.pack(fill="both",expand=True,padx=10,pady=5)
        self.text.insert("end","# BrayoOS Editor\n")
        self.cf=None
    def action(self,cmd):
        if cmd=="new":self.text.delete("1.0","end");self.cf=None;self.fl.config(text="untitled.py")
        elif cmd=="open":
            f=filedialog.askopenfilename()
            if f:self.cf=f;self.fl.config(text=os.path.basename(f));self.text.delete("1.0","end");self.text.insert("end",open(f).read())
        elif cmd=="save":
            if not self.cf:self.cf=filedialog.asksaveasfilename(defaultextension=".py")
            if self.cf:open(self.cf,"w").write(self.text.get("1.0","end"));self.fl.config(text=os.path.basename(self.cf))
        elif cmd=="run":
            if self.cf:subprocess.Popen(["python3",self.cf])
if __name__=="__main__":
    r=tk.Tk();Editor(r);r.mainloop()
