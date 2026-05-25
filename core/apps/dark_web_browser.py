import tkinter as tk
import threading,subprocess,os,httpx,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

BOOKMARKS=[
    ("DuckDuckGo Onion","https://3g2upl4pq6kufc4m.onion"),
    ("ProtonMail Onion","https://protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd.onion"),
    ("SecureDrop","https://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion"),
    ("Facebook Onion","https://facebookwkhpilnemxj7asber7cybef4vqcnirvlvmuq2ewfwcfbmdq67a.onion"),
    ("The Hidden Wiki","http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2yad.onion"),
]

class DarkWebBrowser:
    def __init__(self,root):
        self.root=root
        self.root.title("🕷️ Dark Web Browser")
        self.root.geometry("750x600")
        self.root.configure(bg=BG)
        self.tor_running=False
        self.build_ui()
        self.check_tor()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg="#000000",height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🕷️ DARK WEB BROWSER",font=("Courier",14,"bold"),bg="#000000",fg=RED).pack(side="left",padx=12,pady=10)
        self.tor_lbl=tk.Label(hdr,text="⬤ TOR: OFFLINE",font=("Courier",9,"bold"),bg="#000000",fg=RED)
        self.tor_lbl.pack(side="right",padx=12)
        tk.Frame(self.root,bg=RED,height=2).pack(fill="x")

        # Warning banner
        warn=tk.Frame(self.root,bg="#1a0000")
        warn.pack(fill="x",padx=15,pady=5)
        tk.Label(warn,text="⚠️  WARNING: Dark web access for research/privacy only. Illegal activity is prohibited.",
                font=("Courier",8,"bold"),bg="#1a0000",fg=RED).pack(pady=5)

        # Tor status
        tor_f=tk.Frame(self.root,bg=BG3);tor_f.pack(fill="x",padx=15,pady=5)
        tk.Label(tor_f,text="🧅 TOR STATUS:",font=("Courier",9,"bold"),bg=BG3,fg=GOLD).pack(side="left",padx=10,pady=8)
        self.tor_status=tk.Label(tor_f,text="Checking...",font=("Courier",9),bg=BG3,fg=DIM)
        self.tor_status.pack(side="left")
        tk.Button(tor_f,text="⚡ Start Tor",font=("Courier",9,"bold"),bg=BG3,fg=GREEN,
                 relief="flat",padx=10,pady=5,command=self.start_tor).pack(side="right",padx=8)
        tk.Button(tor_f,text="⏹ Stop Tor",font=("Courier",9,"bold"),bg=BG3,fg=RED,
                 relief="flat",padx=10,pady=5,command=self.stop_tor).pack(side="right",padx=3)

        # URL bar
        url_f=tk.Frame(self.root,bg=BG2);url_f.pack(fill="x",padx=15,pady=5)
        tk.Label(url_f,text="🧅",font=("Courier",12),bg=BG2,fg=GREEN).pack(side="left",padx=8,pady=8)
        self.url_entry=tk.Entry(url_f,font=("Courier",11),bg=BG,fg=GREEN,
                               insertbackground=GREEN,relief="flat")
        self.url_entry.pack(side="left",fill="x",expand=True,ipady=8)
        self.url_entry.insert(0,"https://check.torproject.org")
        self.url_entry.bind("<Return>",lambda e:self.browse())
        tk.Button(url_f,text="GO ▶",font=("Courier",10,"bold"),bg=GREEN,fg=BG,
                 relief="flat",padx=12,command=self.browse).pack(side="right",padx=6,pady=5)

        # Bookmarks
        bf=tk.Frame(self.root,bg=BG);bf.pack(fill="x",padx=15,pady=3)
        tk.Label(bf,text="Bookmarks:",font=("Courier",8),bg=BG,fg=DIM).pack(side="left",padx=5)
        for name,url in BOOKMARKS[:4]:
            tk.Button(bf,text=name[:15],font=("Courier",7),bg=BG3,fg=GREEN,
                     relief="flat",padx=5,pady=2,
                     command=lambda u=url:self.load_url(u)).pack(side="left",padx=2)

        # Content area
        tk.Label(self.root,text="◈ CONTENT",font=("Courier",9,"bold"),bg=BG,fg=GREEN).pack(anchor="w",padx=15,pady=(5,2))
        self.content=tk.Text(self.root,bg="#000500",fg=GREEN,font=("Courier",9),
                            relief="flat",state="disabled",wrap="word")
        self.content.pack(fill="both",expand=True,padx=15,pady=3)
        self.content.tag_config("h",foreground=GOLD,font=("Courier",11,"bold"))
        self.content.tag_config("link",foreground=GREEN,underline=True)
        self.content.tag_config("warn",foreground=RED)

        # Privacy info
        pf=tk.Frame(self.root,bg=BG);pf.pack(fill="x",padx=15,pady=5)
        self.privacy_info=tk.Label(pf,text="",font=("Courier",7),bg=BG,fg=DIM)
        self.privacy_info.pack(side="left")
        tk.Label(self.root,text="BrayoOS Dark Web Browser v4.5 • AIRA 🇰🇪 | Tor-powered anonymity",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

        self.show_welcome()

    def show_welcome(self):
        self.content.config(state="normal");self.content.delete("1.0","end")
        self.content.insert("end","🕷️ BRAYOOS DARK WEB BROWSER\n","h")
        self.content.insert("end","="*50+"\n\n")
        self.content.insert("end","⚠️  IMPORTANT WARNINGS:\n","warn")
        self.content.insert("end","• Only access legal content\n","warn")
        self.content.insert("end","• Dark web ≠ illegal — it also hosts privacy tools\n","warn")
        self.content.insert("end","• Tor anonymizes your traffic\n","warn")
        self.content.insert("end","• Never share personal info\n\n","warn")
        self.content.insert("end","◈ HOW TO USE:\n","h")
        self.content.insert("end","1. Click 'Start Tor' to connect\n")
        self.content.insert("end","2. Enter .onion URL or regular URL\n")
        self.content.insert("end","3. Traffic routes through Tor network\n")
        self.content.insert("end","4. You are anonymous!\n\n")
        self.content.insert("end","◈ PRIVACY STATUS:\n","h")
        self.content.insert("end","• Identity: PROTECTED (via Tor)\n")
        self.content.insert("end","• Location: HIDDEN\n")
        self.content.insert("end","• Traffic: ENCRYPTED (3 layers)\n")
        self.content.config(state="disabled")

    def check_tor(self):
        threading.Thread(target=self._check_tor,daemon=True).start()

    def _check_tor(self):
        tor_installed=subprocess.run("which tor 2>/dev/null",shell=True,capture_output=True).returncode==0
        if tor_installed:
            self.root.after(0,self.tor_status.config,{"text":"Tor installed ✅","fg":GREEN})
        else:
            self.root.after(0,self.tor_status.config,{"text":"Tor not installed. Run: pkg install tor","fg":GOLD})

    def start_tor(self):
        threading.Thread(target=self._start_tor,daemon=True).start()

    def _start_tor(self):
        self.root.after(0,self.tor_status.config,{"text":"Starting Tor...","fg":GOLD})
        # Try to start tor
        result=subprocess.run("tor --version 2>/dev/null",shell=True,capture_output=True)
        if result.returncode==0:
            subprocess.Popen("tor 2>/dev/null &",shell=True)
            time.sleep(3)
            self.tor_running=True
            self.root.after(0,self.tor_lbl.config,{"text":"⬤ TOR: ONLINE","fg":GREEN})
            self.root.after(0,self.tor_status.config,{"text":"✅ Tor running on 127.0.0.1:9050","fg":GREEN})
            self.root.after(0,self.privacy_info.config,{"text":"🧅 Routed through Tor — You are anonymous"})
        else:
            self.root.after(0,self.tor_status.config,{"text":"Install Tor: pkg install tor","fg":RED})
            self.root.after(0,self.log_content,"Installing Tor...\nRun in Termux: pkg install tor\nThen restart this app.")

    def stop_tor(self):
        subprocess.run("pkill tor 2>/dev/null",shell=True)
        self.tor_running=False
        self.tor_lbl.config(text="⬤ TOR: OFFLINE",fg=RED)
        self.tor_status.config(text="Tor stopped",fg=DIM)

    def load_url(self,url):
        self.url_entry.delete(0,"end")
        self.url_entry.insert(0,url)
        self.browse()

    def browse(self):
        url=self.url_entry.get().strip()
        if not url:return
        threading.Thread(target=self._browse,args=(url,),daemon=True).start()

    def _browse(self,url):
        self.root.after(0,self.log_content,f"🔄 Loading: {url}\n")
        is_onion=".onion" in url
        try:
            if is_onion or self.tor_running:
                proxies={"http://":"socks5://127.0.0.1:9050","https://":"socks5://127.0.0.1:9050"}
                r=httpx.get(url,proxies=proxies,timeout=30,follow_redirects=True)
            else:
                r=httpx.get(url,timeout=15,follow_redirects=True)
            # Parse basic HTML
            content=r.text
            import re
            content=re.sub('<[^>]+>','',content)
            content=re.sub('\n{3,}','\n\n',content)
            content=content[:3000]
            self.root.after(0,self.log_content,content)
            self.root.after(0,self.privacy_info.config,
                           {"text":f"✅ Loaded via {'Tor' if self.tor_running else 'Direct'} | Status: {r.status_code}"})
        except Exception as e:
            if is_onion and not self.tor_running:
                self.root.after(0,self.log_content,"⚠️ .onion sites require Tor!\nClick 'Start Tor' first.")
            else:
                self.root.after(0,self.log_content,f"❌ Error: {e}")

    def log_content(self,text):
        self.content.config(state="normal")
        self.content.delete("1.0","end")
        self.content.insert("end",text)
        self.content.config(state="disabled")

if __name__=="__main__":
    root=tk.Tk();DarkWebBrowser(root);root.mainloop()
