import tkinter as tk
import threading,httpx,os
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class CurrencyConverter:
    def __init__(self,root):
        self.root=root
        self.root.title("💱 Currency Converter")
        self.root.geometry("580x500")
        self.root.configure(bg=BG)
        self.rates={}
        self.build_ui()
        self.fetch_rates()

    def build_ui(self):
        tk.Label(self.root,text="💱 CURRENCY CONVERTER",
                font=("Courier",15,"bold"),bg=BG,fg=GOLD).pack(pady=8)
        tk.Label(self.root,text="Live exchange rates",
                font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=GOLD,height=2).pack(fill="x",pady=6)

        # Converter
        cf=tk.Frame(self.root,bg=BG3);cf.pack(fill="x",padx=15,pady=8)
        row1=tk.Frame(cf,bg=BG3);row1.pack(fill="x",padx=10,pady=8)
        tk.Label(row1,text="Amount:",font=("Courier",10),
                bg=BG3,fg=DIM,width=10,anchor="w").pack(side="left")
        self.amount_e=tk.Entry(row1,font=("Courier",13,"bold"),
                              bg=BG,fg=GOLD,insertbackground=NEON,
                              relief="flat",width=12)
        self.amount_e.pack(side="left",ipady=8)
        self.amount_e.insert(0,"1000")
        self.amount_e.bind("<KeyRelease>",lambda e:self.convert())

        row2=tk.Frame(cf,bg=BG3);row2.pack(fill="x",padx=10,pady=5)
        tk.Label(row2,text="From:",font=("Courier",10),
                bg=BG3,fg=DIM,width=10,anchor="w").pack(side="left")
        self.from_var=tk.StringVar(value="KES")
        currencies=["KES","USD","EUR","GBP","NGN","TZS","UGX","ZAR","INR","CNY","JPY","AED"]
        tk.OptionMenu(row2,self.from_var,*currencies).pack(side="left",padx=5)
        self.from_var.trace("w",lambda *a:self.convert())

        row3=tk.Frame(cf,bg=BG3);row3.pack(fill="x",padx=10,pady=5)
        tk.Label(row3,text="To:",font=("Courier",10),
                bg=BG3,fg=DIM,width=10,anchor="w").pack(side="left")
        self.to_var=tk.StringVar(value="USD")
        tk.OptionMenu(row3,self.to_var,*currencies).pack(side="left",padx=5)
        self.to_var.trace("w",lambda *a:self.convert())

        # Result
        self.result=tk.Label(self.root,text="",
                            font=("Courier",22,"bold"),bg=BG,fg=GREEN)
        self.result.pack(pady=10)
        self.rate_lbl=tk.Label(self.root,text="",
                              font=("Courier",9),bg=BG,fg=DIM)
        self.rate_lbl.pack()

        # Quick conversions
        tk.Label(self.root,text="◈ COMMON RATES (vs KES)",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(10,3))
        self.rates_box=tk.Text(self.root,height=8,bg=BG3,fg=WHITE,
                              font=("Courier",9),relief="flat",state="disabled")
        self.rates_box.pack(fill="both",expand=True,padx=15,pady=5)
        self.rates_box.tag_config("g",foreground=GREEN)
        self.rates_box.tag_config("y",foreground=GOLD)

        self.status=tk.Label(self.root,text="Fetching rates...",
                            font=("Courier",8),bg=BG,fg=DIM)
        self.status.pack()
        tk.Label(self.root,text="BrayoOS Currency v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def fetch_rates(self):
        threading.Thread(target=self._fetch,daemon=True).start()

    def _fetch(self):
        try:
            r=httpx.get(
                "https://api.exchangerate-api.com/v4/latest/KES",
                timeout=8)
            if r.status_code==200:
                self.rates=r.json().get("rates",{})
                self.root.after(0,self.show_rates)
                self.root.after(0,self.convert)
                self.root.after(0,self.status.config,
                               {"text":f"✅ Rates updated {datetime.now().strftime('%H:%M')}",
                                "fg":GREEN})
        except:
            # Fallback rates
            self.rates={"USD":0.0077,"EUR":0.0071,"GBP":0.0061,
                       "NGN":10.5,"TZS":19.8,"UGX":28.5,
                       "ZAR":0.14,"INR":0.64,"CNY":0.056}
            self.root.after(0,self.show_rates)
            self.root.after(0,self.convert)
            self.root.after(0,self.status.config,
                           {"text":"⚠️ Offline rates","fg":GOLD})

    def show_rates(self):
        self.rates_box.config(state="normal")
        self.rates_box.delete("1.0","end")
        pairs=[("USD","🇺🇸"),("EUR","🇪🇺"),("GBP","🇬🇧"),
               ("NGN","🇳🇬"),("TZS","🇹🇿"),("ZAR","🇿🇦"),
               ("INR","🇮🇳"),("CNY","🇨🇳")]
        for code,flag in pairs:
            rate=self.rates.get(code,0)
            if rate:
                kes_per=1/rate if rate<1 else rate
                self.rates_box.insert("end",
                    f"  {flag} {code}: 1 KES = {rate:.4f} | 1 {code} = {1/rate:.1f} KES\n",
                    "g" if code=="USD" else "y")
        self.rates_box.config(state="disabled")

    def convert(self):
        try:
            amount=float(self.amount_e.get())
            frm=self.from_var.get()
            to=self.to_var.get()
            if not self.rates:return
            if frm=="KES":
                result=amount*self.rates.get(to,1)
            else:
                in_kes=amount/self.rates.get(frm,1)
                result=in_kes*self.rates.get(to,1)
            self.result.config(text=f"{amount:,.0f} {frm} = {result:,.2f} {to}")
            rate=result/amount if amount>0 else 0
            self.rate_lbl.config(text=f"Rate: 1 {frm} = {rate:.4f} {to}")
        except:pass

if __name__=="__main__":
    root=tk.Tk();CurrencyConverter(root);root.mainloop()
