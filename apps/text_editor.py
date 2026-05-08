import tkinter as tk
from tkinter import filedialog, messagebox
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
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
        # Menu
        menubar = tk.Menu(
            self.root,
            bg=DARK, fg=ACCENT)

        file_menu = tk.Menu(
            menubar, tearoff=0,
            bg=DARK, fg=ACCENT)
        file_menu.add_command(
            label="New",
            command=self.new_file)
        file_menu.add_command(
            label="Open",
            command=self.open_file)
        file_menu.add_command(
            label="Save",
            command=self.save_file)
        file_menu.add_command(
            label="Save As",
            command=self.save_as)
        menubar.add_cascade(
            label="File",
            menu=file_menu)

        edit_menu = tk.Menu(
            menubar, tearoff=0,
            bg=DARK, fg=ACCENT)
        edit_menu.add_command(
            label="Select All",
            command=self.select_all)
        edit_menu.add_command(
            label="Copy",
            command=self.copy)
        edit_menu.add_command(
            label="Paste",
            command=self.paste)
        menubar.add_cascade(
            label="Edit",
            menu=edit_menu)

        self.root.config(menu=menubar)

        # Toolbar
        toolbar = tk.Frame(
            self.root, bg=DARK)
        toolbar.pack(fill=tk.X)

        for text, cmd in [
            ("📄 New", self.new_file),
            ("📂 Open", self.open_file),
            ("💾 Save", self.save_file),
        ]:
            tk.Button(
                toolbar, text=text,
                bg=DARK, fg=ACCENT,
                font=("monospace", 9),
                relief=tk.FLAT,
                command=cmd).pack(
                    side=tk.LEFT,
                    padx=3, pady=3)

        # Line numbers + editor
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.BOTH, expand=True)

        self.line_nums = tk.Text(
            frame, bg=DARK,
            fg="#444444",
            font=("monospace", 11),
            width=4, state=tk.DISABLED,
            relief=tk.FLAT)
        self.line_nums.pack(
            side=tk.LEFT, fill=tk.Y)

        self.text = tk.Text(
            frame, bg=BG, fg=ACCENT,
            font=("monospace", 11),
            insertbackground=ACCENT,
            relief=tk.FLAT,
            wrap=tk.NONE)
        self.text.pack(
            side=tk.LEFT,
            fill=tk.BOTH, expand=True)
        self.text.bind(
            '<KeyRelease>',
            self.update_lines)

        # Scrollbar
        scroll = tk.Scrollbar(
            frame, command=self.text.yview)
        scroll.pack(
            side=tk.RIGHT, fill=tk.Y)
        self.text.config(
            yscrollcommand=scroll.set)

        # Status
        self.status = tk.Label(
            self.root,
            text="New File",
            bg=DARK, fg=ACCENT,
            font=("monospace", 9))
        self.status.pack(fill=tk.X)

        self.update_lines()

    def update_lines(self, event=None):
        lines = int(self.text.index(
            'end').split('.')[0])
        self.line_nums.config(
            state=tk.NORMAL)
        self.line_nums.delete(1.0, tk.END)
        for i in range(1, lines):
            self.line_nums.insert(
                tk.END, f"{i}\n")
        self.line_nums.config(
            state=tk.DISABLED)

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
            self.status.config(
                text=os.path.basename(path))
            self.update_lines()

    def save_file(self):
        if self.current_file:
            with open(
                    self.current_file, 'w') as f:
                f.write(self.text.get(
                    1.0, tk.END))
            self.status.config(
                text=f"✅ Saved!")
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.current_file = path
            self.save_file()

    def select_all(self):
        self.text.tag_add(
            'sel', '1.0', 'end')

    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(
            self.text.get(
                tk.SEL_FIRST, tk.SEL_LAST))

    def paste(self):
        self.text.insert(
            tk.INSERT,
            self.root.clipboard_get())

if __name__ == "__main__":
    TextEditor()
