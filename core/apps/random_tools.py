import tkinter as tk
import random,os,subprocess,hashlib,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class RandomTools:
    def __init__(self,root):
        self.root=root
        self.root.title("🎲 Random Tools")
        self.root.geometry("700x560")
        self.root.configure(bg=BG)
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🎲 RANDOM TOOLS",
                font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=5)

        nb=tk.Frame(self.root,bg=BG);nb.pack(fill="both",expand=True,padx=10,pady=5)
        tabs=tk.Frame(nb,bg=BG);tabs.pack(fill="x")
        self.pages={}
        self.active_tab=tk.StringVar(value="Dice")
        for name in ["Dice","Coin","Random #","Password","Color","Hash","Timestamp"]:
            f=tk.Frame(nb,bg=BG);self.pages[name]=f
            tk.Button(tabs,text=name,font=("Courier",8),bg=BG3,fg=NEON,
                     relief="flat",padx=8,pady=4,
                     command=lambda n=name:self.show_page(n)).pack(side="left",padx=2)
        self._build_dice();self._build_coin();self._build_random()
        self._build_password();self._build_color();self._build_hash()
        self._build_timestamp()
        self.show_page("Dice")

    def show_page(self,name):
        for p in self.pages.values():p.pack_forget()
        self.pages[name].pack(fill="both",expand=True,pady=5)

    def _lbl(self,parent,text,font_size=28,color=NEON):
        return tk.Label(parent,text=text,font=("Courier",font_size,"bold"),
                       bg=BG,fg=color)

    def _build_dice(self):
        p=self.pages["Dice"]
        self.dice_lbl=self._lbl(p,"🎲");self.dice_lbl.pack(pady=20)
        self.dice_val=self._lbl(p,"?",40,NEON);self.dice_val.pack()
        sf=tk.Frame(p,bg=BG);sf.pack(pady=10)
        for sides in [4,6,8,10,12,20,100]:
            tk.Button(sf,text=f"D{sides}",font=("Courier",9,"bold"),
                     bg=BG3,fg=NEON,relief="flat",padx=8,pady=5,
                     command=lambda s=sides:self.dice_val.config(
                         text=str(random.randint(1,s)))).pack(side="left",padx=3)

    def _build_coin(self):
        p=self.pages["Coin"]
        self.coin_lbl=self._lbl(p,"🪙",40);self.coin_lbl.pack(pady=20)
        self.coin_val=self._lbl(p,"?",24,GOLD);self.coin_val.pack()
        self.flip_count=tk.Label(p,text="Flips: 0",font=("Courier",9),bg=BG,fg=DIM)
        self.flip_count.pack(pady=5)
        self.flips=0
        tk.Button(p,text="🪙 FLIP",font=("Courier",12,"bold"),
                 bg=GOLD,fg=BG,relief="flat",padx=20,pady=8,
                 command=self.flip_coin).pack(pady=10)

    def flip_coin(self):
        self.flips+=1
        result=random.choice(["HEADS","TAILS"])
        self.coin_val.config(text=result,
                            fg=GREEN if result=="HEADS" else RED)
        self.coin_lbl.config(text="🌕" if result=="HEADS" else "🌑")
        self.flip_count.config(text=f"Flips: {self.flips}")

    def _build_random(self):
        p=self.pages["Random #"]
        tf=tk.Frame(p,bg=BG3);tf.pack(fill="x",padx=20,pady=15)
        tk.Label(tf,text="Min:",font=("Courier",10),bg=BG3,fg=DIM).pack(side="left",padx=10,pady=8)
        self.min_e=tk.Entry(tf,font=("Courier",11),bg=BG,fg=WHITE,
                           insertbackground=NEON,relief="flat",width=10)
        self.min_e.pack(side="left",ipady=6);self.min_e.insert(0,"1")
        tk.Label(tf,text="Max:",font=("Courier",10),bg=BG3,fg=DIM).pack(side="left",padx=10)
        self.max_e=tk.Entry(tf,font=("Courier",11),bg=BG,fg=WHITE,
                           insertbackground=NEON,relief="flat",width=10)
        self.max_e.pack(side="left",ipady=6);self.max_e.insert(0,"100")
        self.rand_lbl=self._lbl(p,"?",48,GREEN);self.rand_lbl.pack(pady=15)
        tk.Button(p,text="🎲 GENERATE",font=("Courier",12,"bold"),
                 bg=GREEN,fg=BG,relief="flat",padx=20,pady=8,
                 command=lambda:self.rand_lbl.config(
                     text=str(random.randint(
                         int(self.min_e.get()),int(self.max_e.get()))))).pack()

    def _build_password(self):
        p=self.pages["Password"]
        self.pass_lbl=tk.Label(p,text="Click generate",
                              font=("Courier",10),bg=BG,fg=GREEN,wraplength=400)
        self.pass_lbl.pack(pady=15)
        lf=tk.Frame(p,bg=BG);lf.pack()
        tk.Label(lf,text="Length:",font=("Courier",9),bg=BG,fg=DIM).pack(side="left")
        self.pass_len=tk.IntVar(value=16)
        tk.Scale(lf,from_=8,to=64,orient="horizontal",variable=self.pass_len,
                bg=BG,fg=NEON,troughcolor=BG3,highlightthickness=0,
                length=200).pack(side="left",padx=10)
        bf=tk.Frame(p,bg=BG);bf.pack(pady=8)
        tk.Button(bf,text="⚡ Generate",font=("Courier",10,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=12,pady=6,
                 command=self.gen_pass).pack(side="left",padx=5)
        tk.Button(bf,text="📋 Copy",font=("Courier",10),
                 bg=BG3,fg=GREEN,relief="flat",padx=10,pady=6,
                 command=lambda:[self.root.clipboard_clear(),
                                self.root.clipboard_append(
                                    self.pass_lbl.cget("text"))]).pack(side="left",padx=5)

    def gen_pass(self):
        import string,secrets
        chars=string.ascii_letters+string.digits+"!@#$%^&*()"
        pwd="".join(secrets.choice(chars) for _ in range(self.pass_len.get()))
        self.pass_lbl.config(text=pwd)

    def _build_color(self):
        p=self.pages["Color"]
        self.color_canvas=tk.Canvas(p,width=200,height=100,
                                   bg=BG,highlightthickness=2,
                                   highlightbackground=PURPLE)
        self.color_canvas.pack(pady=15)
        self.hex_lbl=self._lbl(p,"#------",16,WHITE);self.hex_lbl.pack()
        self.rgb_lbl=tk.Label(p,text="",font=("Courier",10),bg=BG,fg=DIM)
        self.rgb_lbl.pack(pady=3)
        tk.Button(p,text="🎨 Random Color",font=("Courier",11,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=7,
                 command=self.rand_color).pack(pady=10)
        tk.Button(p,text="📋 Copy HEX",font=("Courier",9),
                 bg=BG3,fg=NEON,relief="flat",padx=10,pady=5,
                 command=lambda:[self.root.clipboard_clear(),
                                self.root.clipboard_append(
                                    self.hex_lbl.cget("text"))]).pack()

    def rand_color(self):
        r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
        hex_col=f"#{r:02X}{g:02X}{b:02X}"
        self.color_canvas.config(bg=hex_col)
        self.hex_lbl.config(text=hex_col)
        self.rgb_lbl.config(text=f"RGB({r}, {g}, {b})")

    def _build_hash(self):
        p=self.pages["Hash"]
        tk.Label(p,text="Input:",font=("Courier",9),bg=BG,fg=DIM).pack(anchor="w",padx=20,pady=(15,3))
        self.hash_inp=tk.Entry(p,font=("Courier",10),bg=BG3,fg=WHITE,
                              insertbackground=NEON,relief="flat")
        self.hash_inp.pack(fill="x",padx=20,ipady=6)
        hf=tk.Frame(p,bg=BG);hf.pack(pady=8)
        for alg in ["MD5","SHA1","SHA256","SHA512"]:
            tk.Button(hf,text=alg,font=("Courier",9),bg=BG3,fg=NEON,
                     relief="flat",padx=8,pady=5,
                     command=lambda a=alg:self.make_hash(a)).pack(side="left",padx=3)
        self.hash_out=tk.Text(p,height=4,bg=BG3,fg=GREEN,
                             font=("Courier",8),relief="flat",state="disabled",wrap="word")
        self.hash_out.pack(fill="x",padx=20,pady=5)

    def make_hash(self,alg):
        text=self.hash_inp.get()
        h=hashlib.new(alg.lower().replace("sha","sha"),text.encode()).hexdigest()
        self.hash_out.config(state="normal")
        self.hash_out.delete("1.0","end")
        self.hash_out.insert("end",f"{alg}:\n{h}")
        self.hash_out.config(state="disabled")
        self.root.clipboard_clear();self.root.clipboard_append(h)

    def _build_timestamp(self):
        p=self.pages["Timestamp"]
        now=datetime.now()
        self.ts_lbl=self._lbl(p,str(int(time.time())),20,GREEN);self.ts_lbl.pack(pady=15)
        tk.Label(p,text="Unix Timestamp",font=("Courier",9),bg=BG,fg=DIM).pack()
        info=[
            ("ISO Format",now.isoformat()),
            ("UTC",now.strftime("%Y-%m-%d %H:%M:%S UTC")),
            ("Date",now.strftime("%A, %B %d %Y")),
            ("Time",now.strftime("%I:%M:%S %p")),
            ("Week",f"Week {now.strftime('%W')} of {now.year}"),
            ("Day of Year",now.strftime("Day %j of %Y")),
        ]
        if_=tk.Frame(p,bg=BG3);if_.pack(fill="x",padx=20,pady=10)
        for label,val in info:
            f=tk.Frame(if_,bg=BG3);f.pack(fill="x",padx=8,pady=2)
            tk.Label(f,text=label+":",font=("Courier",8),bg=BG3,
                    fg=DIM,width=14,anchor="w").pack(side="left")
            tk.Label(f,text=val,font=("Courier",8,"bold"),
                    bg=BG3,fg=WHITE).pack(side="left")
        tk.Button(p,text="🔄 Refresh",font=("Courier",9),
                 bg=BG3,fg=NEON,relief="flat",padx=10,pady=4,
                 command=lambda:[self.ts_lbl.config(text=str(int(time.time()))),
                                self._build_timestamp()]).pack(pady=8)

if __name__=="__main__":
    root=tk.Tk();RandomTools(root);root.mainloop()
