import tkinter as tk
from tkinter import messagebox
import json
import os
import base64
import hashlib

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class PasswordManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 Password Manager")
        self.root.configure(bg=BG)
        self.root.geometry("600x500")
        self.db_file = os.path.expanduser("~/BrayoOS/memory/passwords.json")
        self.passwords = {}
        self.master_key = None
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔐 Password Manager",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        # Master key
        key_frame = tk.Frame(self.root, bg=BG)
        key_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(key_frame, text="Master Key:",
                bg=BG, fg=TEXT,
                font=("monospace", 11)).pack(side=tk.LEFT)
        self.master_entry = tk.Entry(key_frame, bg=DARK,
                                    fg=ACCENT, show="*",
                                    font=("monospace", 11),
                                    insertbackground=ACCENT)
        self.master_entry.pack(side=tk.LEFT, fill=tk.X,
                               expand=True, padx=5)
        tk.Button(key_frame, text="🔓 Unlock",
                 bg=ACCENT, fg=BG,
                 command=self.unlock).pack(side=tk.LEFT)

        # Add entry
        add_frame = tk.LabelFrame(self.root, text="➕ Add Password",
                                 bg=BG, fg=ACCENT,
                                 font=("monospace", 10))
        add_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entries = {}
        for label, key in [("Site:", "site"),
                           ("Username:", "user"),
                           ("Password:", "pass")]:
            f = tk.Frame(add_frame, bg=BG)
            f.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(f, text=label, bg=BG, fg=TEXT,
                    font=("monospace", 10),
                    width=10).pack(side=tk.LEFT)
            e = tk.Entry(f, bg=DARK, fg=ACCENT,
                        font=("monospace", 10),
                        insertbackground=ACCENT,
                        show="*" if key == "pass" else "")
            e.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[key] = e

        tk.Button(add_frame, text="💾 Save",
                 bg=ACCENT, fg=BG,
                 command=self.save_password).pack(pady=5)

        # List
        self.listbox = tk.Listbox(self.root, bg=DARK, fg=TEXT,
                                 font=("monospace", 10),
                                 selectbackground=ACCENT,
                                 selectforeground=BG)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox.bind("<Double-Button-1>", self.show_password)

        tk.Button(self.root, text="🗑️ Delete Selected",
                 bg=DARK, fg="red",
                 command=self.delete_password).pack(pady=5)

    def unlock(self):
        key = self.master_entry.get()
        if not key:
            messagebox.showwarning("Error", "Enter master key!")
            return
        self.master_key = hashlib.sha256(key.encode()).hexdigest()
        self.load_passwords()
        messagebox.showinfo("Unlocked", "✅ Vault unlocked!")

    def encrypt(self, data):
        return base64.b64encode(data.encode()).decode()

    def decrypt(self, data):
        try:
            return base64.b64decode(data.encode()).decode()
        except:
            return data

    def save_password(self):
        if not self.master_key:
            messagebox.showwarning("Locked", "Unlock first!")
            return
        site = self.entries["site"].get()
        user = self.entries["user"].get()
        pwd = self.entries["pass"].get()
        if not all([site, user, pwd]):
            messagebox.showwarning("Error", "Fill all fields!")
            return
        self.passwords[site] = {
            "username": self.encrypt(user),
            "password": self.encrypt(pwd)
        }
        self.save_db()
        self.load_passwords()
        for e in self.entries.values():
            e.delete(0, tk.END)
        messagebox.showinfo("Saved", f"✅ {site} saved!")

    def save_db(self):
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        with open(self.db_file, 'w') as f:
            json.dump(self.passwords, f)

    def load_passwords(self):
        self.listbox.delete(0, tk.END)
        if os.path.exists(self.db_file):
            with open(self.db_file) as f:
                self.passwords = json.load(f)
        for site in self.passwords:
            self.listbox.insert(tk.END, f"🔑 {site}")

    def show_password(self, event):
        sel = self.listbox.get(tk.ACTIVE)
        if not sel:
            return
        site = sel[3:]
        if site in self.passwords:
            user = self.decrypt(self.passwords[site]["username"])
            pwd = self.decrypt(self.passwords[site]["password"])
            messagebox.showinfo(site,
                f"👤 Username: {user}\n🔑 Password: {pwd}")

    def delete_password(self):
        sel = self.listbox.get(tk.ACTIVE)
        if not sel:
            return
        site = sel[3:]
        if messagebox.askyesno("Delete", f"Delete {site}?"):
            del self.passwords[site]
            self.save_db()
            self.load_passwords()

if __name__ == "__main__":
    PasswordManager()
