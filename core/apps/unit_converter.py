import tkinter as tk

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

UNITS={
    "Length":{"m":1,"km":1000,"cm":0.01,"mm":0.001,
              "ft":0.3048,"in":0.0254,"mi":1609.34,"yd":0.9144},
    "Weight":{"kg":1,"g":0.001,"mg":0.000001,
              "lb":0.453592,"oz":0.0283495,"ton":1000},
    "Temperature":{"C":"C","F":"F","K":"K"},
    "Speed":{"m/s":1,"km/h":0.277778,"mph":0.44704,"knot":0.514444},
    "Area":{"m2":1,"km2":1e6,"cm2":0.0001,
            "ft2":0.092903,"acre":4046.86,"ha":10000},
    "Data":{"B":1,"KB":1024,"MB":1048576,"GB":1073741824,"TB":1099511627776},
}

class UnitConverter:
    def __init__(self,root):
        self.root=root
        self.root.title("📐 Unit Converter")
        self.root.geometry("560x480")
        self.root.configure(bg=BG)
        self.category=tk.StringVar(value="Length")
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="📐 UNIT CONVERTER",
                font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=5)

        # Category
        cf=tk.Frame(self.root,bg=BG);cf.pack(fill="x",padx=15,pady=5)
        tk.Label(cf,text="Category:",font=("Courier",9),
                bg=BG,fg=DIM).pack(side="left",padx=5)
        for cat in UNITS:
            tk.Radiobutton(cf,text=cat,variable=self.category,value=cat,
                          bg=BG,fg=NEON,selectcolor=PURPLE,
                          activebackground=BG,font=("Courier",8),
                          command=self.update_units).pack(side="left",padx=5)

        # Input
        inf=tk.Frame(self.root,bg=BG3);inf.pack(fill="x",padx=15,pady=8)
        tk.Label(inf,text="Value:",font=("Courier",10),
                bg=BG3,fg=DIM).pack(side="left",padx=10,pady=8)
        self.inp=tk.Entry(inf,font=("Courier",14,"bold"),bg=BG,
                         fg=GOLD,insertbackground=NEON,relief="flat",width=15)
        self.inp.pack(side="left",ipady=8)
        self.inp.insert(0,"1")
        self.inp.bind("<KeyRelease>",lambda e:self.convert())

        self.from_var=tk.StringVar(value="m")
        self.from_menu=tk.OptionMenu(inf,self.from_var,"m")
        self.from_menu.pack(side="left",padx=10)
        tk.Label(inf,text="→",font=("Courier",14),
                bg=BG3,fg=PURPLE).pack(side="left")
        self.to_var=tk.StringVar(value="km")
        self.to_menu=tk.OptionMenu(inf,self.to_var,"km")
        self.to_menu.pack(side="left",padx=5)
        self.from_var.trace("w",lambda *a:self.convert())
        self.to_var.trace("w",lambda *a:self.convert())

        # Result
        self.result=tk.Label(self.root,text="",
                            font=("Courier",20,"bold"),bg=BG,fg=GREEN)
        self.result.pack(pady=15)

        # All conversions grid
        tk.Label(self.root,text="◈ ALL CONVERSIONS",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.grid_box=tk.Text(self.root,bg=BG3,fg=WHITE,
                             font=("Courier",9),relief="flat",
                             state="disabled")
        self.grid_box.pack(fill="both",expand=True,padx=15,pady=5)
        self.grid_box.tag_config("h",foreground=NEON)

        tk.Label(self.root,text="BrayoOS Unit Converter v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)
        self.update_units()

    def update_units(self):
        cat=self.category.get()
        units=list(UNITS[cat].keys())
        self.from_var.set(units[0])
        self.to_var.set(units[1] if len(units)>1 else units[0])
        for menu,var in [(self.from_menu,self.from_var),(self.to_menu,self.to_var)]:
            menu["menu"].delete(0,"end")
            for u in units:
                menu["menu"].add_command(label=u,
                    command=tk._setit(var,u))
        self.convert()

    def convert(self):
        try:
            val=float(self.inp.get())
            cat=self.category.get()
            frm=self.from_var.get()
            to=self.to_var.get()
            units=UNITS[cat]
            if cat=="Temperature":
                result=self.convert_temp(val,frm,to)
            else:
                base=val*units[frm]
                result=base/units[to]
            self.result.config(text=f"{val} {frm} = {result:.6g} {to}")
            self.show_all(val,frm,units,cat)
        except:pass

    def convert_temp(self,val,frm,to):
        if frm=="C":
            c=val
        elif frm=="F":
            c=(val-32)*5/9
        else:
            c=val-273.15
        if to=="C":return round(c,4)
        elif to=="F":return round(c*9/5+32,4)
        else:return round(c+273.15,4)

    def show_all(self,val,frm,units,cat):
        self.grid_box.config(state="normal")
        self.grid_box.delete("1.0","end")
        self.grid_box.insert("end",f"  {val} {frm} equals:\n","h")
        for unit,factor in units.items():
            if unit!=frm:
                try:
                    if cat=="Temperature":
                        r=self.convert_temp(val,frm,unit)
                    else:
                        base=val*units[frm]
                        r=base/factor
                    self.grid_box.insert("end",f"  {r:.6g} {unit}\n")
                except:pass
        self.grid_box.config(state="disabled")

if __name__=="__main__":
    root=tk.Tk();UnitConverter(root);root.mainloop()
