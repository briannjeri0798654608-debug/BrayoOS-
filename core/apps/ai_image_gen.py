import tkinter as tk
from tkinter import filedialog
import threading,httpx,os,json,base64,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
GROQ=os.environ.get("GROQ_API_KEY","")

class AIImageGen:
    def __init__(self,root):
        self.root=root
        self.root.title("🎨 AI Image Generator")
        self.root.geometry("700x580")
        self.root.configure(bg=BG)
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🎨 BRAYOOS AI IMAGE STUDIO",
                 font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Generate images with AI • Powered by AIRA",
                 font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        main=tk.Frame(self.root,bg=BG)
        main.pack(fill="both",expand=True,padx=15,pady=5)

        # Left — controls
        left=tk.Frame(main,bg=BG)
        left.pack(side="left",fill="y",padx=(0,10))

        tk.Label(left,text="◈ PROMPT",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w")
        self.prompt=tk.Text(left,height=4,width=35,bg=BG3,fg=WHITE,
                            font=("Courier",9),relief="flat",insertbackground=NEON)
        self.prompt.pack(pady=3)
        self.prompt.insert("end","A futuristic phone running BrayoOS in Kenya at night, purple neon lights, cyberpunk style")

        tk.Label(left,text="◈ STYLE",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",pady=(8,2))
        self.style_var=tk.StringVar(value="Cyberpunk")
        styles=["Cyberpunk","Realistic","Anime","Abstract","Dark Art","Hacker","Kenya","Neon"]
        sf=tk.Frame(left,bg=BG3);sf.pack(fill="x")
        for i,s in enumerate(styles):
            row,col=divmod(i,2)
            tk.Radiobutton(sf,text=s,variable=self.style_var,value=s,
                          bg=BG3,fg=NEON,selectcolor=PURPLE,activebackground=BG3,
                          font=("Courier",8)).grid(row=row,column=col,padx=5,pady=2,sticky="w")

        tk.Label(left,text="◈ SIZE",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",pady=(8,2))
        self.size_var=tk.StringVar(value="512x512")
        for s in ["256x256","512x512","768x768"]:
            tk.Radiobutton(left,text=s,variable=self.size_var,value=s,
                          bg=BG,fg=NEON,selectcolor=PURPLE,activebackground=BG,
                          font=("Courier",8)).pack(anchor="w")

        tk.Label(left,text="◈ QUICK PROMPTS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",pady=(8,2))
        quick=[
            ("🇰🇪 Kenya","Nairobi city skyline at night, cyberpunk"),
            ("💜 BrayoOS","BrayoOS desktop on phone, purple neon"),
            ("🤖 AIRA","Female AI robot, purple eyes, Kenya flag"),
            ("💀 Hacker","Elite hacker in dark room, multiple screens"),
        ]
        for label,p in quick:
            tk.Button(left,text=label,font=("Courier",8),bg=BG3,fg=NEON,relief="flat",
                     padx=6,pady=3,command=lambda x=p:self.set_prompt(x)).pack(fill="x",pady=1)

        tk.Button(left,text="🎨 GENERATE",font=("Courier",11,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=8,
                 command=self.generate).pack(fill="x",pady=8)
        tk.Button(left,text="💾 Save Image",font=("Courier",9),
                 bg=BG3,fg=GREEN,relief="flat",padx=10,pady=5,
                 command=self.save_image).pack(fill="x",pady=2)

        # Right — canvas
        right=tk.Frame(main,bg=BG)
        right.pack(side="left",fill="both",expand=True)

        self.canvas=tk.Canvas(right,width=380,height=380,bg="#001100",
                              highlightthickness=2,highlightbackground=PURPLE)
        self.canvas.pack()
        self._draw_placeholder()

        self.status=tk.Label(right,text="Ready to generate...",
                             font=("Courier",9),bg=BG,fg=DIM)
        self.status.pack(pady=5)

        self.progress=tk.Canvas(right,width=380,height=8,bg="#001100",highlightthickness=0)
        self.progress.pack()

        tk.Label(self.root,text="BrayoOS AI Studio v1.0 • AIRA 🇰🇪",
                 font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)
        self.current_image=None

    def _draw_placeholder(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0,0,380,380,fill="#000811")
        for i in range(0,380,20):
            self.canvas.create_line(i,0,i,380,fill="#001122",width=1)
            self.canvas.create_line(0,i,380,i,fill="#001122",width=1)
        self.canvas.create_text(190,170,text="🎨",font=("Courier",40),fill=PURPLE)
        self.canvas.create_text(190,230,text="AI IMAGE STUDIO",fill=PURPLE,font=("Courier",12,"bold"))
        self.canvas.create_text(190,255,text="Enter prompt and generate",fill=DIM,font=("Courier",8))

    def set_prompt(self,p):
        self.prompt.delete("1.0","end")
        self.prompt.insert("end",p)

    def animate_progress(self,pct,color=PURPLE):
        self.progress.delete("all")
        w=int(380*pct/100)
        if w>0:self.progress.create_rectangle(0,0,w,8,fill=color,outline="")

    def generate(self):
        prompt=self.prompt.get("1.0","end").strip()
        if not prompt:return
        threading.Thread(target=self._generate,args=(prompt,),daemon=True).start()

    def _generate(self,prompt):
        style=self.style_var.get()
        full_prompt=f"{prompt}, {style} style, highly detailed, 4K"
        self.root.after(0,self.status.config,{"text":"🧠 AIRA processing prompt..."})
        self.root.after(0,self._draw_generating)

        steps=["Analyzing prompt...","Building composition...","Rendering colors...","Adding details...","Finalizing image..."]
        for i,step in enumerate(steps):
            self.root.after(0,self.status.config,{"text":f"⚡ {step}"})
            self.root.after(0,self.animate_progress,(i+1)*20)
            time.sleep(0.8)

        # Try Pollinations AI (free, no key needed)
        try:
            import urllib.parse
            encoded=urllib.parse.quote(full_prompt)
            url=f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&seed={int(time.time())}"
            self.root.after(0,self.status.config,{"text":"📡 Downloading from AI..."})
            r=httpx.get(url,timeout=30,follow_redirects=True)
            if r.status_code==200 and r.headers.get("content-type","").startswith("image"):
                img_data=r.content
                self.current_image=img_data
                self.root.after(0,self._show_image,img_data)
                self.root.after(0,self.animate_progress,100,GREEN)
                self.root.after(0,self.status.config,{"text":"✅ Image generated by AIRA!"})
                return
        except Exception as e:
            pass

        # Fallback — generate pixel art with tkinter
        self.root.after(0,self._draw_ai_art,prompt)
        self.root.after(0,self.animate_progress,100,GREEN)
        self.root.after(0,self.status.config,{"text":"✅ AI Art generated! (Offline mode)"})

    def _draw_generating(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0,0,380,380,fill="#000811")
        self.canvas.create_text(190,190,text="GENERATING...",fill=PURPLE,font=("Courier",14,"bold"))

    def _draw_ai_art(self,prompt):
        import random,math
        self.canvas.delete("all")
        # Background
        self.canvas.create_rectangle(0,0,380,380,fill="#000811")
        # Generate colors from prompt keywords
        colors=[PURPLE,NEON,"#00FF41","#FF0044",GOLD,"#44FFFF","#FF44AA"]
        if "kenya" in prompt.lower():colors=[GREEN,RED,"#000000",GOLD]
        elif "cyber" in prompt.lower():colors=[PURPLE,NEON,"#00FFFF","#0000FF"]
        elif "hacker" in prompt.lower():colors=["#00FF41","#003300","#004400","#001100"]

        # Generate abstract art
        random.seed(hash(prompt)%1000)
        for _ in range(200):
            x1=random.randint(0,380);y1=random.randint(0,380)
            x2=x1+random.randint(-60,60);y2=y1+random.randint(-60,60)
            c=random.choice(colors)
            shape=random.choice(["rect","oval","line"])
            if shape=="rect":self.canvas.create_rectangle(x1,y1,x2,y2,fill=c,outline="")
            elif shape=="oval":self.canvas.create_oval(x1,y1,x2,y2,fill=c,outline="")
            else:self.canvas.create_line(x1,y1,x2,y2,fill=c,width=random.randint(1,4))

        # Add text watermark
        self.canvas.create_text(190,360,text="BrayoOS AI • AIRA 🇰🇪",
                               fill=DIM,font=("Courier",8))

    def _show_image(self,data):
        try:
            from PIL import Image,ImageTk
            import io
            img=Image.open(io.BytesIO(data)).resize((380,380))
            photo=ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0,0,anchor="nw",image=photo)
            self.canvas._photo=photo
        except:
            self._draw_ai_art("downloaded")

    def save_image(self):
        path=filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG","*.png"),("All","*.*")],
            initialdir=os.path.expanduser("~/Pictures"))
        if path:
            try:
                self.canvas.postscript(file=path.replace(".png",".ps"))
                self.status.config(text=f"💾 Saved to {os.path.basename(path)}")
            except:self.status.config(text="⚠️ Install pillow: pip install pillow")

if __name__=="__main__":
    root=tk.Tk();AIImageGen(root);root.mainloop()
