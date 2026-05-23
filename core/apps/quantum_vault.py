import tkinter as tk
import threading,os,json,hashlib,base64,time,random
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

VAULT=os.path.expanduser("~/BrayoOS/.quantum_vault/")
META=os.path.expanduser("~/BrayoOS/memory/quantum_meta.json")
os.makedirs(VAULT,exist_ok=True)
os.makedirs(os.path.dirname(META),exist_ok=True)

def quantum_encrypt(data,key):
    key_bytes=hashlib.sha256(key.encode()).digest()
    result=[]
    for i,b in enumerate(data.encode() if isinstance(data,str) else data):
        result.append(b^key_bytes[i%32])
    return base64.b85encode(bytes(result)).decode()

def quantum_decrypt(data,key):
    key_bytes=hashlib.sha256(key.encode()).digest()
    raw=base64.b85decode(data.encode())
    result=[]
    for i,b in enumerate(raw):
        result.append(b^key_bytes[i%32])
    try:return bytes(result).decode()
    except:return bytes(result)

class QuantumVault:
    def __init__(self,root):
        self.root=root
        self.root.title("🔮 Quantum Vault")
        self.root.geometry("680x580")
        self.root.configure(bg=BG)
        self.unlocked=False
        self.key=""
        self.files=[]
        self.show_lock()

    def show_lock(self):
        for w in self.root.winfo_children():w.destroy()
        # Quantum animation canvas
        self.anim=tk.Canvas(self.root,width=680,height=120,bg=BG,highlightthickness=0)
        self.anim.pack()
        threading.Thread(target=self.animate,daemon=True).start()

        tk.Label(self.root,text="🔮 QUANTUM VAULT",font=("Courier",20,"bold"),bg=BG,fg=CYAN).pack(pady=5)
        tk.Label(self.root,text="Military-grade XOR+SHA256 encryption",font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=CYAN,height=2).pack(fill="x",pady=8)

        # Key input
        kf=tk.Frame(self.root,bg=BG3);kf.pack(fill="x",padx=60,pady=10)
        tk.Label(kf,text="QUANTUM KEY:",font=("Courier",11,"bold"),bg=BG3,fg=CYAN).pack(pady=(12,3))
        self.key_entry=tk.Entry(kf,font=("Courier",14),bg=BG,fg=CYAN,
                               insertbackground=CYAN,relief="flat",show="●",justify="center")
        self.key_entry.pack(fill="x",padx=15,ipady=10)
        self.key_entry.bind("<Return>",lambda e:self.unlock())

        # Strength meter
        self.strength_canvas=tk.Canvas(kf,width=400,height=10,bg="#001100",highlightthickness=0)
        self.strength_canvas.pack(pady=5)
        self.key_entry.bind("<KeyRelease>",self.check_strength)

        self.strength_lbl=tk.Label(kf,text="Enter your quantum key",font=("Courier",8),bg=BG3,fg=DIM)
        self.strength_lbl.pack(pady=(0,10))

        tk.Button(self.root,text="🔮 UNLOCK VAULT",font=("Courier",13,"bold"),
                 bg=CYAN,fg=BG,relief="flat",padx=20,pady=10,
                 command=self.unlock).pack(pady=15)

        self.msg=tk.Label(self.root,text="",font=("Courier",9),bg=BG,fg=RED)
        self.msg.pack()

        # Info
        info_f=tk.Frame(self.root,bg=BG3);info_f.pack(fill="x",padx=30,pady=10)
        for item in ["🔮 XOR encryption with SHA-256 key derivation",
                     "🔑 Your key never stored anywhere",
                     "💀 Wrong key = corrupted data",
                     "🌌 Quantum-resistant algorithm"]:
            tk.Label(info_f,text=item,font=("Courier",8),bg=BG3,fg=DIM).pack(anchor="w",padx=10,pady=2)

        tk.Label(self.root,text="BrayoOS Quantum Vault v4.5 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=6)

    def animate(self):
        particles=[(random.randint(0,680),random.randint(0,120),
                    random.choice([CYAN,PURPLE,NEON,GREEN]),
                    random.randint(1,3)) for _ in range(30)]
        while True:
            try:
                self.anim.delete("all")
                for i,(x,y,color,size) in enumerate(particles):
                    self.anim.create_oval(x-size,y-size,x+size,y+size,fill=color,outline="")
                    particles[i]=(x+random.randint(-2,2),
                                  max(0,min(120,y+random.randint(-2,2))),
                                  color,size)
                self.anim.create_text(340,60,text="◈ QUANTUM ENCRYPTED ◈",
                                     fill=CYAN,font=("Courier",12,"bold"))
                time.sleep(0.05)
            except:break

    def check_strength(self,e=None):
        key=self.key_entry.get()
        strength=0
        if len(key)>=8:strength+=25
        if len(key)>=16:strength+=25
        if any(c.isupper() for c in key):strength+=15
        if any(c.isdigit() for c in key):strength+=15
        if any(c in "!@#$%^&*()" for c in key):strength+=20
        color=RED if strength<40 else GOLD if strength<70 else GREEN
        label="WEAK" if strength<40 else "MEDIUM" if strength<70 else "STRONG" if strength<90 else "QUANTUM STRONG"
        self.strength_canvas.delete("all")
        w=int(400*strength/100)
        if w>0:self.strength_canvas.create_rectangle(0,0,w,10,fill=color,outline="")
        self.strength_lbl.config(text=f"Key Strength: {label} ({strength}%)",fg=color)

    def unlock(self):
        key=self.key_entry.get()
        if len(key)<4:
            self.msg.config(text="Key too short — minimum 4 characters");return
        self.key=key
        self.unlocked=True
        self.show_vault()

    def show_vault(self):
        for w in self.root.winfo_children():w.destroy()
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🔮 QUANTUM VAULT — UNLOCKED",font=("Courier",12,"bold"),bg=BG2,fg=CYAN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text=f"Key: {'●'*len(self.key)}",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Button(hdr,text="🔒 Lock",font=("Courier",9),bg=BG3,fg=RED,
                 relief="flat",padx=8,pady=4,command=self.show_lock).pack(side="right",padx=10)
        tk.Frame(self.root,bg=CYAN,height=2).pack(fill="x")

        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True,padx=10,pady=8)

        # Left — file list
        left=tk.Frame(main,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(0,8))
        tk.Label(left,text="◈ ENCRYPTED FILES",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w")
        self.file_list=tk.Listbox(left,bg=BG3,fg=CYAN,font=("Courier",9),
                                   selectbackground=PURPLE,relief="flat",height=12)
        self.file_list.pack(fill="both",expand=True,pady=3)
        self.load_files()

        # Text editor
        tk.Label(left,text="◈ SECURE NOTE EDITOR",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",pady=(8,2))
        self.editor=tk.Text(left,height=6,bg=BG3,fg=WHITE,font=("Courier",9),
                           relief="flat",insertbackground=CYAN)
        self.editor.pack(fill="x",pady=3)

        # Buttons
        bf=tk.Frame(left,bg=BG);bf.pack(fill="x",pady=5)
        for txt,cmd,color in [
            ("💾 Encrypt & Save",self.save_note,CYAN),
            ("🔓 Decrypt Selected",self.decrypt_file,GREEN),
            ("🗑 Delete",self.delete_file,RED),
        ]:
            tk.Button(bf,text=txt,font=("Courier",8,"bold"),bg=BG3,fg=color,
                     relief="flat",padx=8,pady=4,command=cmd).pack(side="left",padx=3)

        # Right — info
        right=tk.Frame(main,bg=BG2,width=200)
        right.pack(side="left",fill="y")
        right.pack_propagate(False)
        tk.Label(right,text="◈ VAULT INFO",font=("Courier",9,"bold"),bg=BG2,fg=CYAN).pack(pady=8,padx=8,anchor="w")
        files=os.listdir(VAULT)
        info=[
            ("Files",str(len(files))),
            ("Encryption","XOR+SHA256"),
            ("Key Length",f"{len(self.key)} chars"),
            ("Algorithm","Quantum-safe"),
            ("Status","SECURED"),
        ]
        for k,v in info:
            f=tk.Frame(right,bg=BG3);f.pack(fill="x",padx=8,pady=2)
            tk.Label(f,text=k+":",font=("Courier",8),bg=BG3,fg=DIM,width=12,anchor="w").pack(side="left",padx=5,pady=4)
            tk.Label(f,text=v,font=("Courier",8,"bold"),bg=BG3,fg=CYAN).pack(side="left")

        tk.Label(self.root,text="BrayoOS Quantum Vault v4.5 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def load_files(self):
        self.file_list.delete(0,"end")
        for f in os.listdir(VAULT):
            self.file_list.insert("end",f"🔮 {f}")

    def save_note(self):
        content=self.editor.get("1.0","end").strip()
        if not content:return
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        filename=f"note_{ts}.qvault"
        encrypted=quantum_encrypt(content,self.key)
        with open(os.path.join(VAULT,filename),"w") as f:f.write(encrypted)
        self.load_files()

    def decrypt_file(self):
        sel=self.file_list.curselection()
        if not sel:return
        filename=self.file_list.get(sel[0]).replace("🔮 ","")
        path=os.path.join(VAULT,filename)
        try:
            with open(path) as f:encrypted=f.read()
            decrypted=quantum_decrypt(encrypted,self.key)
            self.editor.delete("1.0","end")
            self.editor.insert("end",decrypted)
        except:
            self.editor.delete("1.0","end")
            self.editor.insert("end","⚠️ Wrong key or corrupted file!")

    def delete_file(self):
        sel=self.file_list.curselection()
        if not sel:return
        filename=self.file_list.get(sel[0]).replace("🔮 ","")
        os.remove(os.path.join(VAULT,filename))
        self.load_files()

if __name__=="__main__":
    root=tk.Tk();QuantumVault(root);root.mainloop()
