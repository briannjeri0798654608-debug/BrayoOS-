import tkinter as tk
import os,json
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

FILE=os.path.expanduser("~/BrayoOS/memory/budget.json")
os.makedirs(os.path.dirname(FILE),exist_ok=True)

class BudgetManager:
    def __init__(self,root):
        self.root=root
        self.root.title("💰 Budget Manager")
        self.root.geometry("660x540")
        self.root.configure(bg=BG)
        self.data=self.load()
        self.build_ui()

    def load(self):
        if os.path.exists(FILE):
            with open(FILE) as f:return json.load(f)
        return {"income":[],"expenses":[],"budget":10000}

    def save(self):
        with open(FILE,"w") as f:json.dump(self.data,f,indent=2)

    def build_ui(self):
        tk.Label(self.root,text="💰 BUDGET MANAGER",
                font=("Courier",15,"bold"),bg=BG,fg=GOLD).pack(pady=8)
        tk.Label(self.root,text="Track income & expenses — KES",
                font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=GOLD,height=2).pack(fill="x",pady=5)

        # Overview
        income=sum(t["amount"] for t in self.data.get("income",[]))
        expenses=sum(t["amount"] for t in self.data.get("expenses",[]))
        balance=income-expenses
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=5)
        for col,(lbl,val,color) in enumerate([
            ("INCOME",f"KES {income:,.0f}",GREEN),
            ("EXPENSES",f"KES {expenses:,.0f}",RED),
            ("BALANCE",f"KES {balance:,.0f}",GREEN if balance>=0 else RED),
            ("BUDGET",f"KES {self.data['budget']:,.0f}",GOLD)]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            tk.Label(f,text=val,font=("Courier",10,"bold"),bg=BG3,fg=color).pack(pady=2)

        # Spending bar
        if income>0:
            pct=min(100,int(expenses*100/income))
            bar_f=tk.Frame(self.root,bg=BG3);bar_f.pack(fill="x",padx=15,pady=3)
            bar=tk.Canvas(bar_f,width=620,height=10,bg="#001100",highlightthickness=0)
            bar.pack(padx=5,pady=5)
            w=int(620*pct/100)
            color=RED if pct>80 else GOLD if pct>50 else GREEN
            if w>0:bar.create_rectangle(0,0,w,10,fill=color,outline="")

        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True,padx=10)
        # Add transaction
        left=tk.Frame(main,bg=BG);left.pack(side="left",fill="y",padx=(0,8))
        tk.Label(left,text="◈ ADD TRANSACTION",
                font=("Courier",9,"bold"),bg=BG,fg=GOLD).pack(anchor="w")
        af=tk.Frame(left,bg=BG3);af.pack(fill="x",pady=5)
        self.fields={}
        for label,default in [("Description","Lunch"),("Amount (KES)","500")]:
            row=tk.Frame(af,bg=BG3);row.pack(fill="x",padx=8,pady=4)
            tk.Label(row,text=label+":",font=("Courier",8),
                    bg=BG3,fg=DIM).pack(anchor="w")
            e=tk.Entry(row,font=("Courier",10),bg=BG,fg=WHITE,
                      insertbackground=NEON,relief="flat")
            e.insert(0,default);e.pack(fill="x",ipady=5)
            self.fields[label]=e

        self.type_var=tk.StringVar(value="expense")
        tf=tk.Frame(af,bg=BG3);tf.pack(fill="x",padx=8,pady=4)
        for t,label,color in [("income","💚 Income",GREEN),("expense","❌ Expense",RED)]:
            tk.Radiobutton(tf,text=label,variable=self.type_var,value=t,
                          bg=BG3,fg=color,selectcolor=PURPLE,
                          activebackground=BG3,
                          font=("Courier",9)).pack(side="left",padx=8)
        tk.Button(af,text="➕ ADD",font=("Courier",10,"bold"),
                 bg=GOLD,fg=BG,relief="flat",padx=12,pady=5,
                 command=self.add_transaction).pack(pady=8)

        # Transactions list
        right=tk.Frame(main,bg=BG);right.pack(side="left",fill="both",expand=True)
        tk.Label(right,text="◈ TRANSACTIONS",
                font=("Courier",9,"bold"),bg=BG,fg=GOLD).pack(anchor="w")
        self.trans_box=tk.Text(right,bg=BG3,fg=WHITE,
                              font=("Courier",8),relief="flat",
                              state="disabled")
        self.trans_box.pack(fill="both",expand=True,pady=5)
        self.trans_box.tag_config("i",foreground=GREEN)
        self.trans_box.tag_config("e",foreground=RED)
        bf=tk.Frame(right,bg=BG);bf.pack()
        tk.Button(bf,text="🗑 Clear All",font=("Courier",8),
                 bg=BG3,fg=RED,relief="flat",padx=8,pady=3,
                 command=self.clear_all).pack(side="left",padx=3)
        tk.Label(self.root,text="BrayoOS Budget Manager v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)
        self.render_transactions()

    def add_transaction(self):
        desc=self.fields["Description"].get().strip()
        try:amount=float(self.fields["Amount (KES)"].get())
        except:return
        ttype=self.type_var.get()
        entry={"desc":desc,"amount":amount,
               "date":datetime.now().strftime("%Y-%m-%d %H:%M")}
        self.data[ttype+"s" if ttype=="expense" else "income"].append(entry)
        self.save()
        for w in self.root.winfo_children():w.destroy()
        self.build_ui()

    def render_transactions(self):
        self.trans_box.config(state="normal")
        self.trans_box.delete("1.0","end")
        all_trans=[]
        for t in self.data.get("income",[]):
            all_trans.append(("i",t))
        for t in self.data.get("expenses",[]):
            all_trans.append(("e",t))
        if not all_trans:
            self.trans_box.insert("end","  No transactions yet\n")
        for tag,t in reversed(all_trans[-20:]):
            symbol="+" if tag=="i" else "-"
            self.trans_box.insert("end",
                f"  {symbol} KES {t['amount']:,.0f} — {t['desc']} ({t['date']})\n",tag)
        self.trans_box.config(state="disabled")

    def clear_all(self):
        self.data={"income":[],"expenses":[],"budget":self.data.get("budget",10000)}
        self.save()
        for w in self.root.winfo_children():w.destroy()
        self.build_ui()

if __name__=="__main__":
    root=tk.Tk();BudgetManager(root);root.mainloop()
