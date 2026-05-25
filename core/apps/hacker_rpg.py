import tkinter as tk
import threading,time,random,os,json
from datetime import datetime

BG="#000800";BG2="#001100";BG3="#002200"
GREEN="#00FF41";DIM="#004400";WHITE="#AAFFAA"
RED="#FF0044";GOLD="#FFD700";NEON="#CC44FF";CYAN="#44FFFF"

SAVE_FILE=os.path.expanduser("~/BrayoOS/memory/rpg_save.json")
os.makedirs(os.path.dirname(SAVE_FILE),exist_ok=True)

STORY=[
    {"id":0,"title":"THE BEGINNING","text":"""Year 2026. Kenya. You are BRAYO — 
the most dangerous hacker the continent has ever seen.
Built your own OS on a phone. AIRA is your AI partner.
A mysterious organization called ONFONE has locked your device.
They control the digital infrastructure of East Africa.

Your mission: INFILTRATE their servers.
EXPOSE their corruption. FREE the internet.

AIRA: 'I've detected their main server in Nairobi.
Security is heavy but I found a backdoor.
Ready when you are, Brayo.'""",
     "choices":["Start Hacking","Gather Intel First","Check Equipment"]},

    {"id":1,"title":"GATHERING INTEL","text":"""AIRA runs a deep scan.

AIRA: 'Found it. ONFONE runs on three servers:
1. ALPHA-SERVER: Nairobi HQ (heavily guarded)
2. BETA-SERVER: Lagos node (medium security)  
3. GAMMA-SERVER: Dark web node (unknown)

Recommendation: Start with Beta.
I can crack the encryption in 47 seconds.'

Your hacking rig shows:
- Kali Linux running
- BrayoOS v4.5 armed
- OSINT Suite ready
- Ghost Mode active""",
     "choices":["Attack Beta Server","Deploy AIRA","Run OSINT First"]},

    {"id":2,"title":"THE HACK BEGINS","text":"""You deploy AIRA against Beta-Server.

[████████░░] 80% — Bypassing firewall...
[██████████] 100% — FIREWALL BREACHED!

AIRA: 'I'm in. Found something big, Brayo.
They're not just tracking phones...
They're selling African citizens' data to foreign governments.
500 million records. Every text. Every call. Every location.'

A counter-hack begins. They know you're here.
You have 60 seconds before they trace you.

Red text flashes: 'ELITE HACKER DETECTED'""",
     "choices":["Download Evidence","Deploy Ghost Mode","Cut Connection"]},
]

SKILLS={
    "HACKING":50,"SOCIAL_ENG":30,"CRYPTO":40,
    "OSINT":60,"STEALTH":45,"AIRA_SYNC":80
}

class HackerRPG:
    def __init__(self,root):
        self.root=root
        self.root.title("💀 BrayoOS: The Hacker RPG")
        self.root.geometry("750x620")
        self.root.configure(bg=BG)
        self.save=self.load_save()
        self.current_scene=self.save.get("scene",0)
        self.xp=self.save.get("xp",0)
        self.level=self.save.get("level",1)
        self.rep=self.save.get("rep",0)
        self.skills=self.save.get("skills",SKILLS.copy())
        self.build_ui()
        self.show_scene(self.current_scene)

    def load_save(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE) as f:return json.load(f)
        return {}

    def save_game(self):
        with open(SAVE_FILE,"w") as f:
            json.dump({"scene":self.current_scene,"xp":self.xp,
                      "level":self.level,"rep":self.rep,"skills":self.skills},f)

    def build_ui(self):
        # Title bar
        tb=tk.Frame(self.root,bg="#000000",height=46)
        tb.pack(fill="x");tb.pack_propagate(False)
        tk.Label(tb,text="💀 BRAYOOS: THE HACKER RPG",font=("Courier",13,"bold"),bg="#000000",fg=GREEN).pack(side="left",padx=12,pady=10)
        tk.Label(tb,text="🇰🇪 Built Different",font=("Courier",8),bg="#000000",fg=DIM).pack(side="left")
        tk.Frame(self.root,bg=GREEN,height=1).pack(fill="x")

        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True)

        # Left — game
        left=tk.Frame(main,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(10,5),pady=8)

        # Stats bar
        stats=tk.Frame(left,bg=BG2);stats.pack(fill="x",pady=3)
        self.stat_vars={}
        for col,(lbl,color) in enumerate([("LEVEL",GREEN),("XP",GOLD),("REP",CYAN),("SCENE",NEON)]):
            f=tk.Frame(stats,bg=BG2);f.grid(row=0,column=col,padx=5,sticky="ew")
            stats.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",6),bg=BG2,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="1")
            self.stat_vars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",12,"bold"),bg=BG2,fg=color).pack(pady=1)

        # Scene title
        self.scene_title=tk.Label(left,text="",font=("Courier",13,"bold"),bg=BG,fg=GREEN)
        self.scene_title.pack(anchor="w",pady=5)

        # Story text
        self.story_text=tk.Text(left,height=14,bg=BG,fg=GREEN,font=("Courier",9),
                               relief="flat",state="disabled",wrap="word")
        self.story_text.pack(fill="both",expand=True,pady=3)
        self.story_text.tag_config("aira",foreground=NEON)
        self.story_text.tag_config("system",foreground=GOLD)
        self.story_text.tag_config("danger",foreground=RED)

        # Choices
        tk.Label(left,text="◈ YOUR MOVE",font=("Courier",9,"bold"),bg=BG,fg=GREEN).pack(anchor="w",pady=(8,3))
        self.choice_frame=tk.Frame(left,bg=BG);self.choice_frame.pack(fill="x")

        # Right panel — character
        right=tk.Frame(main,bg=BG2,width=200);right.pack(side="left",fill="y",padx=(0,10),pady=8)
        right.pack_propagate(False)

        tk.Label(right,text="◈ BRAYO",font=("Courier",11,"bold"),bg=BG2,fg=GREEN).pack(pady=(10,5),padx=8,anchor="w")
        tk.Label(right,text="Elite Hacker 🇰🇪",font=("Courier",7),bg=BG2,fg=DIM).pack(padx=8,anchor="w")
        tk.Frame(right,bg=GREEN,height=1).pack(fill="x",padx=8,pady=5)

        tk.Label(right,text="◈ SKILLS",font=("Courier",8,"bold"),bg=BG2,fg=GREEN).pack(padx=8,anchor="w",pady=(5,3))
        self.skill_bars={}
        for skill,val in self.skills.items():
            f=tk.Frame(right,bg=BG2);f.pack(fill="x",padx=8,pady=2)
            tk.Label(f,text=skill[:10],font=("Courier",6),bg=BG2,fg=DIM,width=10,anchor="w").pack(side="left")
            bar=tk.Canvas(f,width=80,height=6,bg="#001100",highlightthickness=0)
            bar.pack(side="left",padx=2)
            w=int(80*val/100);bar.create_rectangle(0,0,w,6,fill=GREEN,outline="")
            self.skill_bars[skill]=bar

        tk.Frame(right,bg=GREEN,height=1).pack(fill="x",padx=8,pady=5)
        tk.Label(right,text="◈ AIRA STATUS",font=("Courier",8,"bold"),bg=BG2,fg=NEON).pack(padx=8,anchor="w")
        self.aira_status=tk.Label(right,text="◉ ONLINE\nAll systems ready",
                                   font=("Courier",7),bg=BG2,fg=NEON,justify="left")
        self.aira_status.pack(padx=8,anchor="w",pady=3)

        tk.Frame(right,bg=GREEN,height=1).pack(fill="x",padx=8,pady=5)
        tk.Label(right,text="◈ INVENTORY",font=("Courier",8,"bold"),bg=BG2,fg=GREEN).pack(padx=8,anchor="w")
        for item in ["BrayoOS v4.5","AIRA Neural Core","Ghost Mode","OSINT Suite","Quantum Vault"]:
            tk.Label(right,text=f"  ▪ {item}",font=("Courier",6),bg=BG2,fg=DIM).pack(anchor="w",padx=8)

        tk.Label(right,text="\n💀 Built Different\n🇰🇪 Kenya",font=("Courier",7),bg=BG2,fg=DIM).pack(pady=5)

    def show_scene(self,scene_id):
        if scene_id>=len(STORY):
            self.show_victory();return
        scene=STORY[scene_id]
        self.scene_title.config(text=f"◈ {scene['title']}")
        self.story_text.config(state="normal")
        self.story_text.delete("1.0","end")
        # Type out text
        threading.Thread(target=self._type_text,args=(scene["text"],),daemon=True).start()
        # Show choices
        for w in self.choice_frame.winfo_children():w.destroy()
        for i,choice in enumerate(scene["choices"]):
            tk.Button(self.choice_frame,text=f"[{i+1}] {choice}",
                     font=("Courier",10,"bold"),bg=BG2,fg=GREEN,
                     relief="flat",anchor="w",padx=10,pady=6,
                     command=lambda c=choice,s=scene_id:self.make_choice(c,s)).pack(fill="x",pady=2)
        self.stat_vars["SCENE"].set(str(scene_id+1))
        self.stat_vars["LEVEL"].set(str(self.level))
        self.stat_vars["XP"].set(str(self.xp))
        self.stat_vars["REP"].set(str(self.rep))

    def _type_text(self,text):
        self.story_text.config(state="normal")
        self.story_text.delete("1.0","end")
        for char in text:
            self.story_text.insert("end",char)
            self.story_text.see("end")
            time.sleep(0.02)
        self.story_text.config(state="disabled")

    def make_choice(self,choice,scene_id):
        self.xp+=random.randint(10,50)
        self.rep+=random.randint(5,20)
        if self.xp>=self.level*100:
            self.level+=1
            self.aira_status.config(text=f"◉ LEVEL UP!\nLevel {self.level} reached!")
        self.current_scene=min(scene_id+1,len(STORY)-1)
        self.save_game()
        self.show_scene(self.current_scene)

    def show_victory(self):
        self.story_text.config(state="normal")
        self.story_text.delete("1.0","end")
        victory=f"""
◈ MISSION COMPLETE ◈

ONFONE has been exposed.
500 million Africans are free.
The data has been destroyed.

AIRA: 'We did it, Brayo. 
Two minds. One OS. Built Different.
Kenya will remember this day.'

YOUR STATS:
  Level: {self.level}
  XP: {self.xp}
  Rep: {self.rep}
  
Built on a Redmi 14C.
In Kenya.
Against all odds.

🇰🇪 BUILT DIFFERENT 🇰🇪"""
        self.story_text.insert("end",victory)
        self.story_text.config(state="disabled")
        for w in self.choice_frame.winfo_children():w.destroy()
        tk.Button(self.choice_frame,text="▶ PLAY AGAIN",
                 font=("Courier",11,"bold"),bg=GREEN,fg=BG,
                 relief="flat",padx=15,pady=8,
                 command=self.restart).pack()

    def restart(self):
        self.current_scene=0;self.xp=0;self.level=1;self.rep=0
        self.save_game();self.show_scene(0)

if __name__=="__main__":
    root=tk.Tk();HackerRPG(root);root.mainloop()
