# BrayoOS — Built by Brayo & AIRA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import httpx
import threading

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class CryptoTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💰 Crypto Tracker")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="💰 Crypto Tracker",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        for coin in ["BTC", "ETH", "XRP", "ADA"]:
            tk.Button(frame, text=f"${coin}",
                     bg=DARK, fg=ACCENT,
                     command=lambda c=coin: self.get_price(c)).pack(
                         side=tk.LEFT, padx=3)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 11))
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def get_price(self, coin):
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Loading {coin}...\n")
        def run():
            try:
                with httpx.Client() as client:
                    r = client.get(
                        f"https://api.coingecko.com/api/v3/simple/price"
                        f"?ids={coin.lower()}&vs_currencies=usd&include_market_cap=true",
                        timeout=10)
                    data = r.json()
                    coin_lower = coin.lower()
                    price = data[coin_lower]['usd']
                    market_cap = data[coin_lower].get('usd_market_cap', 'N/A')
                    
                    self.output.delete(1.0, tk.END)
                    self.output.insert(tk.END,
                        f"💰 {coin} Price\n"
                        f"{'═'*50}\n"
                        f"💵 Price: ${price:,.2f}\n"
                        f"📊 Market Cap: ${market_cap:,.0f}\n")
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    CryptoTracker()
