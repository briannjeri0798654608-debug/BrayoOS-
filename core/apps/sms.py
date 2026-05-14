import tkinter as tk,subprocess
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A"
class SMS:
    def __init__(self,r):
        r.title("SMS");r.geometry("450x380");r.configure(bg=BG)
        tk.Label(r,text="◈ BRAYOOS SMS",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        pf=tk.Frame(r,bg=BG3);pf.pack(fill="x",padx=15,pady=8)
        tk.Label(pf,text="To:",font=("Courier",10),bg=BG3,fg=PURPLE).pack(side="left",padx=8)
        self.phone=tk.Entry(pf,font=("Courier",11),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
        self.phone.pack(side="left",fill="x",expand=True,ipady=6)
        tk.Label(r,text="Message:",font=("Courier",10),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.msg=tk.Text(r,height=8,bg=BG3,fg=WHITE,font=("Courier",10),relief="flat",insertbackground=NEON)
        self.msg.pack(fill="both",expand=True,padx=15,pady=5)
        tk.Button(r,text="📱 SEND",font=("Courier",11,"bold"),bg=PURPLE,fg=WHITE,
            relief="flat",padx=15,pady=8,command=self.send).pack(pady=6)
        self.st=tk.Label(r,text="",font=("Courier",9),bg=BG,fg=NEON);self.st.pack()
    def send(self):
        p=self.phone.get().strip();m=self.msg.get("1.0","end").strip()
        if p and m:
            subprocess.Popen(f'termux-sms-send -n "{p}" "{m}" 2>/dev/null',shell=True)
            self.st.config(text=f"✅ Sent to {p}");self.msg.delete("1.0","end")
        else:self.st.config(text="⚠️ Enter phone and message")
if __name__=="__main__":
    r=tk.Tk();SMS(r);r.mainloop()
