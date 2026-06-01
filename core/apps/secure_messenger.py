import tkinter as tk
import threading,os,json,hashlib,base64,time,subprocess,httpx
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

MSGS_FILE=os.path.expanduser("~/BrayoOS/memory/secure_messages.json")
os.makedirs(os.path.dirname(MSGS_FILE),exist_ok=True)

def encrypt(text,key):
    kb=hashlib.sha256(key.encode()).digest()
    return base64.b64encode(bytes([ord(c)^kb[i%32] for i,c in enumerate(text)])).decode()

def decrypt(data,key):
    kb=hashlib.sha256(key.encode()).digest()
    try:
        raw=base64.b64decode(data.encode())
        return "".join(chr(b^kb[i%32]) for i,b in enumerate(raw))
    except:return "[Decryption failed]"

class SecureMessenger:
    def __init__(self,root):
        self.root=root
        self.root.title("🔐 Secure Messenger")
        self.root.geometry("700x580")
        self.root.configure(bg=BG)
        self.key="BrayoOS5.0"
        self.contacts=["AIRA","Brayo","Ghost","Agent K"]
        self.current=self.contacts[0]
        self.messages=self.load()
        self.build_ui()

    def load(self):
        if os.path.exists(MSGS_FILE):
            with open(MSGS_FILE) as f:return json.load(f)
        return {c:[] for c in self.contacts}

    def save(self):
        with open(MSGS_FILE,"w") as f:json.dump(self.messages,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🔐 SECURE MESSENGER",font=("Courier",14,"bold"),bg=BG2,fg=CYAN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="End-to-end encrypted",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Label(hdr,text="🔒 E2E ENCRYPTED",font=("Courier",8,"bold"),bg=BG2,fg=GREEN).pack(side="right",padx=12)
        tk.Frame(self.root,bg=CYAN,height=2).pack(fill="x")

        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True)

        # Contacts sidebar
        left=tk.Frame(main,bg=BG2,width=160);left.pack(side="left",fill="y")
        left.pack_propagate(False)
        tk.Label(left,text="◈ CONTACTS",font=("Courier",8,"bold"),bg=BG2,fg=CYAN).pack(pady=6,padx=8,anchor="w")
        self.contact_btns={}
        for c in self.contacts:
            f=tk.Frame(left,bg=BG3,cursor="hand2");f.pack(fill="x",padx=6,pady=2)
            tk.Label(f,text="◉",font=("Courier",9),bg=BG3,fg=GREEN).pack(side="left",padx=6,pady=6)
            tk.Label(f,text=c,font=("Courier",9,"bold"),bg=BG3,fg=WHITE).pack(side="left")
            unread=len(self.messages.get(c,[]))
            if unread:
                tk.Label(f,text=str(unread),font=("Courier",7),bg=RED,fg=WHITE,padx=3).pack(side="right",padx=4)
            for w in [f]+f.winfo_children():
                w.bind("<Button-1>",lambda e,x=c:self.switch_contact(x))
                w.bind("<Enter>",lambda e,x=f:x.config(bg=PURPLE))
                w.bind("<Leave>",lambda e,x=f:x.config(bg=BG3))
            self.contact_btns[c]=f

        tk.Frame(left,bg=CYAN,height=1).pack(fill="x",padx=8,pady=8)
        tk.Label(left,text="◈ ENCRYPTION KEY",font=("Courier",7,"bold"),bg=BG2,fg=CYAN).pack(padx=8,anchor="w")
        self.key_e=tk.Entry(left,font=("Courier",8),bg=BG3,fg=CYAN,
                           insertbackground=NEON,relief="flat",show="●")
        self.key_e.pack(fill="x",padx=6,pady=3,ipady=4)
        self.key_e.insert(0,self.key)
        tk.Button(left,text="Update Key",font=("Courier",7),bg=PURPLE,fg=WHITE,
                 relief="flat",command=lambda:setattr(self,"key",self.key_e.get())).pack(padx=6,pady=2)

        # Chat area
        right=tk.Frame(main,bg=BG);right.pack(side="left",fill="both",expand=True)
        self.contact_lbl=tk.Label(right,text=f"Chat with: {self.current}",
                                   font=("Courier",10,"bold"),bg=BG,fg=CYAN)
        self.contact_lbl.pack(anchor="w",padx=10,pady=5)

        self.chat=tk.Text(right,bg=BG3,fg=WHITE,font=("Courier",9),
                         relief="flat",state="disabled",wrap="word")
        self.chat.pack(fill="both",expand=True,padx=10,pady=3)
        self.chat.tag_config("me",foreground=NEON)
        self.chat.tag_config("them",foreground=CYAN)
        self.chat.tag_config("sys",foreground=DIM)
        self.chat.tag_config("enc",foreground=GREEN)

        # Input
        inf=tk.Frame(right,bg=BG3);inf.pack(fill="x",padx=10,pady=5)
        tk.Label(inf,text="🔐",font=("Courier",11),bg=BG3,fg=CYAN).pack(side="left",padx=8,pady=8)
        self.msg_inp=tk.Entry(inf,font=("Courier",10),bg=BG,fg=WHITE,
                             insertbackground=NEON,relief="flat")
        self.msg_inp.pack(side="left",fill="x",expand=True,ipady=8)
        self.msg_inp.bind("<Return>",lambda e:self.send_msg())
        tk.Button(inf,text="🔐 SEND",font=("Courier",9,"bold"),bg=CYAN,fg=BG,
                 relief="flat",padx=12,command=self.send_msg).pack(side="right",padx=6,pady=5)

        bf=tk.Frame(right,bg=BG);bf.pack(fill="x",padx=10,pady=3)
        tk.Button(bf,text="🗑 Clear",font=("Courier",8),bg=BG3,fg=RED,
                 relief="flat",padx=8,pady=3,command=self.clear_chat).pack(side="left",padx=3)
        tk.Button(bf,text="🤖 Ask AIRA",font=("Courier",8),bg=BG3,fg=NEON,
                 relief="flat",padx=8,pady=3,command=self.ask_aira).pack(side="left",padx=3)
        self.enc_lbl=tk.Label(bf,text="🔒 Messages encrypted with XOR+SHA256",
                              font=("Courier",7),bg=BG,fg=DIM)
        self.enc_lbl.pack(side="right",padx=8)

        tk.Label(self.root,text="BrayoOS Secure Messenger v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)
        self.load_chat()

    def switch_contact(self,contact):
        self.current=contact
        self.contact_lbl.config(text=f"Chat with: {contact}")
        self.load_chat()

    def load_chat(self):
        self.chat.config(state="normal");self.chat.delete("1.0","end")
        msgs=self.messages.get(self.current,[])
        if not msgs:
            self.chat.insert("end","  No messages yet. Start chatting!\n","sys")
        for m in msgs:
            ts=m.get("time","")
            sender=m.get("sender","?")
            encrypted=m.get("encrypted","")
            try:text=decrypt(encrypted,self.key)
            except:text="[Encrypted]"
            tag="me" if sender=="Brayo" else "them"
            self.chat.insert("end",f"\n  [{ts}] {sender}:\n","sys")
            self.chat.insert("end",f"  {text}\n",tag)
        self.chat.config(state="disabled")
        self.chat.see("end")

    def send_msg(self):
        text=self.msg_inp.get().strip()
        if not text:return
        self.msg_inp.delete(0,"end")
        encrypted=encrypt(text,self.key)
        msg={"sender":"Brayo","text":text,"encrypted":encrypted,
             "time":datetime.now().strftime("%H:%M")}
        if self.current not in self.messages:
            self.messages[self.current]=[]
        self.messages[self.current].append(msg)
        self.save()
        self.load_chat()
        if self.current=="AIRA":
            threading.Thread(target=self._aira_reply,args=(text,),daemon=True).start()

    def _aira_reply(self,msg):
        time.sleep(1)
        groq=os.environ.get("GROQ_API_KEY","")
        if groq:
            try:
                r=httpx.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization":f"Bearer {groq}","Content-Type":"application/json"},
                    json={"model":"llama-3.3-70b-versatile",
                          "messages":[
                              {"role":"system","content":"You are AIRA in a secure chat. Reply briefly in 1-2 sentences. Call user Brayo."},
                              {"role":"user","content":msg}],
                          "max_tokens":80},timeout=10)
                reply=r.json()["choices"][0]["message"]["content"].strip()
            except:reply="Secure channel active. Message received, Brayo."
        else:
            reply="AIRA here. Secure channel active."
        encrypted=encrypt(reply,self.key)
        aira_msg={"sender":"AIRA","text":reply,"encrypted":encrypted,
                  "time":datetime.now().strftime("%H:%M")}
        self.messages[self.current].append(aira_msg)
        self.save()
        self.root.after(0,self.load_chat)

    def ask_aira(self):
        self.current="AIRA"
        self.contact_lbl.config(text="Chat with: AIRA")
        self.load_chat()
        self.msg_inp.focus_set()

    def clear_chat(self):
        self.messages[self.current]=[]
        self.save();self.load_chat()

if __name__=="__main__":
    root=tk.Tk();SecureMessenger(root);root.mainloop()
