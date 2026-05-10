import tkinter as tk
from tkinter import messagebox
import json
import hashlib
import os
from datetime import datetime

USERS_FILE = os.path.expanduser("~/BrayoOS/memory/users.json")
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

DEFAULT_USERS = {
    "Brayo": {
        "pin": hashlib.sha256("1337".encode()).hexdigest(),
        "clearance": "LEVEL 5 — OWNER",
        "color": "#00FF41",
        "created": "2026-05-10",
        "last_login": "Never"
    },
    "Guest": {
        "pin": hashlib.sha256("0000".encode()).hexdigest(),
        "clearance": "LEVEL 1 — GUEST",
        "color": "#888888",
        "created": "2026-05-10",
        "last_login": "Never"
    }
}

class UserManager:
    def __init__(self, root):
        self.root = root
        self.root.title("👤 User Manager")
        self.root.geometry("620x560")
        self.root.configure(bg="#0D0D0D")
        self.users = self.load_users()
        self.build_ui()

    def load_users(self):
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE) as f:
                return json.load(f)
        with open(USERS_FILE, "w") as f:
            json.dump(DEFAULT_USERS, f, indent=2)
        return DEFAULT_USERS

    def save_users(self):
        with open(USERS_FILE, "w") as f:
            json.dump(self.users, f, indent=2)

    def build_ui(self):
        tk.Label(self.root, text="👤 USER MANAGER", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=8)
        tk.Label(self.root, text="[ BRAYOOS MULTI-USER CLEARANCE SYSTEM ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        tk.Label(self.root, text="◈ SYSTEM USERS", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15, pady=(10,3))

        self.user_frame = tk.Frame(self.root, bg="#0D0D0D")
        self.user_frame.pack(fill="x", padx=15)
        self.render_users()

        # Add user form
        tk.Label(self.root, text="◈ ADD NEW USER", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15, pady=(15,3))

        form = tk.Frame(self.root, bg="#001100")
        form.pack(fill="x", padx=15, pady=3)

        for label, attr in [("Username:", "new_name"), ("PIN (4 digits):", "new_pin")]:
            row = tk.Frame(form, bg="#001100")
            row.pack(fill="x", padx=8, pady=4)
            tk.Label(row, text=label, font=("Courier", 9), bg="#001100",
                     fg="#004400", width=16, anchor="w").pack(side="left")
            entry = tk.Entry(row, font=("Courier", 10), bg="#000800",
                             fg="#00FF41", insertbackground="#00FF41",
                             relief="flat", show="*" if "PIN" in label else "")
            entry.pack(side="left", fill="x", expand=True, ipady=5, padx=5)
            setattr(self, attr, entry)

        # Clearance selector
        row = tk.Frame(form, bg="#001100")
        row.pack(fill="x", padx=8, pady=4)
        tk.Label(row, text="Clearance:", font=("Courier", 9), bg="#001100",
                 fg="#004400", width=16, anchor="w").pack(side="left")
        self.clearance_var = tk.StringVar(value="LEVEL 1 — GUEST")
        levels = ["LEVEL 1 — GUEST", "LEVEL 2 — USER",
                  "LEVEL 3 — ADMIN", "LEVEL 4 — HACKER", "LEVEL 5 — OWNER"]
        tk.OptionMenu(row, self.clearance_var, *levels).configure(
            bg="#001100", fg="#00FF41", font=("Courier", 9),
            activebackground="#003300", relief="flat")
        tk.OptionMenu(row, self.clearance_var, *levels).pack(side="left")

        tk.Button(form, text="➕ CREATE USER", command=self.add_user,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(pady=8)

        # Log
        self.log_box = tk.Text(self.root, height=5, bg="#000800", fg="#00FF41",
                                font=("Courier", 8), relief="flat", state="disabled")
        self.log_box.pack(fill="both", padx=15, pady=5)

        tk.Label(self.root, text="BrayoOS User Engine v1.0 • Brayo & Virgy 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def render_users(self):
        for w in self.user_frame.winfo_children():
            w.destroy()
        for username, data in self.users.items():
            card = tk.Frame(self.user_frame, bg="#001100")
            card.pack(fill="x", pady=3)
            tk.Label(card, text=f"👤 {username}", font=("Courier", 11, "bold"),
                     bg="#001100", fg=data.get("color","#00FF41")).pack(side="left", padx=10, pady=6)
            tk.Label(card, text=data["clearance"], font=("Courier", 9),
                     bg="#001100", fg="#004400").pack(side="left", padx=10)
            tk.Label(card, text=f"Last: {data['last_login']}", font=("Courier", 8),
                     bg="#001100", fg="#003300").pack(side="left")
            if username != "Brayo":
                tk.Button(card, text="🗑 Delete", font=("Courier", 8),
                          bg="#1a0000", fg="#FF0000", relief="flat",
                          command=lambda u=username: self.delete_user(u)).pack(side="right", padx=8)

    def add_user(self):
        name = self.new_name.get().strip()
        pin = self.new_pin.get().strip()
        if not name or not pin:
            messagebox.showwarning("Error", "Fill all fields!")
            return
        if name in self.users:
            messagebox.showwarning("Error", f"User {name} already exists!")
            return
        self.users[name] = {
            "pin": hashlib.sha256(pin.encode()).hexdigest(),
            "clearance": self.clearance_var.get(),
            "color": "#00FFFF",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_login": "Never"
        }
        self.save_users()
        self.log(f"✅ User {name} created with {self.clearance_var.get()}")
        self.render_users()
        self.new_name.delete(0, "end")
        self.new_pin.delete(0, "end")

    def delete_user(self, username):
        if messagebox.askyesno("Delete", f"Delete user {username}?"):
            del self.users[username]
            self.save_users()
            self.log(f"🗑 User {username} deleted.")
            self.render_users()

    def log(self, msg):
        self.log_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    UserManager(root)
    root.mainloop()
