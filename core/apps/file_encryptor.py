import tkinter as tk
from tkinter import filedialog
import threading,os,hashlib,base64,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
CYAN="#44FFFF"

class FileEncryptor:
    def __init__(self,root):
        self.root=root
        self.root.title("🔐 File Encryptor")
        self.root.geometry("620x520")
        self.root.configure(bg=BG)
        self.files=[]
        self.build_ui()

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🔐 FILE ENCRYPTOR",font=("Courier",14,"bold"),bg=BG2,fg=CYAN).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="Encrypt any file with XOR+SHA256",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Frame(self.root,bg=CYAN,height=2).pack(fill="x")

        # Key
        kf=tk.Frame(self.root,bg=BG3);kf.pack(fill="x",padx=15,pady=8)
        tk.Label(kf,text="🔑 ENCRYPTION KEY:",font=("Courier",10,"bold"),bg=BG3,fg=CYAN).pack(side="left",padx=10,pady=8)
        self.key_e=tk.Entry(kf,font=("Courier",12),bg=BG,fg=CYAN,
                           insertbackground=CYAN,relief="flat",show="●",width=25)
        self.key_e.pack(side="left",ipady=8,padx=5)
        self.key_e.insert(0,"BrayoOS1337")
        tk.Button(kf,text="👁",font=("Courier",10),bg=BG3,fg=DIM,relief="flat",
                 command=lambda:self.key_e.config(show="" if self.key_e.cget("show")=="●" else "●")).pack(side="left")

        # File list
        tk.Label(self.root,text="◈ FILES TO PROCESS",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(5,2))
        list_f=tk.Frame(self.root,bg=BG3);list_f.pack(fill="x",padx=15,pady=3)
        self.file_list=tk.Listbox(list_f,bg=BG3,fg=WHITE,font=("Courier",9),
                                   selectbackground=PURPLE,relief="flat",height=6)
        self.file_list.pack(fill="x",padx=5,pady=5)

        bf=tk.Frame(self.root,bg=BG);bf.pack(fill="x",padx=15,pady=3)
        tk.Button(bf,text="📂 Add Files",font=("Courier",9),bg=BG3,fg=CYAN,
                 relief="flat",padx=10,pady=4,command=self.add_files).pack(side="left",padx=3)
        tk.Button(bf,text="📁 Add Folder",font=("Courier",9),bg=BG3,fg=NEON,
                 relief="flat",padx=10,pady=4,command=self.add_folder).pack(side="left",padx=3)
        tk.Button(bf,text="🗑 Remove",font=("Courier",9),bg=BG3,fg=RED,
                 relief="flat",padx=10,pady=4,command=self.remove_file).pack(side="left",padx=3)

        # Progress
        tk.Label(self.root,text="◈ PROGRESS",font=("Courier",9,"bold"),bg=BG,fg=CYAN).pack(anchor="w",padx=15,pady=(8,2))
        self.progress_c=tk.Canvas(self.root,width=580,height=12,bg="#001100",highlightthickness=0)
        self.progress_c.pack(padx=15,pady=3)
        self.progress_lbl=tk.Label(self.root,text="Ready",font=("Courier",8),bg=BG,fg=DIM)
        self.progress_lbl.pack()

        # Log
        self.log_box=tk.Text(self.root,height=7,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=5)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("c",foreground=CYAN)

        # Action buttons
        abf=tk.Frame(self.root,bg=BG);abf.pack(pady=6)
        tk.Button(abf,text="🔒 ENCRYPT ALL",font=("Courier",11,"bold"),bg=CYAN,fg=BG,
                 relief="flat",padx=15,pady=7,command=lambda:self.process("encrypt")).pack(side="left",padx=5)
        tk.Button(abf,text="🔓 DECRYPT ALL",font=("Courier",11,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=15,pady=7,command=lambda:self.process("decrypt")).pack(side="left",padx=5)
        tk.Label(self.root,text="BrayoOS File Encryptor v4.5 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def log(self,msg,tag="c"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def add_files(self):
        paths=filedialog.askopenfilenames()
        for p in paths:
            if p not in self.files:
                self.files.append(p)
                self.file_list.insert("end",f"  📄 {os.path.basename(p)}")

    def add_folder(self):
        folder=filedialog.askdirectory()
        if folder:
            for f in os.listdir(folder):
                path=os.path.join(folder,f)
                if os.path.isfile(path) and path not in self.files:
                    self.files.append(path)
                    self.file_list.insert("end",f"  📄 {f}")

    def remove_file(self):
        sel=self.file_list.curselection()
        if sel:
            self.file_list.delete(sel[0])
            del self.files[sel[0]]

    def xor_encrypt(self,data,key):
        key_bytes=hashlib.sha256(key.encode()).digest()
        return bytes([b^key_bytes[i%32] for i,b in enumerate(data)])

    def process(self,mode):
        if not self.files:
            self.log("⚠️ Add files first!","r");return
        key=self.key_e.get()
        if not key:
            self.log("⚠️ Enter encryption key!","r");return
        threading.Thread(target=self._process,args=(mode,key),daemon=True).start()

    def _process(self,mode,key):
        total=len(self.files)
        for i,filepath in enumerate(self.files):
            try:
                pct=int((i/total)*100)
                self.root.after(0,self._update_progress,pct,f"Processing: {os.path.basename(filepath)}")
                with open(filepath,"rb") as f:data=f.read()
                if mode=="encrypt":
                    processed=self.xor_encrypt(data,key)
                    out_path=filepath+".brayos"
                    header=b"BRAYOS_ENCRYPTED_V4.5\n"
                    processed=header+base64.b85encode(processed)
                else:
                    if data.startswith(b"BRAYOS_ENCRYPTED_V4.5\n"):
                        encrypted=base64.b85decode(data[22:])
                        processed=self.xor_encrypt(encrypted,key)
                        out_path=filepath.replace(".brayos","")
                    else:
                        self.root.after(0,self.log,f"  ⚠️ Not encrypted: {os.path.basename(filepath)}","r")
                        continue
                with open(out_path,"wb") as f:f.write(processed)
                action="🔒 Encrypted" if mode=="encrypt" else "🔓 Decrypted"
                self.root.after(0,self.log,f"  {action}: {os.path.basename(out_path)}","g")
            except Exception as e:
                self.root.after(0,self.log,f"  ❌ Failed: {os.path.basename(filepath)}: {e}","r")
        self.root.after(0,self._update_progress,100,"Complete!")
        action="Encryption" if mode=="encrypt" else "Decryption"
        self.root.after(0,self.log,f"✅ {action} complete! {total} files processed.","c")

    def _update_progress(self,pct,msg):
        self.progress_c.delete("all")
        w=int(580*pct/100)
        if w>0:self.progress_c.create_rectangle(0,0,w,12,fill=CYAN,outline="")
        self.progress_lbl.config(text=f"{msg} ({pct}%)")

if __name__=="__main__":
    root=tk.Tk();FileEncryptor(root);root.mainloop()
