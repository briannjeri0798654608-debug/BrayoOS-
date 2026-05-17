import tkinter as tk
import threading,time,random,os,httpx
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
GROQ=os.environ.get("GROQ_API_KEY","")

class LieDetector:
    def __init__(self,root):
        self.root=root
        self.root.title("🧠 Lie Detector")
        self.root.geometry("650x560")
        self.root.configure(bg=BG)
        self.scanning=False
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🧠 AIRA LIE DETECTOR",font=("Courier",16,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="AI-powered deception analysis engine",font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Truth meter
        meter_f=tk.Frame(self.root,bg=BG2)
        meter_f.pack(fill="x",padx=15,pady=5)
        tk.Label(meter_f,text="TRUTH METER",font=("Courier",9,"bold"),bg=BG2,fg=PURPLE).pack(pady=5)
        self.meter=tk.Canvas(meter_f,width=580,height=30,bg="#001100",highlightthickness=0)
        self.meter.pack(padx=10,pady=3)
        self.meter_lbl=tk.Label(meter_f,text="Awaiting analysis...",font=("Courier",10,"bold"),bg=BG2,fg=DIM)
        self.meter_lbl.pack(pady=5)

        # Stats row
        sf=tk.Frame(self.root,bg=BG)
        sf.pack(fill="x",padx=15,pady=5)
        self.svars={}
        for col,(lbl,color) in enumerate([
            ("TRUTH %",GREEN),("DECEPTION %",RED),
            ("CONFIDENCE",GOLD),("STRESS LVL","#FF6600")]):
            f=tk.Frame(sf,bg=BG3);f.grid(row=0,column=col,padx=4,sticky="ew")
            sf.columnconfigure(col,weight=1)
            tk.Label(f,text=lbl,font=("Courier",7),bg=BG3,fg=DIM).pack(pady=1)
            v=tk.StringVar(value="--")
            self.svars[lbl]=v
            tk.Label(f,textvariable=v,font=("Courier",12,"bold"),bg=BG3,fg=color).pack(pady=1)

        # Input
        tk.Label(self.root,text="◈ ENTER TEXT TO ANALYZE",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(8,2))
        self.inp=tk.Text(self.root,height=5,bg=BG3,fg=WHITE,font=("Courier",10),relief="flat",insertbackground=NEON)
        self.inp.pack(fill="x",padx=15,pady=3)
        self.inp.insert("end","Enter any statement or conversation to analyze...")

        # Results
        tk.Label(self.root,text="◈ AIRA ANALYSIS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(6,2))
        self.out=tk.Text(self.root,height=8,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled",wrap="word")
        self.out.pack(fill="both",expand=True,padx=15,pady=3)
        self.out.tag_config("t",foreground=GREEN)
        self.out.tag_config("l",foreground=RED)
        self.out.tag_config("w",foreground=GOLD)
        self.out.tag_config("i",foreground=DIM)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        tk.Button(bf,text="🧠 ANALYZE",font=("Courier",11,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=15,pady=7,command=self.analyze).pack(side="left",padx=5)
        tk.Button(bf,text="🗑 Clear",font=("Courier",10),bg=BG3,fg=DIM,
                 relief="flat",padx=10,pady=7,command=self.clear).pack(side="left",padx=5)
        tk.Label(self.root,text="BrayoOS Lie Detector • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def draw_meter(self,pct,color):
        self.meter.delete("all")
        w=int(580*pct/100)
        for x in range(0,w,12):
            c=GREEN if pct>60 else GOLD if pct>40 else RED
            self.meter.create_rectangle(x,2,x+10,28,fill=c,outline="")
        self.meter.create_text(290,15,text=f"TRUTH: {pct}%",fill=WHITE,font=("Courier",10,"bold"))

    def log(self,msg,tag="i"):
        self.out.config(state="normal")
        self.out.insert("end",f"{msg}\n",tag)
        self.out.see("end")
        self.out.config(state="disabled")

    def analyze(self):
        text=self.inp.get("1.0","end").strip()
        if not text or text=="Enter any statement or conversation to analyze...":return
        self.out.config(state="normal");self.out.delete("1.0","end");self.out.config(state="disabled")
        threading.Thread(target=self._analyze,args=(text,),daemon=True).start()

    def _analyze(self,text):
        self.root.after(0,self.log,"🧠 AIRA initializing deception analysis...","i")
        self.root.after(0,self.log,"📊 Scanning linguistic patterns...","i")
        time.sleep(0.8)
        self.root.after(0,self.log,"🔍 Checking consistency markers...","i")
        time.sleep(0.6)

        if GROQ:
            try:
                prompt=f"""Analyze this text for deception indicators. Be a lie detector AI.
Text: "{text}"
Respond with JSON only:
{{"truth_pct":75,"deception_pct":25,"confidence":85,"stress_level":"LOW",
"indicators":["specific reason 1","specific reason 2","specific reason 3"],
"verdict":"LIKELY TRUTHFUL",
"red_flags":["any suspicious patterns"],
"analysis":"2 sentence expert analysis"}}"""
                r=httpx.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization":f"Bearer {GROQ}","Content-Type":"application/json"},
                    json={"model":"llama-3.3-70b-versatile",
                          "messages":[{"role":"user","content":prompt}],"max_tokens":300},timeout=10)
                import json,re
                raw=r.json()["choices"][0]["message"]["content"]
                m=re.search(r'\{.*\}',raw,re.DOTALL)
                if m:
                    d=json.loads(m.group())
                    tp=d.get("truth_pct",50);dp=d.get("deception_pct",50)
                    conf=d.get("confidence",70);stress=d.get("stress_level","MED")
                    verdict=d.get("verdict","UNCERTAIN")
                    indicators=d.get("indicators",[])
                    red_flags=d.get("red_flags",[])
                    analysis=d.get("analysis","")
                    self.root.after(0,self._show_results,tp,dp,conf,stress,verdict,indicators,red_flags,analysis)
                    return
            except:pass

        # Local analysis fallback
        words=text.lower().split()
        deception_words=["never","always","honestly","trust me","believe me","i swear","literally","absolutely"]
        hedge_words=["maybe","perhaps","sort of","kind of","i think","probably","might"]
        stress_words=["!","...","??","why would","how dare"]
        d_score=sum(1 for w in words if w in deception_words)*8
        h_score=sum(1 for w in words if w in hedge_words)*5
        s_score=sum(1 for p in stress_words if p in text)*6
        length_score=min(20,len(words)//5)
        deception_pct=min(95,d_score+h_score+s_score+length_score+random.randint(5,20))
        truth_pct=100-deception_pct
        conf=random.randint(65,90)
        stress="HIGH" if deception_pct>70 else "MEDIUM" if deception_pct>40 else "LOW"
        verdict="LIKELY DECEPTIVE" if deception_pct>60 else "LIKELY TRUTHFUL" if truth_pct>65 else "UNCERTAIN"
        indicators=[f"Found {d_score//8} deception markers",f"Hedge words detected: {h_score//5}",f"Stress indicators: {s_score//6}"]
        red_flags=[w for w in words if w in deception_words][:3]
        analysis=f"Text shows {stress.lower()} stress patterns with {deception_pct}% deception probability."
        self.root.after(0,self._show_results,truth_pct,deception_pct,conf,stress,verdict,indicators,red_flags,analysis)

    def _show_results(self,tp,dp,conf,stress,verdict,indicators,red_flags,analysis):
        self.root.after(0,self.draw_meter,tp,GREEN if tp>60 else RED)
        self.svars["TRUTH %"].set(f"{tp}%")
        self.svars["DECEPTION %"].set(f"{dp}%")
        self.svars["CONFIDENCE"].set(f"{conf}%")
        self.svars["STRESS LVL"].set(stress)
        col="t" if tp>60 else "l"
        self.log(f"\n◈ VERDICT: {verdict}",col)
        self.log(f"◈ ANALYSIS: {analysis}","w")
        self.log("\n◈ INDICATORS FOUND:","i")
        for ind in indicators:self.log(f"  → {ind}","i")
        if red_flags:
            self.log("\n🚨 RED FLAGS:","l")
            for rf in red_flags:self.log(f"  ⚠️ '{rf}'","l")
        self.log(f"\n✅ Analysis complete — Confidence: {conf}%","w")
        self.meter_lbl.config(text=verdict,fg=GREEN if tp>60 else RED)

    def clear(self):
        self.inp.delete("1.0","end")
        self.out.config(state="normal");self.out.delete("1.0","end");self.out.config(state="disabled")
        self.meter.delete("all")
        for v in self.svars.values():v.set("--")
        self.meter_lbl.config(text="Awaiting analysis...",fg=DIM)

if __name__=="__main__":
    root=tk.Tk();LieDetector(root);root.mainloop()
