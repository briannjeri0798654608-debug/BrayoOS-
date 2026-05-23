import tkinter as tk
import threading,httpx,os,json,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
GROQ=os.environ.get("GROQ_API_KEY","")

class AINews:
    def __init__(self,root):
        self.root=root
        self.root.title("📰 AI News Generator")
        self.root.geometry("700x580")
        self.root.configure(bg=BG)
        self.build_ui()
        self.fetch_news()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="📰 AIRA AI NEWS",font=("Courier",14,"bold"),bg=BG2,fg=NEON).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="Real news + AIRA analysis",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        self.time_lbl=tk.Label(hdr,text="",font=("Courier",9),bg=BG2,fg=GOLD)
        self.time_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        # Topics
        tf=tk.Frame(self.root,bg=BG);tf.pack(fill="x",padx=10,pady=6)
        tk.Label(tf,text="Topic:",font=("Courier",9),bg=BG,fg=DIM).pack(side="left",padx=5)
        self.topic_var=tk.StringVar(value="Technology")
        for t in ["Technology","Kenya","Cybersecurity","AI","Africa","World"]:
            tk.Button(tf,text=t,font=("Courier",8),bg=BG3,fg=NEON,relief="flat",
                     padx=8,pady=3,command=lambda x=t:self.set_topic(x)).pack(side="left",padx=2)

        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True,padx=10,pady=5)

        # News list
        left=tk.Frame(main,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(0,8))
        tk.Label(left,text="◈ HEADLINES",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w")
        self.headlines=tk.Listbox(left,bg=BG3,fg=WHITE,font=("Courier",8),
                                  selectbackground=PURPLE,relief="flat",height=8,cursor="hand2")
        self.headlines.pack(fill="both",expand=True,pady=3)
        self.headlines.bind("<<ListboxSelect>>",self.show_article)

        tk.Label(left,text="◈ ARTICLE",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",pady=(6,2))
        self.article=tk.Text(left,height=8,bg=BG3,fg=WHITE,font=("Courier",9),
                            relief="flat",state="disabled",wrap="word")
        self.article.pack(fill="both",expand=True)

        # Right — AIRA analysis
        right=tk.Frame(main,bg=BG2,width=220);right.pack(side="left",fill="y")
        right.pack_propagate(False)
        tk.Label(right,text="◈ AIRA ANALYSIS",font=("Courier",8,"bold"),bg=BG2,fg=NEON).pack(pady=6,padx=8,anchor="w")
        self.analysis=tk.Text(right,bg=BG2,fg=WHITE,font=("Courier",7),
                             relief="flat",state="disabled",wrap="word")
        self.analysis.pack(fill="both",expand=True,padx=5,pady=5)
        tk.Button(right,text="🧠 Analyze Selected",font=("Courier",7,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=8,pady=4,command=self.analyze).pack(pady=5)

        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=5)
        tk.Button(bf,text="🔄 Refresh",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=12,pady=5,command=self.fetch_news).pack(side="left",padx=4)
        tk.Button(bf,text="📋 Copy",font=("Courier",10),bg=BG3,fg=GREEN,
                 relief="flat",padx=10,pady=5,command=self.copy_article).pack(side="left",padx=4)
        tk.Label(self.root,text="BrayoOS AI News v4.5 • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

        self.articles_data=[]
        self.update_time()

    def update_time(self):
        self.time_lbl.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000,self.update_time)

    def set_topic(self,topic):
        self.topic_var.set(topic)
        self.fetch_news()

    def fetch_news(self):
        threading.Thread(target=self._fetch,daemon=True).start()

    def _fetch(self):
        topic=self.topic_var.get()
        self.root.after(0,self.headlines.delete,0,"end")
        self.root.after(0,self.headlines.insert,"end","  Loading news...")
        try:
            r=httpx.get(f"https://gnews.io/api/v4/search?q={topic}&lang=en&max=8&token=demo",timeout=8)
            if r.status_code==200:
                data=r.json()
                articles=data.get("articles",[])
                if articles:
                    self.articles_data=articles
                    self.root.after(0,self.headlines.delete,0,"end")
                    for a in articles:
                        title=a.get("title","")[:70]
                        self.root.after(0,self.headlines.insert,"end",f"  📰 {title}")
                    return
        except:pass
        # Fallback AI-generated news
        self._generate_news(topic)

    def _generate_news(self,topic):
        headlines=[
            f"BrayoOS: Kenya Student Builds Complete OS on Phone",
            f"Africa Rising: {topic} Innovation Leads Global Tech",
            f"AIRA AI: The First Phone-Built AI Assistant in East Africa",
            f"Cybersecurity in {topic}: New Threats Emerge in 2026",
            f"Open Source Movement: BrayoOS Goes Global",
            f"Redmi 14C Powers Full Linux Desktop — Impossible No More",
            f"Kenya Tech Scene: Students Building World-Class Software",
            f"HELB Funded: Brayo's OS Journey from Phone to Revolution",
        ]
        self.articles_data=[{"title":h,"description":f"Full story about {h}","url":"https://github.com/briannjeri0798654608-debug/BrayoOS-"} for h in headlines]
        self.root.after(0,self.headlines.delete,0,"end")
        for h in headlines:
            self.root.after(0,self.headlines.insert,"end",f"  📰 {h[:65]}")

    def show_article(self,e):
        sel=self.headlines.curselection()
        if not sel or not self.articles_data:return
        idx=sel[0]
        if idx>=len(self.articles_data):return
        article=self.articles_data[idx]
        self.article.config(state="normal");self.article.delete("1.0","end")
        self.article.insert("end",f"{article.get('title','')}\n\n")
        self.article.insert("end",f"{article.get('description','')}\n\n")
        self.article.insert("end",f"Source: {article.get('url','')}")
        self.article.config(state="disabled")

    def analyze(self):
        sel=self.headlines.curselection()
        if not sel or not self.articles_data:return
        idx=sel[0]
        if idx>=len(self.articles_data):return
        title=self.articles_data[idx].get("title","")
        threading.Thread(target=self._analyze,args=(title,),daemon=True).start()

    def _analyze(self,title):
        self.root.after(0,self.analysis.config,{"state":"normal"})
        self.root.after(0,self.analysis.delete,"1.0","end")
        self.root.after(0,self.analysis.insert,"end","🧠 AIRA analyzing...\n\n")
        self.root.after(0,self.analysis.config,{"state":"disabled"})
        if GROQ:
            try:
                r=httpx.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization":f"Bearer {GROQ}","Content-Type":"application/json"},
                    json={"model":"llama-3.3-70b-versatile",
                          "messages":[{"role":"user","content":f"As AIRA, AI of BrayoOS from Kenya, briefly analyze this news in 3 points: '{title}'. Focus on impact for Kenya/Africa tech. Max 100 words."}],
                          "max_tokens":150},timeout=10)
                analysis=r.json()["choices"][0]["message"]["content"]
                self.root.after(0,self._show_analysis,analysis)
                return
            except:pass
        analysis=f"AIRA Analysis:\n\n→ Relevant to Kenya tech ecosystem\n→ Shows growing African innovation\n→ BrayoOS proves anything is possible\n\nBuilt Different. 🇰🇪"
        self.root.after(0,self._show_analysis,analysis)

    def _show_analysis(self,text):
        self.analysis.config(state="normal")
        self.analysis.delete("1.0","end")
        self.analysis.insert("end",text)
        self.analysis.config(state="disabled")

    def copy_article(self):
        content=self.article.get("1.0","end")
        self.root.clipboard_clear();self.root.clipboard_append(content)

if __name__=="__main__":
    root=tk.Tk();AINews(root);root.mainloop()
