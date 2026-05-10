import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import subprocess

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"

class FileManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS - File Manager")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.current_path = os.path.expanduser("~")
        self.build_ui()
        self.load_dir()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📁 File Manager",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        # Path bar
        path_frame = tk.Frame(self.root, bg=BG)
        path_frame.pack(fill=tk.X, padx=10)

        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(path_frame, textvvirgyble=self.path_var,
                                  bg="#1A1A1A", fg=ACCENT,
                                  font=("monospace", 11),
                                  insertbackground=ACCENT)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.path_entry.bind("<Return>", lambda e: self.navigate())

        tk.Button(path_frame, text="Go", bg=ACCENT, fg=BG,
                 command=self.navigate).pack(side=tk.LEFT, padx=5)
        tk.Button(path_frame, text="⬆ Up", bg="#1A1A1A", fg=TEXT,
                 command=self.go_up).pack(side=tk.LEFT, padx=2)

        # Button bar
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="🗑 Delete", bg="#1A1A1A",
                 fg="red", command=self.delete_file).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="📋 Copy Path", bg="#1A1A1A",
                 fg=TEXT, command=self.copy_path).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🔄 Refresh", bg="#1A1A1A",
                 fg=TEXT, command=self.load_dir).pack(side=tk.LEFT, padx=2)

        # File list
        self.listbox = tk.Listbox(self.root, bg="#1A1A1A", fg=TEXT,
                                 font=("monospace", 11),
                                 selectbackground=ACCENT,
                                 selectforeground=BG)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

        # Status bar
        self.status = tk.Label(self.root, text="", bg="#1A1A1A",
                              fg=ACCENT, font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def load_dir(self):
        self.listbox.delete(0, tk.END)
        self.path_var.set(self.current_path)
        try:
            items = sorted(os.listdir(self.current_path))
            for item in items:
                full = os.path.join(self.current_path, item)
                prefix = "📁 " if os.path.isdir(full) else "📄 "
                self.listbox.insert(tk.END, prefix + item)
            self.status.config(text=f"{len(items)} items")
        except Exception as e:
            self.status.config(text=f"Error: {e}")

    def navigate(self):
        path = self.path_var.get()
        if os.path.isdir(path):
            self.current_path = path
            self.load_dir()

    def go_up(self):
        self.current_path = os.path.dirname(self.current_path)
        self.load_dir()

    def on_double_click(self, event):
        selection = self.listbox.get(tk.ACTIVE)
        name = selection[3:]
        full_path = os.path.join(self.current_path, name)
        if os.path.isdir(full_path):
            self.current_path = full_path
            self.load_dir()

    def delete_file(self):
        selection = self.listbox.get(tk.ACTIVE)
        if not selection:
            return
        name = selection[3:]
        full_path = os.path.join(self.current_path, name)
        if messagebox.askyesno("Delete", f"Delete {name}?"):
            try:
                os.remove(full_path)
                self.load_dir()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def copy_path(self):
        selection = self.listbox.get(tk.ACTIVE)
        if selection:
            name = selection[3:]
            full_path = os.path.join(self.current_path, name)
            self.root.clipboard_clear()
            self.root.clipboard_append(full_path)
            self.status.config(text=f"Copied: {full_path}")

if __name__ == "__main__":
    FileManager()
