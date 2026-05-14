import tkinter as tk
import os,shutil
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GOLD="#FFD700"
class Files:
    def __init__(self,r):
        r.title("Files");r.geometry("600x500");r.configure(bg=BG)
        tk.Label(r,text="◈ FILE MANAGER",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        self.path=os.path.expanduser("~")
        self.pl=tk.Label(r,text=self.path,font=("Courier",9),bg=BG,fg=GOLD)
        self.pl.pack(anchor="w",padx=15,pady=3)
        self.lb=tk.Listbox(r,bg=BG3,fg=WHITE,font=("Courier",9),selectbackground=PURPLE,relief="flat",height=18)
        self.lb.pack(fill="both",expand=True,padx=15,pady=3)
        self.lb.bind("<Double-Button-1>",self.open_item)
        bf=tk.Frame(r,bg=BG);bf.pack(fill="x",padx=15,pady=5)
        for t,c in [("⬆ Up","up"),("🔄 Refresh","ref"),("🗑 Delete","del"),("📋 Copy Path","copy")]:
            tk.Button(bf,text=t,font=("Courier",8),bg=BG3,fg=NEON,relief="flat",
                padx=8,pady=4,command=lambda x=c:self.act(x)).pack(side="left",padx=3)
        self.load()
    def load(self):
        self.lb.delete(0,"end");self.pl.config(text=self.path)
        try:
            for i in sorted(os.listdir(self.path)):
                self.lb.insert("end",("📁 " if os.path.isdir(os.path.join(self.path,i)) else "📄 ")+i)
        except:self.lb.insert("end","Permission denied")
    def open_item(self,e):
        s=self.lb.curselection()
        if s:
            n=self.lb.get(s[0]).replace("📁 ","").replace("📄 ","")
            f=os.path.join(self.path,n)
            if os.path.isdir(f):self.path=f;self.load()
    def act(self,cmd):
        if cmd=="up":self.path=os.path.dirname(self.path);self.load()
        elif cmd=="ref":self.load()
        elif cmd=="copy":
            s=self.lb.curselection()
            if s:
                n=self.lb.get(s[0]).replace("📁 ","").replace("📄 ","")
                self.lb.master.clipboard_clear();self.lb.master.clipboard_append(os.path.join(self.path,n))
        elif cmd=="del":
            s=self.lb.curselection()
            if s:
                n=self.lb.get(s[0]).replace("📁 ","").replace("📄 ","")
                f=os.path.join(self.path,n)
                try:shutil.rmtree(f) if os.path.isdir(f) else os.remove(f);self.load()
                except:pass
if __name__=="__main__":
    r=tk.Tk();Files(r);r.mainloop()
