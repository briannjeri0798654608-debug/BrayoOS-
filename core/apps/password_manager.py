import tkinter as tk
import threading,os,json,hashlib,secrets,string,pyperclip
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

PASS_FILE=os.path.expanduser("~/BrayoOS/memory/passwords.json")
os.makedirs(os.path.dirname(PASS_FILE),exist_ok=True)

class PasswordManager:
    def __init__(self,root):
        self.root=root
        self.root.title("🔑 Password Manager")
        self.root.geometry("680x580")
        self.root.configure(bg=BG)
        self.passwords=self.load()
        self.build_ui()

    def load(self):
        if os.path.exists(PASS_FILE):
            with open(PASS_FILE) as f:return json.load(f)
        return []

    def save(self):
        with open(PASS_FILE,"w") as f:json.dump(self.passwords,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=46)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="🔑 PASSWORD MANAGER",font=("Courier",14,"bold"),bg=BG2,fg=GOLD).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="Generate • Store • Protect",font=("Courier",8),bg=BG2,fg=DIM).pack(side="left")
        tk.Frame(self.root,bg=GOLD,height=2).pack(fill="x")

        main=tk.Frame(self.root,bg=BG);main.pack(fill="both",expand=True,padx=10,pady=8)
        left=tk.Frame(main,bg=BG);left.pack(side="left",fill="both",expand=True,padx=(0,8))
        right=tk.Frame(main,bg=BG2,width=220);right.pack(side="left",fill="y")
        right.pack_propagate(False)

        # Generator
        tk.Label(left,text="◈ PASSWORD GENERATOR",font=("Courier",9,"bold"),bg=BG,fg=GOLD).pack(anchor="w")
        gf=tk.Frame(left,bg=BG3);gf.pack(fill="x",pady=3)

        # Options
        opts=tk.Frame(gf,bg=BG3);opts.pack(fill="x",padx=8,pady=5)
        self.use_upper=tk.BooleanVar(value=True)
        self.use_lower=tk.BooleanVar(value=True)
        self.use_digits=tk.BooleanVar(value=True)
        self.use_symbols=tk.BooleanVar(value=True)
        for text,var in [("ABC Uppercase",self.use_upper),("abc Lowercase",self.use_lower),
                         ("123 Numbers",self.use_digits),("!@# Symbols",self.use_symbols)]:
            tk.Checkbutton(opts,text=text,variable=var,bg=BG3,fg=NEON,
                          selectcolor=PURPLE,activebackground=BG3,
                          font=("Courier",8)).pack(side="left",padx=8)

        # Length
        lf=tk.Frame(gf,bg=BG3);lf.pack(fill="x",padx=8,pady=3)
        tk.Label(lf,text="Length:",font=("Courier",9),bg=BG3,fg=DIM).pack(side="left")
        self.length_var=tk.IntVar(value=16)
        tk.Scale(lf,from_=8,to=64,orient="horizontal",variable=self.length_var,
                bg=BG3,fg=GOLD,troughcolor=BG,highlightthickness=0,length=300).pack(side="left",padx=10)
        self.len_lbl=tk.Label(lf,text="16",font=("Courier",10,"bold"),bg=BG3,fg=GOLD)
        self.len_lbl.pack(side="left")
        self.length_var.trace("w",lambda *a:self.len_lbl.config(text=str(self.length_var.get())))

        # Generated password display
        self.gen_pass=tk.Entry(gf,font=("Courier",14),bg=BG,fg=GREEN,
                              insertbackground=NEON,relief="flat",justify="center")
        self.gen_pass.pack(fill="x",padx=8,pady=5,ipady=10)

        # Strength bar
        self.strength_c=tk.Canvas(gf,width=580,height=8,bg="#001100",highlightthickness=0)
        self.strength_c.pack(padx=8,pady=2)
        self.strength_lbl=tk.Label(gf,text="",font=("Courier",7),bg=BG3,fg=DIM)
        self.strength_lbl.pack(anchor="w",padx=8,pady=(0,5))

        bf=tk.Frame(gf,bg=BG3);bf.pack(fill="x",padx=8,pady=5)
        tk.Button(bf,text="⚡ GENERATE",font=("Courier",10,"bold"),bg=GOLD,fg=BG,
                 relief="flat",padx=12,pady=5,command=self.generate).pack(side="left",padx=3)
        tk.Button(bf,text="📋 Copy",font=("Courier",9),bg=BG3,fg=GREEN,
                 relief="flat",padx=8,pady=5,command=self.copy_pass).pack(side="left",padx=3)

        # Save form
        tk.Label(left,text="◈ SAVE PASSWORD",font=("Courier",9,"bold"),bg=BG,fg=GOLD).pack(anchor="w",pady=(8,2))
        sf=tk.Frame(left,bg=BG3);sf.pack(fill="x",pady=3)
        self.save_fields={}
        for label,default in [("Website/App","github.com"),("Username","brayo"),("Notes","")]:
            row=tk.Frame(sf,bg=BG3);row.pack(fill="x",padx=8,pady=3)
            tk.Label(row,text=f"{label}:",font=("Courier",8),bg=BG3,fg=DIM,width=12,anchor="w").pack(side="left")
            e=tk.Entry(row,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
            e.insert(0,default);e.pack(side="left",fill="x",expand=True,ipady=5)
            self.save_fields[label]=e
        tk.Button(sf,text="💾 Save Password",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=12,pady=5,command=self.save_password).pack(pady=6)

        # Right — saved passwords
        tk.Label(right,text="◈ SAVED PASSWORDS",font=("Courier",8,"bold"),bg=BG2,fg=GOLD).pack(pady=6,padx=8,anchor="w")
        tk.Label(right,text=f"Total: {len(self.passwords)}",font=("Courier",7),bg=BG2,fg=DIM).pack(padx=8,anchor="w")

        self.pass_list=tk.Listbox(right,bg=BG2,fg=WHITE,font=("Courier",7),
                                  selectbackground=PURPLE,relief="flat")
        self.pass_list.pack(fill="both",expand=True,padx=5,pady=5)
        self.pass_list.bind("<<ListboxSelect>>",self.show_password)
        self.render_passwords()

        self.pass_detail=tk.Text(right,height=5,bg=BG3,fg=WHITE,font=("Courier",7),
                                relief="flat",state="disabled")
        self.pass_detail.pack(fill="x",padx=5,pady=3)

        bf2=tk.Frame(right,bg=BG2);bf2.pack(pady=5)
        tk.Button(bf2,text="📋",font=("Courier",10),bg=BG3,fg=GREEN,relief="flat",
                 padx=8,command=self.copy_saved).pack(side="left",padx=2)
        tk.Button(bf2,text="🗑",font=("Courier",10),bg=BG3,fg=RED,relief="flat",
                 padx=8,command=self.delete_password).pack(side="left",padx=2)

        tk.Label(self.root,text="BrayoOS Password Manager v4.5 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)
        self.generate()

    def generate(self):
        chars=""
        if self.use_upper.get():chars+=string.ascii_uppercase
        if self.use_lower.get():chars+=string.ascii_lowercase
        if self.use_digits.get():chars+=string.digits
        if self.use_symbols.get():chars+="!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not chars:chars=string.ascii_letters+string.digits
        length=self.length_var.get()
        password="".join(secrets.choice(chars) for _ in range(length))
        self.gen_pass.delete(0,"end")
        self.gen_pass.insert(0,password)
        self._check_strength(password)

    def _check_strength(self,pwd):
        score=0
        if len(pwd)>=8:score+=20
        if len(pwd)>=16:score+=20
        if any(c.isupper() for c in pwd):score+=15
        if any(c.islower() for c in pwd):score+=15
        if any(c.isdigit() for c in pwd):score+=15
        if any(c in "!@#$%^&*()" for c in pwd):score+=15
        color=RED if score<40 else GOLD if score<70 else GREEN
        label="WEAK" if score<40 else "MEDIUM" if score<70 else "STRONG" if score<90 else "UNBREAKABLE"
        self.strength_c.delete("all")
        w=int(580*score/100)
        if w>0:self.strength_c.create_rectangle(0,0,w,8,fill=color,outline="")
        self.strength_lbl.config(text=f"Strength: {label} ({score}%) — Est. crack time: {'centuries' if score>80 else 'years' if score>60 else 'days'}",fg=color)

    def copy_pass(self):
        pwd=self.gen_pass.get()
        self.root.clipboard_clear();self.root.clipboard_append(pwd)

    def save_password(self):
        pwd=self.gen_pass.get()
        site=self.save_fields["Website/App"].get()
        user=self.save_fields["Username"].get()
        notes=self.save_fields["Notes"].get()
        if not pwd or not site:return
        entry={"site":site,"user":user,"pass":pwd,"notes":notes,
               "date":datetime.now().strftime("%Y-%m-%d")}
        self.passwords.append(entry)
        self.save();self.render_passwords()

    def render_passwords(self):
        self.pass_list.delete(0,"end")
        for p in self.passwords:
            self.pass_list.insert("end",f"  🔑 {p['site'][:20]}")

    def show_password(self,e):
        sel=self.pass_list.curselection()
        if not sel or sel[0]>=len(self.passwords):return
        p=self.passwords[sel[0]]
        self.pass_detail.config(state="normal");self.pass_detail.delete("1.0","end")
        self.pass_detail.insert("end",f"Site: {p['site']}\nUser: {p['user']}\nPass: {p['pass']}\nNotes: {p['notes']}\nDate: {p['date']}")
        self.pass_detail.config(state="disabled")

    def copy_saved(self):
        sel=self.pass_list.curselection()
        if not sel or sel[0]>=len(self.passwords):return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.passwords[sel[0]]["pass"])

    def delete_password(self):
        sel=self.pass_list.curselection()
        if not sel or sel[0]>=len(self.passwords):return
        del self.passwords[sel[0]]
        self.save();self.render_passwords()

if __name__=="__main__":
    root=tk.Tk();PasswordManager(root);root.mainloop()
