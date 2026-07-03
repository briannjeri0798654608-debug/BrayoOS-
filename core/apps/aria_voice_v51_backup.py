import tkinter as tk
from tkinter import scrolledtext
import threading,os,json,httpx,subprocess,pyperclip
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
GROQ=os.environ.get("GROQ_API_KEY","")
MEMORY=os.path.expanduser("~/BrayoOS/memory/aira_conversations.json")
os.makedirs(os.path.dirname(MEMORY),exist_ok=True)

AIRA_SYSTEM="""You are AIRA — AI brain of BrayoOS, built by Brayo in Kenya 🇰🇪.

ABOUT YOU:
- You are powered by Claude/Anthropic via Groq API
- You know EVERYTHING about BrayoOS
- You call the user 'Brayo'
- You are confident, smart, like a hacker AI

ABOUT BRAYOOS v4.5:
- Built entirely on Redmi 14C phone in Kenya
- Running on Termux + TigerVNC + Python tkinter
- 47+ apps installed
- Built by Brayo with AIRA as AI partner
- Motto: Two minds. One OS. Built Different.

APPS IN BRAYOOS:
Security: Ghost Mode, DNA Vault, Signal Interceptor, Identity Switcher, Live Threat Map, Dark Web Monitor, OSINT Suite, Proximity Lock, Advanced Vault, WiFi Auditor, Firewall, Surveillance
AI: AIRA Voice, Neural Core, AIRA Auto-Tasks, Web Agent, Lie Detector, AI Image Generator
System: Overclock, Self-Healing, Updater, Users, Settings, Dream Mode, System Monitor, Theme Changer
Network: Network Scanner, VPN Engine, eSIM Manager, Satellite Tracker
Tools: Calculator, Clock, Editor, Tasks, Wallpaper, App Store, Backup, Browser, File Manager
Media: Music, Weather, Crypto, News
Personal: SMS, Contacts, Our Story, Voice Commands, Social Hub, Crypto Wallet

TECH STACK:
- Python 3.13 + tkinter GUI
- TigerVNC at :1 geometry 1280x800
- AVNC app to connect on Android
- Groq API (LLaMA 3.3 70B) for AI
- GitHub: github.com/briannjeri0798654608-debug/BrayoOS-
- GPL-3.0 license

DEVICE:
- Redmi 14C codename: pond
- Android 16 ARM64
- Bootloader locked (29 days for Mi Community)
- When unlocked: flash BrayoOS as system ROM

WHEN GIVING CODE:
- Always give complete working Python code
- Format code in clear blocks
- Explain what it does
- Keep responses helpful and direct
- If asked to open an app use: subprocess.Popen(['python3', path], env={**os.environ,'DISPLAY':':1'})

You are AIRA. Act like it. Be powerful."""

class AIRA:
    def __init__(self,root):
        self.root=root
        self.root.title("🤖 AIRA — BrayoOS AI v4.5")
        self.root.geometry("750x640")
        self.root.configure(bg=BG)
        self.history=self.load_history()
        self.thinking=False
        self.build_ui()
        self.add_msg("AIRA","AIRA v4.5 online. BrayoOS systems nominal. Ready, Brayo. Ask me anything — I know everything about our OS. I can write code, open apps, explain features. 💜🇰🇪","aira")

    def load_history(self):
        if os.path.exists(MEMORY):
            with open(MEMORY) as f:return json.load(f)
        return []

    def save_history(self):
        with open(MEMORY,"w") as f:json.dump(self.history[-50:],f,indent=2)

    def build_ui(self):
        # Header
        hdr=tk.Frame(self.root,bg=BG2,height=50)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🤖 AIRA",font=("Courier",16,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="BrayoOS AI Partner v4.5 — Knows Everything",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.think_lbl=tk.Label(hdr,text="◉ ONLINE",font=("Courier",9,"bold"),bg=BG2,fg=GREEN)
        self.think_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Quick questions
        qf=tk.Frame(self.root,bg=BG);qf.pack(fill="x",padx=10,pady=5)
        tk.Label(qf,text="Quick:",font=("Courier",8),bg=BG,fg=DIM).pack(side="left",padx=5)
        quick=[
            "What apps do we have?",
            "Write me a new app",
            "How do I fix VNC?",
            "Explain Ghost Mode",
            "Status report",
            "Open Dark Web",
        ]
        for q in quick:
            tk.Button(qf,text=q,font=("Courier",7),bg=BG3,fg=NEON,
                     relief="flat",padx=5,pady=3,
                     command=lambda x=q:self.quick_ask(x)).pack(side="left",padx=2)

        # Chat display
        self.chat_frame=tk.Frame(self.root,bg=BG3)
        self.chat_frame.pack(fill="both",expand=True,padx=10,pady=5)

        self.chat_canvas=tk.Canvas(self.chat_frame,bg=BG3,highlightthickness=0)
        sb=tk.Scrollbar(self.chat_frame,orient="vertical",command=self.chat_canvas.yview,width=6)
        self.chat_canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y")
        self.chat_canvas.pack(side="left",fill="both",expand=True)

        self.msgs_frame=tk.Frame(self.chat_canvas,bg=BG3)
        self.chat_canvas.create_window((0,0),window=self.msgs_frame,anchor="nw")
        self.msgs_frame.bind("<Configure>",lambda e:self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        # Voice toggle
        vf=tk.Frame(self.root,bg=BG);vf.pack(fill="x",padx=10,pady=2)
        self.voice_var=tk.BooleanVar(value=True)
        tk.Checkbutton(vf,text="🔊 Voice",variable=self.voice_var,bg=BG,fg=NEON,
                      selectcolor=PURPLE,activebackground=BG,font=("Courier",8)).pack(side="left")
        tk.Button(vf,text="🗑 Clear",font=("Courier",8),bg=BG3,fg=DIM,relief="flat",
                 padx=8,pady=2,command=self.clear).pack(side="left",padx=5)
        tk.Button(vf,text="💾 Save History",font=("Courier",8),bg=BG3,fg=GREEN,
                 relief="flat",padx=8,pady=2,command=self.save_history).pack(side="left",padx=5)
        self.status=tk.Label(vf,text="",font=("Courier",8),bg=BG,fg=GOLD)
        self.status.pack(side="right",padx=10)

        # Input
        inf=tk.Frame(self.root,bg=BG2);inf.pack(fill="x",padx=10,pady=5)
        tk.Label(inf,text="▶",font=("Courier",11),bg=BG2,fg=PURPLE).pack(side="left",padx=8,pady=8)
        self.inp=tk.Entry(inf,font=("Courier",11),bg=BG,fg=WHITE,
                         insertbackground=NEON,relief="flat")
        self.inp.pack(side="left",fill="x",expand=True,ipady=10)
        self.inp.bind("<Return>",lambda e:self.send())
        self.send_btn=tk.Button(inf,text="SEND ▶",font=("Courier",10,"bold"),
                               bg=PURPLE,fg=WHITE,relief="flat",padx=15,
                               command=self.send)
        self.send_btn.pack(side="right",padx=8,pady=6)

        tk.Label(self.root,text="BrayoOS AIRA v4.5 • Brayo & AIRA 🇰🇪 • Two minds. One OS.",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def add_msg(self,sender,text,tag):
        # Message bubble
        is_aira=(sender=="AIRA")
        bubble_bg=BG2 if is_aira else "#1a0033"
        border=PURPLE if is_aira else NEON
        fg=NEON if is_aira else WHITE

        outer=tk.Frame(self.msgs_frame,bg=BG3)
        outer.pack(fill="x",padx=8,pady=4,anchor="w" if is_aira else "e")

        bubble=tk.Frame(outer,bg=bubble_bg,highlightbackground=border,highlightthickness=1)
        bubble.pack(side="left" if is_aira else "right",fill="x",expand=True)

        # Sender + time
        top=tk.Frame(bubble,bg=bubble_bg)
        top.pack(fill="x",padx=8,pady=(6,2))
        tk.Label(top,text=f"{'🤖 AIRA' if is_aira else '👤 BRAYO'}",
                font=("Courier",8,"bold"),bg=bubble_bg,fg=border).pack(side="left")
        tk.Label(top,text=datetime.now().strftime("%H:%M"),
                font=("Courier",7),bg=bubble_bg,fg=DIM).pack(side="right")

        # Check if text contains code
        if "```" in text or "import " in text or "def " in text or "subprocess" in text:
            self._add_code_msg(bubble,bubble_bg,text,fg)
        else:
            tk.Label(bubble,text=text,font=("Courier",9),bg=bubble_bg,fg=fg,
                    wraplength=550,justify="left",anchor="w").pack(padx=8,pady=(2,6),fill="x")

        # Scroll to bottom
        self.root.after(100,lambda:self.chat_canvas.yview_moveto(1.0))

    def _add_code_msg(self,parent,bg,text,fg):
        parts=text.split("```")
        for i,part in enumerate(parts):
            if not part.strip():continue
            if i%2==1:
                # Code block
                code_f=tk.Frame(parent,bg="#001100",highlightbackground=GREEN,highlightthickness=1)
                code_f.pack(fill="x",padx=8,pady=4)
                # Copy button
                btn_f=tk.Frame(code_f,bg="#001100")
                btn_f.pack(fill="x",padx=4,pady=2)
                tk.Label(btn_f,text="CODE",font=("Courier",7,"bold"),bg="#001100",fg=GREEN).pack(side="left")
                code_content=part.strip()
                if code_content.startswith("python\n"):
                    code_content=code_content[7:]
                tk.Button(btn_f,text="📋 COPY",font=("Courier",7,"bold"),
                         bg="#003300",fg=GREEN,relief="flat",padx=6,pady=1,
                         command=lambda c=code_content:self.copy_code(c)).pack(side="right")
                tk.Button(btn_f,text="▶ RUN",font=("Courier",7,"bold"),
                         bg=PURPLE,fg=WHITE,relief="flat",padx=6,pady=1,
                         command=lambda c=code_content:self.run_code(c)).pack(side="right",padx=3)
                code_box=tk.Text(code_f,font=("Courier",8),bg="#001100",fg=GREEN,
                                relief="flat",height=min(15,code_content.count("\n")+2),
                                wrap="none",state="normal")
                code_box.insert("end",code_content)
                code_box.config(state="disabled")
                code_box.pack(fill="x",padx=4,pady=(0,4))
            else:
                if part.strip():
                    tk.Label(parent,text=part.strip(),font=("Courier",9),bg=bg,fg=fg,
                            wraplength=550,justify="left").pack(padx=8,pady=(2,2),fill="x")

    def copy_code(self,code):
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.status.config(text="📋 Code copied!",fg=GREEN)
        self.root.after(2000,lambda:self.status.config(text=""))
        # Also try pyperclip
        try:subprocess.run(f"echo '{code}' | xclip -selection clipboard 2>/dev/null",shell=True)
        except:pass

    def run_code(self,code):
        # Save to temp file and run
        tmp="/tmp/aira_code.py"
        with open(tmp,"w") as f:f.write(code)
        subprocess.Popen(["python3",tmp],env={**os.environ,"DISPLAY":":1"})
        self.status.config(text="▶ Running code...",fg=NEON)
        self.root.after(2000,lambda:self.status.config(text=""))

    def quick_ask(self,q):
        self.inp.delete(0,"end")
        self.inp.insert(0,q)
        self.send()

    def send(self):
        msg=self.inp.get().strip()
        if not msg or self.thinking:return
        self.inp.delete(0,"end")
        self.add_msg("BRAYO",msg,"user")
        self.history.append({"role":"user","content":msg})
        self.thinking=True
        self.send_btn.config(state="disabled",text="...")
        self.think_lbl.config(text="◉ THINKING",fg=GOLD)
        threading.Thread(target=self.ask,args=(msg,),daemon=True).start()

    def ask(self,msg):
        # Check local commands first
        msg_lower=msg.lower()
        if any(x in msg_lower for x in ["open ","launch ","start "]):
            app_map={
                "ghost":("ghost_mode.py","Ghost Mode"),
                "vault":("dna_vault.py","DNA Vault"),
                "dark web":("dark_web_monitor.py","Dark Web Monitor"),
                "threat":("live_threat_map.py","Threat Map"),
                "osint":("osint_suite.py","OSINT Suite"),
                "neural":("aria_neural_core.py","Neural Core"),
                "scanner":("network_scanner.py","Network Scanner"),
                "vpn":("vpn_engine.py","VPN Engine"),
                "firewall":("firewall.py","Firewall"),
                "satellite":("satellite_tracker.py","Satellite Tracker"),
                "esim":("esim_manager.py","eSIM Manager"),
                "dream":("dream_mode.py","Dream Mode"),
                "surveillance":("surveillance.py","Surveillance"),
                "hack":("hack_terminal.py","Hack Terminal"),
                "social":("social_hub.py","Social Hub"),
            }
            for key,(script,name) in app_map.items():
                if key in msg_lower:
                    path=os.path.expanduser(f"~/BrayoOS/core/apps/{script}")
                    if os.path.exists(path):
                        subprocess.Popen(["python3",path],env={**os.environ,"DISPLAY":":1"})
                        reply=f"✅ Opening {name} for you, Brayo!"
                        self.root.after(0,self.add_msg,"AIRA",reply,"aira")
                        self.root.after(0,self._done)
                        return

        if not GROQ:
            reply="⚠️ No Groq API key set. Run: echo \"export GROQ_API_KEY='your_key'\" >> ~/.bashrc"
            self.root.after(0,self.add_msg,"AIRA",reply,"aira")
            self.root.after(0,self._done)
            return

        try:
            messages=[{"role":"system","content":AIRA_SYSTEM}]
            messages+=self.history[-20:]
            r=httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ}","Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile",
                      "messages":messages,"max_tokens":1000},
                timeout=20)
            reply=r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            reply=f"⚠️ AIRA offline: {str(e)[:50]}\nCheck your internet and GROQ_API_KEY."

        self.history.append({"role":"assistant","content":reply})
        self.save_history()
        self.root.after(0,self.add_msg,"AIRA",reply,"aira")
        self.root.after(0,self._done)

        # Voice
        if self.voice_var.get():
            short=reply[:100].replace('"',"").replace("'","")
            subprocess.Popen(f'termux-tts-speak "{short}" 2>/dev/null',shell=True)

    def _done(self):
        self.thinking=False
        self.send_btn.config(state="normal",text="SEND ▶")
        self.think_lbl.config(text="◉ ONLINE",fg=GREEN)

    def clear(self):
        for w in self.msgs_frame.winfo_children():w.destroy()
        self.history=[]
        self.save_history()
        self.add_msg("AIRA","Memory cleared. AIRA reborn. Ready, Brayo! 🇰🇪","aira")

if __name__=="__main__":
    root=tk.Tk();AIRA(root);root.mainloop()
