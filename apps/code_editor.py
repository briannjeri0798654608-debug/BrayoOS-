import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"

class CodeEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS - Code Editor")
        self.root.configure(bg=BG)
        self.root.geometry("900x700")
        self.current_file = None
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        # Menu bar
        menubar = tk.Menu(self.root, bg="#1A1A1A", fg=TEXT)
        file_menu = tk.Menu(menubar, tearoff=0, bg="#1A1A1A", fg=TEXT)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        menubar.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menubar, tearoff=0, bg="#1A1A1A", fg=TEXT)
        run_menu.add_command(label="Run Python", command=self.run_python)
        run_menu.add_command(label="Run Bash", command=self.run_bash)
        menubar.add_cascade(label="Run", menu=run_menu)
        self.root.config(menu=menubar)

        tk.Label(self.root, text="💻 Code Editor",
                bg=BG, fg=ACCENT,
                font=("monospace", 14, "bold")).pack(pady=5)

        # Editor
        self.editor = scrolledtext.ScrolledText(
            self.root, bg="#1A1A1A", fg=ACCENT,
            font=("monospace", 12), wrap=tk.NONE,
            insertbackground=ACCENT)
        self.editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Output
        tk.Label(self.root, text="Output:",
                bg=BG, fg=TEXT,
                font=("monospace", 10)).pack(anchor=tk.W, padx=10)
        self.output = scrolledtext.ScrolledText(
            self.root, bg="#0A0A0A", fg="#00FF41",
            font=("monospace", 10), height=8)
        self.output.pack(fill=tk.X, padx=10, pady=5)

        # Status
        self.status = tk.Label(self.root, text="New File",
                              bg="#1A1A1A", fg=ACCENT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def new_file(self):
        self.editor.delete(1.0, tk.END)
        self.current_file = None
        self.status.config(text="New File")

    def open_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path) as f:
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, f.read())
            self.current_file = path
            self.status.config(text=path)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as f:
                f.write(self.editor.get(1.0, tk.END))
            self.status.config(text=f"Saved: {self.current_file}")
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.current_file = path
            self.save_file()

    def run_python(self):
        self.save_file()
        if self.current_file:
            import subprocess
            result = subprocess.run(
                ["python", self.current_file],
                capture_output=True, text=True)
            self.output.delete(1.0, tk.END)
            self.output.insert(1.0, result.stdout + result.stderr)

    def run_bash(self):
        self.save_file()
        if self.current_file:
            import subprocess
            result = subprocess.run(
                ["bash", self.current_file],
                capture_output=True, text=True)
            self.output.delete(1.0, tk.END)
            self.output.insert(1.0, result.stdout + result.stderr)

if __name__ == "__main__":
    CodeEditor()
