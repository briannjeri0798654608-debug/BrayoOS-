import tkinter as tk
import subprocess
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A"
class Browser:
    def __init__(self,r):
        r.title("Browser");r.geometry("650x480");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS BROWSER",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        bf=tk.Frame(r,bg=BG);bf.pack(fill="x",padx=10,pady=8)
        tk.Label(bf,text="URL:",font=("Courier",10),bg=BG,fg=PURPLE).pack(side="left",padx=5)
        self.url=tk.Entry(bf,font=("Courier",11),bg=BG3,fg=WHITE,insertbackground=NEON,relief="flat")
        self.url.pack(side="left",fill="x",expand=True,ipady=7)
        self.url.insert(0,"https://google.com")
        self.url.bind("<Return>",lambda e:self.go())
        tk.Button(bf,text="GO ▶",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
            relief="flat",padx=12,command=self.go).pack(side="right",padx=5,pady=4)
        qf=tk.Frame(r,bg=BG);qf.pack(fill="x",padx=10)
        for q in ["google.com","github.com","youtube.com","termux.dev"]:
            tk.Button(qf,text=q,font=("Courier",8),bg=BG3,fg=NEON,relief="flat",
                padx=8,pady=3,command=lambda u=q:self.open(u)).pack(side="left",padx=2)
        self.out=tk.Text(r,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.out.pack(fill="both",expand=True,padx=10,pady=5)
        self.log("BrayoOS Browser — Enter URL and press GO")
    def log(self,msg):
        self.out.config(state="normal");self.out.insert("end",f"{msg}\n");self.out.see("end");self.out.config(state="disabled")
    def go(self):self.open(self.url.get())
    def open(self,url):
        if not url.startswith("http"):url="https://"+url
        self.log(f"Opening: {url}")
        subprocess.Popen(f'termux-open-url "{url}" 2>/dev/null || xdg-open "{url}" 2>/dev/null',shell=True)
if __name__=="__main__":
    r=tk.Tk();Browser(r);r.mainloop()
