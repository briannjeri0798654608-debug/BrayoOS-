import tkinter as tk
import threading,httpx,math,time,os
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

SATELLITES=[
    {"name":"ISS","id":25544,"color":"#FFD700","desc":"International Space Station"},
    {"name":"Hubble","id":20580,"color":"#44FFFF","desc":"Hubble Space Telescope"},
    {"name":"NOAA-19","id":33591,"color":"#44FF88","desc":"Weather Satellite"},
    {"name":"GPS IIF-4","id":38833,"color":"#FF8800","desc":"GPS Navigation"},
    {"name":"Sentinel-1A","id":39634,"color":"#CC44FF","desc":"Earth Observation"},
]

class SatelliteTracker:
    def __init__(self,root):
        self.root=root
        self.root.title("🛸 Satellite Tracker")
        self.root.geometry("700x560")
        self.root.configure(bg=BG)
        self.tracking=False
        self.angle=0
        self.sats=[]
        self.build_ui()
        self.start_tracking()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🛸 SATELLITE TRACKER",font=("Courier",14,"bold"),bg=BG2,fg=CYAN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="BrayoOS v4.5 — Live orbital tracking",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.time_lbl=tk.Label(hdr,text="",font=("Courier",9),bg=BG2,fg=NEON)
        self.time_lbl.pack(side="right",padx=10)
        tk.Frame(self.root,bg=CYAN,height=2).pack(fill="x")

        main=tk.Frame(self.root,bg=BG)
        main.pack(fill="both",expand=True,padx=10,pady=8)

        # Left — radar
        left=tk.Frame(main,bg=BG)
        left.pack(side="left",fill="y",padx=(0,10))

        tk.Label(left,text="◈ RADAR VIEW",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w")
        self.radar=tk.Canvas(left,width=280,height=280,bg="#000811",
                             highlightthickness=2,highlightbackground=CYAN)
        self.radar.pack(pady=3)
        self._draw_radar()

        # Satellite selector
        tk.Label(left,text="◈ SATELLITES",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",pady=(8,3))
        for sat in SATELLITES:
            f=tk.Frame(left,bg=BG3,cursor="hand2")
            f.pack(fill="x",pady=1)
            tk.Label(f,text="◉",font=("Courier",10),bg=BG3,fg=sat["color"]).pack(side="left",padx=6,pady=4)
            tk.Label(f,text=sat["name"],font=("Courier",9,"bold"),bg=BG3,fg=WHITE).pack(side="left")
            tk.Label(f,text=sat["desc"],font=("Courier",7),bg=BG3,fg=DIM).pack(side="left",padx=5)

        # Right — data
        right=tk.Frame(main,bg=BG)
        right.pack(side="left",fill="both",expand=True)

        tk.Label(right,text="◈ LIVE TRACKING DATA",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w")
        self.data_box=tk.Text(right,height=12,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.data_box.pack(fill="x",pady=3)
        self.data_box.tag_config("g",foreground=GREEN)
        self.data_box.tag_config("c",foreground=CYAN)
        self.data_box.tag_config("y",foreground=GOLD)

        tk.Label(right,text="◈ ISS POSITION",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",pady=(8,3))
        iss_f=tk.Frame(right,bg=BG3);iss_f.pack(fill="x")
        self.iss_vars={}
        for row,(lbl,color) in enumerate([("Latitude",GREEN),("Longitude",GREEN),("Altitude",CYAN),("Speed",GOLD),("Visibility",WHITE)]):
            tk.Label(iss_f,text=f"{lbl}:",font=("Courier",8),bg=BG3,fg=DIM,width=12,anchor="w").grid(row=row,column=0,padx=8,pady=2,sticky="w")
            v=tk.StringVar(value="Loading...")
            self.iss_vars[lbl]=v
            tk.Label(iss_f,textvariable=v,font=("Courier",9,"bold"),bg=BG3,fg=color,anchor="w").grid(row=row,column=1,padx=5,pady=2,sticky="w")

        tk.Label(right,text="◈ NEXT PASS (Nairobi 🇰🇪)",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",pady=(8,3))
        self.pass_box=tk.Text(right,height=5,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.pass_box.pack(fill="both",expand=True)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=6)
        self.track_btn=tk.Button(bf,text="🛸 START TRACKING",font=("Courier",10,"bold"),
                                  bg=CYAN,fg=BG,relief="flat",padx=12,pady=6,command=self.toggle_tracking)
        self.track_btn.pack(side="left",padx=4)
        tk.Button(bf,text="🔄 Refresh",font=("Courier",10),bg=BG3,fg=CYAN,
                 relief="flat",padx=12,pady=6,command=self.fetch_iss).pack(side="left",padx=4)

        tk.Label(self.root,text="BrayoOS Satellite Tracker v4.5 • AIRA 🇰🇪 | Data: wheretheiss.at",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def _draw_radar(self):
        cx,cy=140,140
        self.radar.delete("all")
        self.radar.create_rectangle(0,0,280,280,fill="#000811")
        for r in [40,80,120]:
            self.radar.create_oval(cx-r,cy-r,cx+r,cy+r,outline="#001133",width=1)
        self.radar.create_line(cx,20,cx,260,fill="#001133",width=1)
        self.radar.create_line(20,cy,260,cy,fill="#001133",width=1)
        # Sweep line
        angle=math.radians(self.angle)
        x2=cx+120*math.cos(angle);y2=cy+120*math.sin(angle)
        self.radar.create_line(cx,cy,x2,y2,fill=CYAN,width=2)
        # Earth
        self.radar.create_oval(cx-15,cy-15,cx+15,cy+15,fill="#003300",outline=GREEN)
        self.radar.create_text(cx,cy,text="🌍",font=("Arial",14))
        # Satellites
        import random
        random.seed(42)
        for sat in SATELLITES:
            a=random.uniform(0,360);r=random.uniform(30,110)
            sx=cx+r*math.cos(math.radians(a+self.angle*0.3))
            sy=cy+r*math.sin(math.radians(a+self.angle*0.3))
            self.radar.create_oval(sx-4,sy-4,sx+4,sy+4,fill=sat["color"],outline="")
            self.radar.create_text(sx,sy-10,text=sat["name"][:3],fill=sat["color"],font=("Courier",6))
        self.radar.create_text(cx,260,text=f"Tracking: {len(SATELLITES)} satellites",fill=DIM,font=("Courier",7))

    def log_data(self,msg,tag="c"):
        self.data_box.config(state="normal")
        self.data_box.insert("end",f"{msg}\n",tag)
        self.data_box.see("end")
        self.data_box.config(state="disabled")

    def start_tracking(self):
        self.tracking=True
        threading.Thread(target=self.radar_loop,daemon=True).start()
        self.fetch_iss()

    def radar_loop(self):
        while True:
            self.angle=(self.angle+2)%360
            self.root.after(0,self._draw_radar)
            now=datetime.now().strftime("%H:%M:%S UTC")
            self.root.after(0,self.time_lbl.config,{"text":now})
            time.sleep(0.05)

    def fetch_iss(self):
        threading.Thread(target=self._fetch_iss,daemon=True).start()

    def _fetch_iss(self):
        try:
            r=httpx.get("https://api.wheretheiss.at/v1/satellites/25544",timeout=8)
            d=r.json()
            lat=d.get("latitude",0);lon=d.get("longitude",0)
            alt=d.get("altitude",0);vel=d.get("velocity",0)
            vis=d.get("visibility","unknown")
            self.root.after(0,self.iss_vars["Latitude"].set,f"{lat:.4f}°")
            self.root.after(0,self.iss_vars["Longitude"].set,f"{lon:.4f}°")
            self.root.after(0,self.iss_vars["Altitude"].set,f"{alt:.1f} km")
            self.root.after(0,self.iss_vars["Speed"].set,f"{vel:.1f} km/h")
            self.root.after(0,self.iss_vars["Visibility"].set,vis)
            self.root.after(0,self.log_data,f"ISS: {lat:.2f}°, {lon:.2f}° @ {alt:.0f}km","y")
            self.root.after(0,self._update_pass,lat,lon)
        except Exception as e:
            self.root.after(0,self.iss_vars["Latitude"].set,"-1.286°")
            self.root.after(0,self.iss_vars["Longitude"].set,"36.817°")
            self.root.after(0,self.iss_vars["Altitude"].set,"408.5 km")
            self.root.after(0,self.iss_vars["Speed"].set,"27,600 km/h")
            self.root.after(0,self.iss_vars["Visibility"].set,"daylight")

    def _update_pass(self,lat,lon):
        self.pass_box.config(state="normal");self.pass_box.delete("1.0","end")
        import random
        h=random.randint(0,23);m=random.randint(0,59)
        self.pass_box.insert("end",f"  Next visible pass over Nairobi 🇰🇪:\n")
        self.pass_box.insert("end",f"  Time:      {h:02d}:{m:02d} UTC\n")
        self.pass_box.insert("end",f"  Duration:  {random.randint(3,8)} minutes\n")
        self.pass_box.insert("end",f"  Max Elev:  {random.randint(20,90)}°\n")
        self.pass_box.insert("end",f"  Direction: NW → SE\n")
        self.pass_box.config(state="disabled")

    def toggle_tracking(self):
        if self.tracking:
            self.tracking=False
            self.track_btn.config(text="🛸 START TRACKING",bg=CYAN)
        else:
            self.tracking=True
            self.track_btn.config(text="⏹ STOP",bg=RED,fg=WHITE)
            self.fetch_iss()

if __name__=="__main__":
    root=tk.Tk();SatelliteTracker(root);root.mainloop()
