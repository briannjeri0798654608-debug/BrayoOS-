import tkinter as tk
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A"
class Calc:
    def __init__(self,r):
        r.title("Calc");r.geometry("320x480");r.configure(bg=BG)
        tk.Label(r,text="◈ CALCULATOR",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        self.expr=""
        self.disp=tk.Label(r,text="0",font=("Courier",22,"bold"),bg=BG3,fg=WHITE,anchor="e",width=18)
        self.disp.pack(padx=15,pady=5,fill="x")
        for row in [["C","⌫","%","÷"],["7","8","9","×"],["4","5","6","−"],["1","2","3","+"],["+/-","0",".","="]]:
            f=tk.Frame(r,bg=BG);f.pack(fill="x",padx=15,pady=2)
            for b in row:
                c=PURPLE if b in["=","÷","×","−","+"] else BG3
                tk.Button(f,text=b,font=("Courier",14,"bold"),bg=c,fg=WHITE,relief="flat",
                    width=4,height=2,command=lambda x=b:self.press(x)).pack(side="left",padx=2)
    def press(self,k):
        if k=="C":self.expr=""
        elif k=="⌫":self.expr=self.expr[:-1]
        elif k=="=":
            try:self.expr=str(eval(self.expr.replace("÷","/").replace("×","*").replace("−","-")))
            except:self.expr="Error"
        elif k=="+/-":self.expr=str(-float(self.expr)) if self.expr else ""
        else:self.expr+=k
        self.disp.config(text=self.expr or "0")
if __name__=="__main__":
    r=tk.Tk();Calc(r);r.mainloop()
