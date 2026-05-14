import tkinter as tk,json,os
BG="#080810";PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF";BG3="#12122A"
F=os.path.expanduser("~/BrayoOS/memory/contacts.json")
os.makedirs(os.path.dirname(F),exist_ok=True)
class Contacts:
    def __init__(self,r):
        r.title("Contacts");r.geometry("500x500");r.configure(bg=BG)
        tk.Label(r,text="◈ CONTACTS",font=("Courier",13,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Frame(r,bg=PURPLE,height=2).pack(fill="x")
        ff=tk.Frame(r,bg=BG3);ff.pack(fill="x",padx=15,pady=8)
        self.entries={}
        for label in ["Name","Phone","Email"]:
            row=tk.Frame(ff,bg=BG3);row.pack(fill="x",padx=8,pady=3)
            tk.Label(row,text=f"{label}:",font=("Courier",9),bg=BG3,fg=PURPLE,width=7,anchor="w").pack(side="left")
            e=tk.Entry(row,font=("Courier",10),bg=BG,fg=WHITE,insertbackground=NEON,relief="flat")
            e.pack(side="left",fill="x",expand=True,ipady=5)
            self.entries[label]=e
        tk.Button(ff,text="➕ ADD",font=("Courier",9,"bold"),bg=PURPLE,fg=WHITE,
            relief="flat",padx=10,pady=5,command=self.add).pack(pady=6)
        self.lb=tk.Listbox(r,bg=BG3,fg=WHITE,font=("Courier",9),selectbackground=PURPLE,relief="flat",height=12)
        self.lb.pack(fill="both",expand=True,padx=15,pady=5)
        tk.Button(r,text="🗑 Delete",font=("Courier",9),bg=BG3,fg="#FF0044",
            relief="flat",padx=10,pady=4,command=self.delete).pack(pady=4)
        self.contacts=json.load(open(F)) if os.path.exists(F) else []
        self.render()
    def save(self):json.dump(self.contacts,open(F,"w"),indent=2)
    def add(self):
        n,p,e=self.entries["Name"].get().strip(),self.entries["Phone"].get().strip(),self.entries["Email"].get().strip()
        if n:
            self.contacts.append({"name":n,"phone":p,"email":e})
            for x in self.entries.values():x.delete(0,"end")
            self.save();self.render()
    def delete(self):
        s=self.lb.curselection()
        if s:del self.contacts[s[0]];self.save();self.render()
    def render(self):
        self.lb.delete(0,"end")
        for c in self.contacts:self.lb.insert("end",f"  {c['name']} | {c['phone']} | {c['email']}")
if __name__=="__main__":
    r=tk.Tk();Contacts(r);r.mainloop()
