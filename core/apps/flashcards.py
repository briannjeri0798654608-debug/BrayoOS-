import tkinter as tk
import os,json,random,threading,httpx
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

CARDS_FILE=os.path.expanduser("~/BrayoOS/memory/flashcards.json")
os.makedirs(os.path.dirname(CARDS_FILE),exist_ok=True)
GROQ=os.environ.get("GROQ_API_KEY","")

class Flashcards:
    def __init__(self,root):
        self.root=root
        self.root.title("🎓 Flashcards")
        self.root.geometry("640x520")
        self.root.configure(bg=BG)
        self.cards=self.load()
        self.current=0
        self.showing_answer=False
        self.score={"correct":0,"wrong":0}
        self.build_ui()

    def load(self):
        if os.path.exists(CARDS_FILE):
            with open(CARDS_FILE) as f:return json.load(f)
        return [
            {"q":"What is BrayoOS?","a":"A complete OS built on Redmi 14C phone in Kenya by Brayo & AIRA"},
            {"q":"What language is BrayoOS built in?","a":"Python 3.13 + tkinter GUI on Termux + TigerVNC"},
            {"q":"What is AIRA?","a":"AI partner of BrayoOS powered by Claude/LLaMA 3.3 70B via Groq API"},
            {"q":"What is Ghost Mode?","a":"Network invisibility — hides BrayoOS from network scanners"},
            {"q":"BrayoOS motto?","a":"Two minds. One OS. Built Different."},
        ]

    def save(self):
        with open(CARDS_FILE,"w") as f:json.dump(self.cards,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=44)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🎓 FLASHCARD STUDY",font=("Courier",13,"bold"),
                bg=BG2,fg=NEON).pack(side="left",padx=12,pady=10)
        self.score_lbl=tk.Label(hdr,text="✅0 ❌0",font=("Courier",9),bg=BG2,fg=GOLD)
        self.score_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Progress
        self.prog_lbl=tk.Label(self.root,text="Card 1 of 5",
                              font=("Courier",9),bg=BG,fg=DIM)
        self.prog_lbl.pack(pady=5)
        self.prog_c=tk.Canvas(self.root,width=600,height=8,
                             bg=BG3,highlightthickness=0)
        self.prog_c.pack()

        # Card
        self.card_f=tk.Frame(self.root,bg=BG3,
                            highlightbackground=PURPLE,highlightthickness=2)
        self.card_f.pack(fill="x",padx=15,pady=10)

        tk.Label(self.card_f,text="QUESTION",font=("Courier",8,"bold"),
                bg=BG3,fg=DIM).pack(anchor="w",padx=12,pady=(10,3))
        self.q_lbl=tk.Label(self.card_f,text="",font=("Courier",13),
                            bg=BG3,fg=NEON,wraplength=560,justify="center")
        self.q_lbl.pack(pady=10,padx=12)
        tk.Frame(self.card_f,bg=PURPLE,height=1).pack(fill="x",padx=12)
        self.ans_lbl=tk.Label(self.card_f,text="[Tap to reveal answer]",
                             font=("Courier",11),bg=BG3,fg=DIM,
                             wraplength=560,justify="center")
        self.ans_lbl.pack(pady=15,padx=12)

        self.card_f.bind("<Button-1>",lambda e:self.flip())
        self.q_lbl.bind("<Button-1>",lambda e:self.flip())
        self.ans_lbl.bind("<Button-1>",lambda e:self.flip())

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        tk.Button(bf,text="✅ Know it",font=("Courier",11,"bold"),
                 bg=GREEN,fg=BG,relief="flat",padx=15,pady=7,
                 command=lambda:self.next_card(True)).pack(side="left",padx=5)
        tk.Button(bf,text="❌ Review",font=("Courier",11,"bold"),
                 bg=RED,fg=WHITE,relief="flat",padx=15,pady=7,
                 command=lambda:self.next_card(False)).pack(side="left",padx=5)
        tk.Button(bf,text="🔀 Shuffle",font=("Courier",10),
                 bg=BG3,fg=GOLD,relief="flat",padx=12,pady=7,
                 command=self.shuffle).pack(side="left",padx=5)
        tk.Button(bf,text="🤖 AI Cards",font=("Courier",10),
                 bg=BG3,fg=NEON,relief="flat",padx=12,pady=7,
                 command=self.ai_generate).pack(side="left",padx=5)

        # Add card
        add_f=tk.Frame(self.root,bg=BG3);add_f.pack(fill="x",padx=15,pady=5)
        row1=tk.Frame(add_f,bg=BG3);row1.pack(fill="x",padx=8,pady=3)
        tk.Label(row1,text="Q:",font=("Courier",9),bg=BG3,fg=DIM,width=3).pack(side="left")
        self.q_inp=tk.Entry(row1,font=("Courier",9),bg=BG,fg=WHITE,
                           insertbackground=NEON,relief="flat")
        self.q_inp.pack(side="left",fill="x",expand=True,ipady=5)
        row2=tk.Frame(add_f,bg=BG3);row2.pack(fill="x",padx=8,pady=3)
        tk.Label(row2,text="A:",font=("Courier",9),bg=BG3,fg=DIM,width=3).pack(side="left")
        self.a_inp=tk.Entry(row2,font=("Courier",9),bg=BG,fg=WHITE,
                           insertbackground=NEON,relief="flat")
        self.a_inp.pack(side="left",fill="x",expand=True,ipady=5)
        tk.Button(add_f,text="➕ Add",font=("Courier",8),bg=PURPLE,fg=WHITE,
                 relief="flat",command=self.add_card).pack(pady=5)

        tk.Label(self.root,text="BrayoOS Flashcards v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)
        self.show_card()

    def show_card(self):
        if not self.cards:return
        self.showing_answer=False
        c=self.cards[self.current]
        self.q_lbl.config(text=c["q"])
        self.ans_lbl.config(text="[Tap to reveal answer]",fg=DIM)
        self.prog_lbl.config(text=f"Card {self.current+1} of {len(self.cards)}")
        pct=int((self.current+1)*600/len(self.cards))
        self.prog_c.delete("all")
        self.prog_c.create_rectangle(0,0,pct,8,fill=PURPLE,outline="")
        self.score_lbl.config(text=f"✅{self.score['correct']} ❌{self.score['wrong']}")

    def flip(self):
        if not self.cards:return
        self.showing_answer=not self.showing_answer
        if self.showing_answer:
            self.ans_lbl.config(text=self.cards[self.current]["a"],fg=GREEN)
        else:
            self.ans_lbl.config(text="[Tap to reveal answer]",fg=DIM)

    def next_card(self,correct):
        if correct:self.score["correct"]+=1
        else:self.score["wrong"]+=1
        self.current=(self.current+1)%len(self.cards)
        self.show_card()

    def shuffle(self):
        random.shuffle(self.cards)
        self.current=0
        self.show_card()

    def add_card(self):
        q=self.q_inp.get().strip()
        a=self.a_inp.get().strip()
        if q and a:
            self.cards.append({"q":q,"a":a})
            self.save()
            self.q_inp.delete(0,"end")
            self.a_inp.delete(0,"end")

    def ai_generate(self):
        if not GROQ:return
        threading.Thread(target=self._ai_gen,daemon=True).start()

    def _ai_gen(self):
        try:
            r=httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ}",
                        "Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile",
                      "messages":[{"role":"user",
                          "content":"Generate 5 cybersecurity flashcards as JSON array: [{\"q\":\"question\",\"a\":\"answer\"}]. Only JSON, no text."}],
                      "max_tokens":400},timeout=15)
            import re
            raw=r.json()["choices"][0]["message"]["content"]
            m=re.search(r'\[.*\]',raw,re.DOTALL)
            if m:
                new=json.loads(m.group())
                self.cards.extend(new)
                self.save()
                self.root.after(0,self.show_card)
        except:pass

if __name__=="__main__":
    root=tk.Tk();Flashcards(root);root.mainloop()
