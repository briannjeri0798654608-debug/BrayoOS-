import tkinter as tk
from tkinter import scrolledtext
import subprocess
import json
import threading

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class Contacts:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("👥 Contacts")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.load_contacts()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="👥 Contacts",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        search_frame = tk.Frame(self.root, bg=BG)
        search_frame.pack(fill=tk.X, padx=10)

        self.search = tk.Entry(search_frame, bg=DARK,
                              fg=ACCENT, font=("monospace", 11),
                              insertbackground=ACCENT)
        self.search.pack(side=tk.LEFT, fill=tk.X,
                        expand=True, padx=5)
        self.search.bind("<Return>", lambda e: self.filter_contacts())

        tk.Button(search_frame, text="🔍 Search",
                 bg=ACCENT, fg=BG,
                 command=self.filter_contacts).pack(side=tk.LEFT)

        self.listbox = tk.Listbox(self.root, bg=DARK, fg=TEXT,
                                 font=("monospace", 11),
                                 selectbackground=ACCENT,
                                 selectforeground=BG)
        self.listbox.pack(fill=tk.BOTH, expand=True,
                         padx=10, pady=5)

        self.status = tk.Label(self.root, text="Loading...",
                              bg=DARK, fg=ACCENT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def load_contacts(self):
        def run():
            try:
                result = subprocess.run(
                    ["termux-contact-list"],
                    capture_output=True, text=True, timeout=10)
                self.contacts = json.loads(result.stdout)
                self.listbox.delete(0, tk.END)
                for c in self.contacts:
                    self.listbox.insert(
                        tk.END,
                        f"👤 {c.get('name','')} - "
                        f"{c.get('number','')}")
                self.status.config(
                    text=f"✅ {len(self.contacts)} contacts")
            except Exception as e:
                self.status.config(text=f"Error: {e}")
        threading.Thread(target=run).start()

    def filter_contacts(self):
        query = self.search.get().lower()
        self.listbox.delete(0, tk.END)
        for c in self.contacts:
            if query in c.get('name', '').lower() or \
               query in c.get('number', '').lower():
                self.listbox.insert(
                    tk.END,
                    f"👤 {c.get('name','')} - "
                    f"{c.get('number','')}")

if __name__ == "__main__":
    Contacts()
