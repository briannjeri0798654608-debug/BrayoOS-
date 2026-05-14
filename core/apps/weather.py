import tkinter as tk,httpx,threading
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A";GOLD="#FFD700"
class Weather:
    def __init__(self,r):
        r.title("Weather");r.geometry("420x380");r.configure(bg=BG)
        tk.Label(r,text="◈ WEATHER",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        sf=tk.Frame(r,bg=BG);sf.pack(fill="x",padx=15,pady=8)
        tk.Label(sf,text="City:",font=("Courier",10),bg=BG,fg=PURPLE).pack(side="left")
        self.city=tk.Entry(sf,font=("Courier",11),bg=BG3,fg=WHITE,insertbackground=NEON,relief="flat")
        self.city.pack(side="left",fill="x",expand=True,ipady=6,padx=5)
        self.city.insert(0,"Nairobi")
        self.city.bind("<Return>",lambda e:self.fetch())
        tk.Button(sf,text="GET ▶",font=("Courier",9,"bold"),bg=PURPLE,fg=WHITE,
            relief="flat",padx=10,command=self.fetch).pack(side="right")
        self.out=tk.Text(r,bg=BG3,fg=WHITE,font=("Courier",10),relief="flat",state="disabled",height=12)
        self.out.pack(fill="both",expand=True,padx=15,pady=5)
        self.fetch()
    def log(self,msg):
        self.out.config(state="normal");self.out.insert("end",f"{msg}\n");self.out.see("end");self.out.config(state="disabled")
    def fetch(self):
        c=self.city.get().strip()
        self.out.config(state="normal");self.out.delete("1.0","end");self.out.config(state="disabled")
        threading.Thread(target=self._fetch,args=(c,),daemon=True).start()
    def _fetch(self,city):
        try:
            r=httpx.get(f"https://wttr.in/{city}?format=j1",timeout=8)
            d=r.json()["current_condition"][0]
            for info in [f"City: {city}",f"Temp: {d['temp_C']}°C",f"Feels: {d['FeelsLikeC']}°C",
                f"Humidity: {d['humidity']}%",f"Wind: {d['windspeedKmph']}km/h",
                f"Condition: {d['weatherDesc'][0]['value']}"]:
                self.log(f"  {info}")
        except Exception as e:self.log(f"Error: {e}")
if __name__=="__main__":
    r=tk.Tk();Weather(r);r.mainloop()
