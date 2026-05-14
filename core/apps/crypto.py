import tkinter as tk,httpx,threading
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GOLD="#FFD700";GREEN="#44FF88";RED="#FF0044"
class Crypto:
    def __init__(self,r):
        r.title("Crypto");r.geometry("480x420");r.configure(bg=BG)
        tk.Label(r,text="◈ CRYPTO TRACKER",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        self.out=tk.Text(r,bg=BG3,fg=WHITE,font=("Courier",10),relief="flat",state="disabled",height=16)
        self.out.pack(fill="both",expand=True,padx=15,pady=8)
        self.out.tag_config("g",foreground=GREEN);self.out.tag_config("r",foreground=RED);self.out.tag_config("y",foreground=GOLD)
        tk.Button(r,text="🔄 Refresh",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
            relief="flat",padx=12,pady=6,command=self.fetch).pack(pady=6)
        self.fetch()
    def log(self,msg,tag="y"):
        self.out.config(state="normal");self.out.insert("end",f"{msg}\n",tag);self.out.see("end");self.out.config(state="disabled")
    def fetch(self):
        self.out.config(state="normal");self.out.delete("1.0","end");self.out.config(state="disabled")
        self.log("Fetching prices...","y")
        threading.Thread(target=self._fetch,daemon=True).start()
    def _fetch(self):
        try:
            coins="bitcoin,ethereum,solana,cardano,dogecoin"
            r=httpx.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd&include_24hr_change=true",timeout=10)
            self.log("\n◈ LIVE PRICES\n","y")
            for coin,data in r.json().items():
                p=data.get("usd",0);c=data.get("usd_24h_change",0)
                tag="g" if c>=0 else "r"
                self.log(f"  {coin.upper():<12} ${p:>10,.2f}  {'▲' if c>=0 else '▼'}{abs(c):.2f}%",tag)
        except Exception as e:self.log(f"Error: {e}","r")
if __name__=="__main__":
    r=tk.Tk();Crypto(r);r.mainloop()
