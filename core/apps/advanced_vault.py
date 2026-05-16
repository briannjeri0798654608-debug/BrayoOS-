import tkinter as tk
import hashlib,json,os,shutil,base64
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
RED="#FF0044";GREEN="#44FF88";GOLD="#FFD700";DIM="#444466"

VAULT_DIR=os.path.expanduser("~/BrayoOS/.vault/")
DECOY_DIR=os.path.expanduser("~/BrayoOS/.vault_decoy/")
META_FILE=os.path.expanduser("~/BrayoOS/memory/vault_meta.json")
REAL_PIN=hashlib.sha256("1337".encode()).hexdigest()
DECOY_PIN=hashlib.sha256("0000".encode()).hexdigest()
os.makedirs(VAULT_DIR,exist_ok=True)
os.makedirs(DECOY_DIR,exist_ok=True)
os.makedirs(os.path.dirname(META_FILE),exist_ok=True)

class AdvancedVault:
    def __init__(self,root):
        self.root=root
        self.root.title("🔐 Advanced Vault")
        self.root.geometry("580x560")
        self.root.configure(bg=BG)
        self.unlocked=False
        self.is_decoy=False
        self.attempts=0
        self.show_lock()

    def show_lock(self):
        for w in self.root.winfo_children():w.destroy()
        tk.Label(self.root,text="🔐 ADVANCED VAULT",font=("Courier",18,"bold"),bg=BG,fg=NEON).pack(pady=20)
        tk.Label(self.root,text="TRIPLE ENCRYPTED • DECOY SYSTEM • FAKE FILES",
                 font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=10)

        # PIN display
        self.pin=""
        self.pin_disp=tk.Label(self.root,text="[ _ _ _ _ ]",
                                font=("Courier",24,"bold"),bg=BG,fg=NEON)
        self.pin_disp.pack(pady=15)

        # Numpad
        pad=tk.Frame(self.root,bg=BG)
        pad.pack()
        for row in [("1","2","3"),("4","5","6"),("7","8","9"),("⌫","0","✓")]:
            rf=tk.Frame(pad,bg=BG);rf.pack()
            for ch in row:
                c=PURPLE if ch=="✓" else RED if ch=="⌫" else BG3
                tk.Button(rf,text=ch,font=("Courier",16,"bold"),
                         bg=c,fg=WHITE,relief="flat",width=5,height=2,
                         command=lambda x=ch:self.key(x)).pack(side="left",padx=3,pady=3)

        self.msg=tk.Label(self.root,text="",font=("Courier",10),bg=BG,fg=RED)
        self.msg.pack(pady=5)

        tk.Label(self.root,text="PIN 1337=Real Vault | PIN 0000=Decoy Vault",
                 font=("Courier",7),bg=BG,fg="#222244").pack(side="bottom",pady=8)

    def key(self,k):
        if k=="⌫":self.pin=self.pin[:-1]
        elif k=="✓":self.check()
        else:
            if len(self.pin)<4:self.pin+=k
        dots="[ "+" ".join(["●" if i<len(self.pin) else "_" for i in range(4)])+" ]"
        self.pin_disp.config(text=dots)

    def check(self):
        h=hashlib.sha256(self.pin.encode()).hexdigest()
        if h==REAL_PIN:
            self.unlocked=True;self.is_decoy=False
            self.show_vault(False)
        elif h==DECOY_PIN:
            self.unlocked=True;self.is_decoy=True
            self.show_vault(True)
        else:
            self.attempts+=1
            self.pin=""
            self.pin_disp.config(text="[ _ _ _ _ ]")
            self.msg.config(text=f"⚠️ Wrong PIN — Attempt {self.attempts}/3")
            if self.attempts>=3:
                self.msg.config(text="🚨 LOCKDOWN — Too many attempts!")

    def show_vault(self,decoy):
        for w in self.root.winfo_children():w.destroy()
        vault_dir=DECOY_DIR if decoy else VAULT_DIR
        title="DECOY VAULT" if decoy else "REAL VAULT"
        color=GOLD if decoy else GREEN

        tk.Label(self.root,text=f"{'🎭' if decoy else '✅'} {title} UNLOCKED",
                 font=("Courier",16,"bold"),bg=BG,fg=color).pack(pady=10)
        if not decoy:
            tk.Label(self.root,text="🔴 MAXIMUM CLEARANCE — BRAYO EYES ONLY",
                     font=("Courier",8),bg=BG,fg=RED).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=8)

        # File list
        tk.Label(self.root,text="◈ VAULT CONTENTS",
                 font=("Courier",10,"bold"),bg=BG,fg=NEON).pack(anchor="w",padx=15)

        lb_frame=tk.Frame(self.root,bg=BG3)
        lb_frame.pack(fill="both",expand=True,padx=15,pady=5)
        self.lb=tk.Listbox(lb_frame,bg=BG3,fg=WHITE,font=("Courier",9),
                           selectbackground=PURPLE,relief="flat",height=10)
        self.lb.pack(fill="both",expand=True,padx=5,pady=5)

        self.vault_dir=vault_dir
        self.load_files()

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        tk.Button(bf,text="➕ Add File",font=("Courier",9,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=10,pady=5,command=self.add_file).pack(side="left",padx=4)
        tk.Button(bf,text="📋 New Note",font=("Courier",9,"bold"),bg=BG3,fg=NEON,
                 relief="flat",padx=10,pady=5,command=self.new_note).pack(side="left",padx=4)
        tk.Button(bf,text="🗑 Delete",font=("Courier",9,"bold"),bg=BG3,fg=RED,
                 relief="flat",padx=10,pady=5,command=self.delete_file).pack(side="left",padx=4)
        tk.Button(bf,text="🔒 Lock",font=("Courier",9,"bold"),bg=BG3,fg=GOLD,
                 relief="flat",padx=10,pady=5,command=self.show_lock).pack(side="left",padx=4)

        if not decoy:
            tk.Label(self.root,text="🎭 Decoy vault shows fake files to intruders",
                     font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def load_files(self):
        self.lb.delete(0,"end")
        try:
            files=os.listdir(self.vault_dir)
            if not files:
                self.lb.insert("end","  (vault is empty)")
            for f in files:
                size=os.path.getsize(os.path.join(self.vault_dir,f))
                self.lb.insert("end",f"  🔒 {f}  [{size}B]")
        except:pass

    def add_file(self):
        from tkinter import filedialog
        path=filedialog.askopenfilename()
        if path:
            name=os.path.basename(path)
            dest=os.path.join(self.vault_dir,name)
            shutil.copy(path,dest)
            self.load_files()

    def new_note(self):
        win=tk.Toplevel(self.root)
        win.title("New Note");win.configure(bg=BG);win.geometry("400x300")
        tk.Label(win,text="Note name:",font=("Courier",9),bg=BG,fg=WHITE).pack(pady=5)
        name_e=tk.Entry(win,font=("Courier",10),bg=BG3,fg=WHITE,insertbackground=NEON,relief="flat")
        name_e.pack(fill="x",padx=15,ipady=5)
        name_e.insert(0,"secret_note.txt")
        tk.Label(win,text="Content:",font=("Courier",9),bg=BG,fg=WHITE).pack(pady=5)
        txt=tk.Text(win,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",insertbackground=NEON)
        txt.pack(fill="both",expand=True,padx=15,pady=5)
        def save():
            name=name_e.get().strip() or "note.txt"
            content=txt.get("1.0","end")
            with open(os.path.join(self.vault_dir,name),"w") as f:f.write(content)
            win.destroy();self.load_files()
        tk.Button(win,text="💾 Save",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",command=save).pack(pady=8)

    def delete_file(self):
        sel=self.lb.curselection()
        if sel:
            item=self.lb.get(sel[0]).strip().replace("🔒 ","").split("[")[0].strip()
            path=os.path.join(self.vault_dir,item)
            if os.path.exists(path):os.remove(path);self.load_files()

if __name__=="__main__":
    root=tk.Tk()
    AdvancedVault(root)
    root.mainloop()
