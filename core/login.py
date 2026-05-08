import tkinter as tk
from tkinter import messagebox
import hashlib
import json
import os
import time
import subprocess
import sys

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
GOLD = "#FFD700"

USERS_FILE = os.path.expanduser(
    "~/BrayoOS/memory/users.json")

class LoginSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS — Login")
        self.root.configure(bg=BG)
        self.root.geometry("500x600+390+60")
        self.root.resizable(False, False)
        self.users = self.load_users()
        self.attempts = 0
        self.build_ui()
        self.root.mainloop()

    def load_users(self):
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE) as f:
                return json.load(f)
        # Create default admin
        users = {
            "brayo": {
                "password": self.hash_pass("brayoos"),
                "role": "admin",
                "created": time.strftime(
                    "%Y-%m-%d"),
                "last_login": None
            }
        }
        self.save_users(users)
        return users

    def save_users(self, users=None):
        if users is None:
            users = self.users
        os.makedirs(os.path.dirname(USERS_FILE),
                   exist_ok=True)
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)

    def hash_pass(self, password):
        return hashlib.sha256(
            password.encode()).hexdigest()

    def build_ui(self):
        canvas = tk.Canvas(self.root, bg=BG,
                          highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Logo
        canvas.create_text(
            250, 80,
            text="⚡",
            font=("monospace", 50),
            fill=ACCENT)

        canvas.create_text(
            250, 140,
            text="BrayoOS v2.0",
            font=("monospace", 24, "bold"),
            fill=ACCENT)

        canvas.create_text(
            250, 170,
            text="Built by Brayo & ARIA — Kenya 2026",
            font=("monospace", 10),
            fill=GOLD)

        # Divider
        canvas.create_line(
            50, 195, 450, 195,
            fill="#1A1A1A", width=1)

        # Login form
        canvas.create_text(
            250, 230,
            text="LOGIN",
            font=("monospace", 14, "bold"),
            fill=ACCENT)

        # Username
        canvas.create_text(
            150, 270,
            text="Username:",
            font=("monospace", 11),
            fill=TEXT)

        self.username = tk.Entry(
            self.root,
            bg=DARK, fg=ACCENT,
            font=("monospace", 12),
            insertbackground=ACCENT,
            relief=tk.FLAT,
            width=20)
        self.username.place(x=150, y=285,
                           width=200, height=35)
        self.username.insert(0, "brayo")

        # Password
        canvas.create_text(
            150, 340,
            text="Password:",
            font=("monospace", 11),
            fill=TEXT)

        self.password = tk.Entry(
            self.root,
            bg=DARK, fg=ACCENT,
            font=("monospace", 12),
            insertbackground=ACCENT,
            relief=tk.FLAT,
            show="●",
            width=20)
        self.password.place(x=150, y=355,
                           width=200, height=35)
        self.password.bind(
            "<Return>",
            lambda e: self.login())

        # Login button
        login_btn = tk.Button(
            self.root,
            text="⚡ LOGIN",
            bg=ACCENT, fg=BG,
            font=("monospace", 12, "bold"),
            relief=tk.FLAT,
            command=self.login,
            cursor="hand2")
        login_btn.place(x=150, y=420,
                       width=200, height=40)

        # Status
        self.status = canvas.create_text(
            250, 480,
            text="",
            font=("monospace", 10),
            fill="red")

        # Footer
        canvas.create_text(
            250, 560,
            text="\"Two minds. One OS. Built Different.\"",
            font=("monospace", 9),
            fill="#222222")

        # Focus password
        self.password.focus()

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            self.show_status(
                "❌ Enter username and password!")
            return

        if username in self.users:
            hashed = self.hash_pass(password)
            if self.users[username][
                    "password"] == hashed:
                # Success
                self.users[username][
                    "last_login"] = time.strftime(
                        "%Y-%m-%d %H:%M:%S")
                self.save_users()
                self.show_status(
                    "✅ Login successful!")
                self.root.after(
                    1000, self.launch_desktop)
            else:
                self.attempts += 1
                if self.attempts >= 3:
                    self.show_status(
                        "🔒 Too many attempts!")
                    self.root.after(
                        3000,
                        self.root.destroy)
                else:
                    self.show_status(
                        f"❌ Wrong password! "
                        f"({3-self.attempts} left)")
        else:
            self.show_status(
                "❌ User not found!")

    def show_status(self, msg):
        self.root.nametowidget(
            self.root.winfo_children()[0])
        canvas = self.root.winfo_children()[0]
        canvas.itemconfig(
            self.status, text=msg)

    def launch_desktop(self):
        self.root.destroy()
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        subprocess.Popen([
            "python",
            os.path.expanduser(
                "~/BrayoOS/core/desktop.py")
        ], env=env)

if __name__ == "__main__":
    LoginSystem()
