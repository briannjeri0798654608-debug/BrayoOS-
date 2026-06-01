import tkinter as tk
import os,json,threading,httpx
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

NOTES_FILE=os.path.expanduser("~/BrayoOS/memory/smart_notes.json")
os.makedirs(os.path.dirname(NOTES_FILE),exist_ok=True)
GROQ=os.environ.get("GROQ_API_KEY","")

class SmartNotes:
    def __init__(self,root):
        self.root=root
        self.root.title("📝 Smart Notes")
        self.root.geometry("700x560")
        self.root.configure(bg=BG)
        self.notes=self.load()
        self.current=None
        self.build_ui()

    def load(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE) as f:return json.load(f)
        return []

    def save(self):
        with open(NOTES_FILE,"w") as f:json.dump(self.notes,f,indent=2)

    def build_ui(self):
        hdr=tk.Frame(self.root,bg=BG2,height=44)
        hdr.pack(fill="x");hdr.pack_propagate(False)
        tk.Label(hdr,text="📝 SMART NOTES",font=("Courier",13,"bold"),
                bg=BG2,fg=NEON).pack(side="left",padx=12,pady=10)
        tk.Label(hdr,text="AIRA-powered notes",font=("Courier",8),
                bg=BG2,fg=DIM).pack(side="left")
        tk.Label(hdr,text=f"{len(self.notes)} notes",font=("Courier",8),
                bg=BG2,fg=PURPLE).pack(side="right",padx=12)
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x")

        main=tk.Frame(self.root,bg=BG)
        main.pack(fill="both",expand=True)

        # Notes list
        left=tk.Frame(main,bg=BG2,width=200)
        left.pack(side="left",fill="y");left.pack_propagate(False)
        tk.Label(left,text="◈ MY NOTES",font=("Courier",8,"bold"),
                bg=BG2,fg=PURPLE).pack(pady=6,padx=8,anchor="w")
        tk.Button(left,text="➕ New Note",font=("Courier",8),
                 bg=PURPLE,fg=WHITE,relief="flat",
                 command=self.new_note).pack(fill="x",padx=6,pady=3)

        self.notes_list=tk.Listbox(left,bg=BG2,fg=WHITE,
                                   font=("Courier",8),
                                   selectbackground=PURPLE,
                                   relief="flat",activestyle="none")
        self.notes_list.pack(fill="both",expand=True,padx=4,pady=4)
        self.notes_list.bind("<<ListboxSelect>>",self.load_note)
        self.render_list()

        # Editor
        right=tk.Frame(main,bg=BG)
        right.pack(side="left",fill="both",expand=True,padx=5,pady=5)

        self.title_e=tk.Entry(right,font=("Courier",12,"bold"),
                             bg=BG3,fg=NEON,insertbackground=NEON,
                             relief="flat")
        self.title_e.pack(fill="x",padx=5,ipady=8)
        self.title_e.insert(0,"Note title...")

        self.editor=tk.Text(right,bg=BG3,fg=WHITE,
                           font=("Courier",10),relief="flat",
                           insertbackground=NEON,wrap="word")
        self.editor.pack(fill="both",expand=True,padx=5,pady=5)

        # Action buttons
        af=tk.Frame(right,bg=BG);af.pack(fill="x",padx=5,pady=3)
        for txt,cmd,color in [
            ("💾 Save",self.save_note,GREEN),
            ("🗑 Delete",self.delete_note,RED),
            ("🤖 Summarize",self.ai_summarize,NEON),
            ("✨ Improve",self.ai_improve,GOLD),
            ("📋 Copy",self.copy_note,"#AAAAFF"),
        ]:
            tk.Button(af,text=txt,font=("Courier",8),bg=BG3,fg=color,
                     relief="flat",padx=8,pady=4,
                     command=cmd).pack(side="left",padx=2)

        self.status=tk.Label(right,text="",font=("Courier",7),bg=BG,fg=DIM)
        self.status.pack(anchor="w",padx=5)
        tk.Label(self.root,text="BrayoOS Smart Notes v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def render_list(self):
        self.notes_list.delete(0,"end")
        for n in self.notes:
            self.notes_list.insert("end",f"  📝 {n['title'][:18]}")

    def new_note(self):
        note={"title":"New Note","content":"",
              "date":datetime.now().strftime("%Y-%m-%d %H:%M")}
        self.notes.insert(0,note)
        self.save();self.render_list()
        self.notes_list.selection_set(0)
        self.current=0
        self.title_e.delete(0,"end")
        self.title_e.insert(0,"New Note")
        self.editor.delete("1.0","end")

    def load_note(self,e=None):
        sel=self.notes_list.curselection()
        if not sel:return
        self.current=sel[0]
        if self.current>=len(self.notes):return
        n=self.notes[self.current]
        self.title_e.delete(0,"end")
        self.title_e.insert(0,n["title"])
        self.editor.delete("1.0","end")
        self.editor.insert("end",n["content"])

    def save_note(self):
        if self.current is None:self.new_note();return
        self.notes[self.current]["title"]=self.title_e.get()
        self.notes[self.current]["content"]=self.editor.get("1.0","end")
        self.notes[self.current]["date"]=datetime.now().strftime("%Y-%m-%d %H:%M")
        self.save();self.render_list()
        self.status.config(text="✅ Saved!",fg=GREEN)

    def delete_note(self):
        if self.current is None:return
        del self.notes[self.current]
        self.current=None
        self.save();self.render_list()
        self.title_e.delete(0,"end")
        self.editor.delete("1.0","end")

    def copy_note(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.editor.get("1.0","end"))
        self.status.config(text="📋 Copied!",fg=GREEN)

    def ai_summarize(self):
        text=self.editor.get("1.0","end").strip()
        if not text or not GROQ:return
        self.status.config(text="🧠 AIRA summarizing...",fg=GOLD)
        threading.Thread(target=self._ai_action,
                        args=(text,"Summarize this in 3 bullet points:"),
                        daemon=True).start()

    def ai_improve(self):
        text=self.editor.get("1.0","end").strip()
        if not text or not GROQ:return
        self.status.config(text="✨ AIRA improving...",fg=GOLD)
        threading.Thread(target=self._ai_action,
                        args=(text,"Improve and rewrite this text:"),
                        daemon=True).start()

    def _ai_action(self,text,prompt):
        try:
            r=httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {GROQ}",
                        "Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile",
                      "messages":[{"role":"user",
                                  "content":f"{prompt}\n\n{text[:500]}"}],
                      "max_tokens":300},timeout=15)
            result=r.json()["choices"][0]["message"]["content"].strip()
            self.root.after(0,self._show_ai_result,result)
        except Exception as e:
            self.root.after(0,self.status.config,
                           {"text":f"❌ {str(e)[:30]}","fg":RED})

    def _show_ai_result(self,result):
        win=tk.Toplevel(self.root)
        win.title("AIRA Result");win.configure(bg=BG);win.geometry("500x350")
        tk.Label(win,text="🤖 AIRA Result",font=("Courier",11,"bold"),
                bg=BG,fg=NEON).pack(pady=8)
        t=tk.Text(win,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",wrap="word")
        t.pack(fill="both",expand=True,padx=10,pady=5)
        t.insert("end",result)
        tk.Button(win,text="📋 Copy & Use",font=("Courier",9,"bold"),
                 bg=PURPLE,fg=WHITE,relief="flat",padx=10,pady=5,
                 command=lambda:[self.editor.delete("1.0","end"),
                                self.editor.insert("end",result),
                                win.destroy()]).pack(pady=5)
        self.status.config(text="✅ Done!",fg=GREEN)

if __name__=="__main__":
    root=tk.Tk();SmartNotes(root);root.mainloop()
