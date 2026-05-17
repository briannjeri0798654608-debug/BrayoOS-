import tkinter as tk
import threading,httpx,json,os
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

WALLETS_FILE=os.path.expanduser("~/BrayoOS/memory/wallets.json")
os.makedirs(os.path.dirname(WALLETS_FILE),exist_ok=True)

class CryptoWallet:
    def __init__(self,root):
        self.root=root
        self.root.title("💰 Crypto Wallet")
        self.root.geometry("620x560")
        self.root.configure(bg=BG)
        self.wallets=self.load()
        self.build_ui()
        self.refresh()

    def load(self):
        if os.path.exists(WALLETS_FILE):
            with open(WALLETS_FILE) as f:return json.load(f)
        return []

    def save(self):
        with open(WALLETS_FILE,"w") as f:json.dump(self.wallets,f,indent=2)

    def build_ui(self):
        tk.Label(self.root,text="💰 CRYPTO WALLET TRACKER",font=("Courier",14,"bold"),bg=BG,fg=GOLD).pack(pady=8)
        tk.Label(self.root,text="Track your crypto portfolio",font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=GOLD,height=2).pack(fill="x",pady=6)

        # Portfolio value
        self.total_lbl=tk.Label(self.root,text="TOTAL: $0.00",font=("Courier",18,"bold"),bg=BG,fg=GOLD)
        self.total_lbl.pack(pady=5)

        # Prices
        tk.Label(self.root,text="◈ LIVE PRICES",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.price_box=tk.Text(self.root,height=6,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.price_box.pack(fill="x",padx=15,pady=3)
        self.price_box.tag_config("g",foreground=GREEN)
        self.price_box.tag_config("r",foreground=RED)
        self.price_box.tag_config("y",foreground=GOLD)

        # Add wallet
        tk.Label(self.root,text="◈ ADD TO PORTFOLIO",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(8,2))
        af=tk.Frame(self.root,bg=BG3);af.pack(fill="x",padx=15,pady=3)
        tk.Label(af,text="Coin:",font=("Courier",9),bg=BG3,fg=DIM).pack(side="left",padx=8,pady=8)
        self.coin_var=tk.StringVar(value="bitcoin")
        tk.OptionMenu(af,self.coin_var,"bitcoin","ethereum","solana","cardano","dogecoin").pack(side="left",padx=5)
        tk.Label(af,text="Amount:",font=("Courier",9),bg=BG3,fg=DIM).pack(side="left",padx=8)
        self.amount_e=tk.Entry(af,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat",width=10)
        self.amount_e.pack(side="left",ipady=5)
        self.amount_e.insert(0,"0.001")
        tk.Button(af,text="➕ ADD",font=("Courier",9,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=10,pady=5,command=self.add_wallet).pack(side="right",padx=8,pady=4)

        # Holdings
        tk.Label(self.root,text="◈ MY HOLDINGS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(6,2))
        self.hold_box=tk.Text(self.root,height=5,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.hold_box.pack(fill="both",expand=True,padx=15,pady=3)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        tk.Button(bf,text="🔄 Refresh",font=("Courier",10,"bold"),bg=GOLD,fg="#000",
                 relief="flat",padx=12,pady=5,command=self.refresh).pack(side="left",padx=4)
        tk.Button(bf,text="🗑 Clear",font=("Courier",10,"bold"),bg=BG3,fg=RED,
                 relief="flat",padx=12,pady=5,command=self.clear).pack(side="left",padx=4)
        tk.Label(self.root,text="BrayoOS Crypto Wallet • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def refresh(self):
        threading.Thread(target=self._refresh,daemon=True).start()

    def _refresh(self):
        try:
            coins="bitcoin,ethereum,solana,cardano,dogecoin,binancecoin"
            r=httpx.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd&include_24hr_change=true",timeout=10)
            self.prices=r.json()
            self.root.after(0,self._update_ui)
        except:
            self.prices={}
            self.root.after(0,self.price_box.config,{"state":"normal"})
            self.root.after(0,self.price_box.insert,"end","⚠️ No internet connection\n")
            self.root.after(0,self.price_box.config,{"state":"disabled"})

    def _update_ui(self):
        self.price_box.config(state="normal");self.price_box.delete("1.0","end")
        total=0
        for coin,data in self.prices.items():
            p=data.get("usd",0);c=data.get("usd_24h_change",0)
            tag="g" if c>=0 else "r"
            arrow="▲" if c>=0 else "▼"
            self.price_box.insert("end",f"  {coin.upper():<12} ${p:>10,.2f}  {arrow}{abs(c):.2f}%\n",tag)
            for w in self.wallets:
                if w["coin"]==coin:
                    total+=p*float(w["amount"])
        self.price_box.config(state="disabled")
        self.total_lbl.config(text=f"TOTAL: ${total:,.2f}")
        self._update_holdings()

    def _update_holdings(self):
        self.hold_box.config(state="normal");self.hold_box.delete("1.0","end")
        if not self.wallets:
            self.hold_box.insert("end","  No holdings yet. Add coins above.\n")
        for w in self.wallets:
            p=self.prices.get(w["coin"],{}).get("usd",0)
            val=p*float(w["amount"])
            self.hold_box.insert("end",f"  {w['coin'].upper():<12} {w['amount']} coins = ${val:,.4f}\n")
        self.hold_box.config(state="disabled")

    def add_wallet(self):
        coin=self.coin_var.get();amount=self.amount_e.get().strip()
        try:float(amount)
        except:return
        self.wallets.append({"coin":coin,"amount":amount,"added":datetime.now().isoformat()})
        self.save();self._update_holdings()

    def clear(self):
        self.wallets=[];self.save();self._update_holdings()

if __name__=="__main__":
    root=tk.Tk();CryptoWallet(root);root.mainloop()
