import tkinter as tk
import threading,os,httpx
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
GROQ=os.environ.get("GROQ_API_KEY","")

class CodeGenerator:
    def __init__(self,root):
        self.root=root
        self.root.title("⚡ AIRA Code Generator")
        self.root.geometry("720x580")
        self.root.configure(bg=BG)
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="⚡ AIRA CODE GENERATOR",
                font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Describe any app — AIRA builds it",
                font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        tk.Label(self.root,text="◈ DESCRIBE YOUR APP",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.desc=tk.Text(self.root,height=3,bg=BG3,fg=WHITE,
                         font=("Courier",10),relief="flat",insertbackground=NEON)
        self.desc.pack(fill="x",padx=15,pady=4)
        self.desc.insert("end","A password strength checker with a color bar")

        qf=tk.Frame(self.root,bg=BG);qf.pack(fill="x",padx=15,pady=3)
        for q in ["Calculator","Clock","To-do List","Weather","Quiz App","File Viewer"]:
            tk.Button(qf,text=q,font=("Courier",7),bg=BG3,fg=NEON,
                     relief="flat",padx=5,pady=2,
                     command=lambda x=q:self.quick(x)).pack(side="left",padx=2)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=5)
        tk.Button(bf,text="⚡ GENERATE",font=("Courier",11,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=7,
                 command=self.generate).pack(side="left",padx=5)
        tk.Button(bf,text="💾 SAVE APP",font=("Courier",10),
                 bg=BG3,fg=GREEN,relief="flat",padx=12,pady=7,
                 command=self.save_app).pack(side="left",padx=5)
        tk.Button(bf,text="▶ RUN",font=("Courier",10),
                 bg=BG3,fg=GOLD,relief="flat",padx=12,pady=7,
                 command=self.run_code).pack(side="left",padx=5)
        tk.Button(bf,text="📋 COPY",font=("Courier",10),
                 bg=BG3,fg=NEON,relief="flat",padx=12,pady=7,
                 command=self.copy_code).pack(side="left",padx=5)

        tk.Label(self.root,text="◈ GENERATED CODE",
                font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        self.code=tk.Text(self.root,bg="#001100",fg=GREEN,
                         font=("Courier",9),relief="flat",insertbackground=GREEN)
        self.code.pack(fill="both",expand=True,padx=15,pady=5)

        self.status=tk.Label(self.root,text="Ready to generate",
                            font=("Courier",8),bg=BG,fg=DIM)
        self.status.pack(pady=3)
        tk.Label(self.root,text="BrayoOS Code Generator v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def quick(self,q):
        self.desc.delete("1.0","end")
        self.desc.insert("end",q)

    def generate(self):
        desc=self.desc.get("1.0","end").strip()
        if not desc:return
        self.status.config(text="🧠 AIRA generating...",fg=GOLD)
        threading.Thread(target=self._gen,args=(desc,),daemon=True).start()

    def _gen(self,desc):
        if not GROQ:
            self.root.after(0,self.status.config,
                           {"text":"❌ No GROQ key!","fg":RED});return
        try:
            r=httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ}",
                        "Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile",
                      "messages":[{
                          "role":"user",
                          "content":f"""Write a complete Python tkinter app for BrayoOS.
App description: {desc}
Requirements:
- Use this theme: BG='#080810' PURPLE='#9D00FF' NEON='#CC44FF' GREEN='#44FF88'
- Complete working code, no placeholders
- Under 80 lines if possible
- Include if __name__=='__main__' block
Only output the Python code, nothing else."""}],
                      "max_tokens":800},timeout=20)
            code=r.json()["choices"][0]["message"]["content"].strip()
            if code.startswith("```"):
                code="\n".join(code.split("\n")[1:])
            if code.endswith("```"):
                code="\n".join(code.split("\n")[:-1])
            self.root.after(0,self._show_code,code)
        except Exception as e:
            self.root.after(0,self.status.config,
                           {"text":f"❌ {str(e)[:40]}","fg":RED})

    def _show_code(self,code):
        self.code.delete("1.0","end")
        self.code.insert("end",code)
        self.status.config(text="✅ Code generated!",fg=GREEN)

    def save_app(self):
        code=self.code.get("1.0","end").strip()
        if not code:return
        name=f"generated_{len(os.listdir(os.path.expanduser('~/BrayoOS/core/apps/')))}.py"
        path=os.path.expanduser(f"~/BrayoOS/core/apps/{name}")
        with open(path,"w") as f:f.write(code)
        self.status.config(text=f"💾 Saved: {name}",fg=GREEN)

    def run_code(self):
        code=self.code.get("1.0","end").strip()
        if not code:return
        with open("/tmp/gen_code.py","w") as f:f.write(code)
        import subprocess
        subprocess.Popen(["python3","/tmp/gen_code.py"],
                        env={**os.environ,"DISPLAY":":1"})
        self.status.config(text="▶ Running...",fg=GOLD)

    def copy_code(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.code.get("1.0","end"))
        self.status.config(text="📋 Copied!",fg=GREEN)

if __name__=="__main__":
    root=tk.Tk();CodeGenerator(root);root.mainloop()
