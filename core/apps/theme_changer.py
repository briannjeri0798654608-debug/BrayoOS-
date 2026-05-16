import tkinter as tk
import json,os,subprocess
from datetime import datetime

CONFIG=os.path.expanduser("~/BrayoOS/memory/theme.json")
os.makedirs(os.path.dirname(CONFIG),exist_ok=True)

THEMES={
    "Purple Hacker":{"bg":"#080810","bg2":"#0D0D1A","bg3":"#12122A","primary":"#9D00FF","neon":"#CC44FF","accent":"#FF44FF"},
    "Red Matrix":{"bg":"#100808","bg2":"#1A0D0D","bg3":"#2A1212","primary":"#FF0044","neon":"#FF4466","accent":"#FF8800"},
    "Cyber Blue":{"bg":"#080F10","bg2":"#0D141A","bg3":"#12202A","primary":"#0044FF","neon":"#44AAFF","accent":"#00FFFF"},
    "Kenya Gold":{"bg":"#100C00","bg2":"#1A1400","bg3":"#2A2000","primary":"#B8860B","neon":"#FFD700","accent":"#00AA44"},
    "Ghost White":{"bg":"#0A0A0F","bg2":"#111118","bg3":"#1A1A25","primary":"#AAAAFF","neon":"#FFFFFF","accent":"#CCCCFF"},
    "Blood Orange":{"bg":"#100800","bg2":"#1A0F00","bg3":"#2A1800","primary":"#FF4400","neon":"#FF8800","accent":"#FFCC00"},
}

class ThemeChanger:
    def __init__(self,root):
        self.root=root
        self.root.title("🎨 Theme Changer")
        self.root.geometry("550x480")
        self.root.configure(bg="#080810")
        self.selected=None
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🎨 BRAYOOS THEME CHANGER",
                 font=("Courier",14,"bold"),bg="#080810",fg="#CC44FF").pack(pady=10)
        tk.Frame(self.root,bg="#9D00FF",height=2).pack(fill="x")
        tk.Label(self.root,text="Select a theme and apply it to BrayoOS",
                 font=("Courier",8),bg="#080810",fg="#444466").pack(pady=5)

        # Theme grid
        gf=tk.Frame(self.root,bg="#080810")
        gf.pack(fill="both",expand=True,padx=15,pady=8)

        self.cards={}
        for i,(name,colors) in enumerate(THEMES.items()):
            row,col=divmod(i,2)
            card=tk.Frame(gf,bg=colors["bg2"],
                         highlightbackground=colors["primary"],
                         highlightthickness=2,cursor="hand2")
            card.grid(row=row,column=col,padx=6,pady=6,sticky="ew")
            gf.columnconfigure(col,weight=1)

            # Preview bar
            prev=tk.Frame(card,bg=colors["bg"],height=20)
            prev.pack(fill="x")
            tk.Frame(prev,bg=colors["primary"],width=30,height=20).pack(side="left")
            tk.Frame(prev,bg=colors["neon"],width=20,height=20).pack(side="left")
            tk.Frame(prev,bg=colors["accent"],width=15,height=20).pack(side="left")

            tk.Label(card,text=name,font=("Courier",10,"bold"),
                    bg=colors["bg2"],fg=colors["neon"]).pack(pady=(5,2),padx=8,anchor="w")
            tk.Label(card,text=f"Primary: {colors['primary']}",
                    font=("Courier",7),bg=colors["bg2"],fg=colors["primary"]).pack(padx=8,anchor="w")
            tk.Label(card,text=f"Neon: {colors['neon']}",
                    font=("Courier",7),bg=colors["bg2"],fg=colors["neon"]).pack(padx=8,anchor="w",pady=(0,6))

            card.bind("<Button-1>",lambda e,n=name:self.select(n))
            for w in card.winfo_children():
                w.bind("<Button-1>",lambda e,n=name:self.select(n))
            self.cards[name]=card

        # Apply button
        self.apply_btn=tk.Button(self.root,text="✨ APPLY THEME",
                                  font=("Courier",11,"bold"),bg="#9D00FF",fg="white",
                                  relief="flat",padx=20,pady=8,command=self.apply)
        self.apply_btn.pack(pady=8)

        self.status=tk.Label(self.root,text="Select a theme above",
                              font=("Courier",9),bg="#080810",fg="#444466")
        self.status.pack()

        tk.Label(self.root,text="BrayoOS Theme Engine • AIRA 🇰🇪",
                 font=("Courier",7),bg="#080810",fg="#222244").pack(side="bottom",pady=5)

    def select(self,name):
        self.selected=name
        colors=THEMES[name]
        # Highlight selected
        for n,card in self.cards.items():
            t=THEMES[n]
            card.config(highlightbackground=t["primary"] if n!=name else "#FFFFFF",
                       highlightthickness=2 if n!=name else 3)
        self.status.config(text=f"Selected: {name}",fg=colors["neon"])
        self.apply_btn.config(bg=colors["primary"])

    def apply(self):
        if not self.selected:
            self.status.config(text="⚠️ Select a theme first!",fg="#FF0044")
            return
        colors=THEMES[self.selected]
        with open(CONFIG,"w") as f:json.dump({"theme":self.selected,"colors":colors},f,indent=2)
        self.status.config(text=f"✅ {self.selected} applied! Restart desktop to see changes.",fg="#44FF88")

        # Update desktop colors dynamically
        script=f"""
import json,os
config='{CONFIG}'
if os.path.exists(config):
    data=json.load(open(config))
    print("Theme:",data['theme'])
"""
        self.status.config(text=f"✅ Theme saved! Run: pkill -f desktop.py && DISPLAY=:1 python3 ~/BrayoOS/core/desktop.py &")

if __name__=="__main__":
    root=tk.Tk()
    ThemeChanger(root)
    root.mainloop()
