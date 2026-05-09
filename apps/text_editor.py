import tkinter as tk
from tkinter import filedialog
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
DARK = "#1A1A1A"

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📝 Text Editor")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.current_file = None
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        menubar = tk.Menu(self.root, bg=DARK, fg=ACCENT)
        file_menu = tk.Menu(menubar, tearoff=0, bg=DARK, fg=ACCENT)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

        toolbar = tk.Frame(self.root, bg=DARK)
        toolbar.pack(fill=tk.X)
        for text, cmd in [("📄 New", self.new_file),
                          ("📂 Open", self.open_file),
                          ("💾 Save", self.save_file)]:
            tk.Button(toolbar, text=text, bg=DARK,
                     fg=ACCENT, font=("monospace", 9),
                     relief=tk.FLAT,
                     command=cmd).pack(side=tk.LEFT, padx=3, pady=3)

        self.text = tk.Text(self.root, bg=BG, fg=ACCENT,
                           font=("monospace", 11),
                           insertbackground=ACCENT,
                           relief=tk.FLAT)
        self.text.pack(fill=tk.BOTH, expand=True, padx=5)

        self.status = tk.Label(self.root, text="New File",
                              bg=DARK, fg=ACCENT,
                              font=("monospace", 9))
        self.status.pack(fill=tk.X)

    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.current_file = None
        self.status.config(text="New File")

    def open_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path) as f:
                self.text.delete(1.0, tk.END)
                self.text.insert(1.0, f.read())
            self.current_file = path
            self.status.config(text=os.path.basename(path))

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as f:
                f.write(self.text.get(1.0, tk.END))
            self.status.config(text="✅ Saved!")
        else:
            path = filedialog.asksaveasfilename()
            if path:
                self.current_file = path
                self.save_file()

if __name__ == "__main__":
    TextEditor()
