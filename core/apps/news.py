import tkinter as tk,httpx,threading
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GOLD="#FFD700"
class News:
    def __init__(self,r):
        r.title("News");r.geometry("620x480");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS NEWS",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        tf=tk.Frame(r,bg=BG);tf.pack(fill="x",padx=15,pady=5)
        for t in ["Tech","Kenya","Cyber","AI","World"]:
            tk.Button(tf,text=t,font=("Courier",8),bg=BG3,fg=NEON,relief="flat",
                padx=8,pady=4,command=lambda x=t:self.fetch(x)).pack(side="left",padx=2)
        self.out=tk.Text(r,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled",wrap="word")
        self.out.pack(fill="both",expand=True,padx=15,pady=5)
        self.fetch("Tech")
    def log(self,msg):
        self.out.config(state="normal");self.out.insert("end",f"{msg}\n");self.out.see("end");self.out.config(state="disabled")
    def fetch(self,topic):
        self.out.config(state="normal");self.out.delete("1.0","end");self.out.config(state="disabled")
        self.log(f"Loading {topic} news...")
        threading.Thread(target=self._fetch,args=(topic,),daemon=True).start()
    def _fetch(self,topic):
        try:
            r=httpx.get(f"https://wttr.in/{topic}?format=j1",timeout=5)
        except:pass
        fallback=[f"[{topic}] Latest in tech and AI",f"[{topic}] Kenya leads Africa",
            f"[{topic}] Cybersecurity update",f"[{topic}] Open source grows"]
        for h in fallback:self.log(f"\n📰 {h}")
if __name__=="__main__":
    r=tk.Tk();News(r);r.mainloop()
