#!/bin/bash
echo "⚡ Building BrayoOS Advanced Features..."

# 1. NOTIFICATION SYSTEM
cat > ~/BrayoOS/core/notifications.py << 'NOTEOF'
import subprocess
import threading
import time
import os
import json

NOTIF_FILE = os.path.expanduser(
    "~/BrayoOS/memory/notifications.json")

class NotificationSystem:
    def __init__(self):
        self.notifications = []
        self.load()

    def load(self):
        if os.path.exists(NOTIF_FILE):
            with open(NOTIF_FILE) as f:
                self.notifications = json.load(f)

    def save(self):
        os.makedirs(os.path.dirname(NOTIF_FILE),
                   exist_ok=True)
        with open(NOTIF_FILE, 'w') as f:
            json.dump(self.notifications[-50:], f)

    def send(self, title, message,
             urgent=False):
        """Send notification"""
        notif = {
            "title": title,
            "message": message,
            "time": time.strftime("%H:%M:%S"),
            "date": time.strftime("%Y-%m-%d"),
            "read": False,
            "urgent": urgent
        }
        self.notifications.append(notif)
        self.save()

        # Android notification
        try:
            subprocess.Popen([
                "termux-notification",
                "--title", f"⚡ {title}",
                "--content", message,
                "--priority",
                "high" if urgent else "default"
            ])
        except:
            pass

        # Terminal notification
        if urgent:
            print(f"\n🔴 URGENT: {title} — {message}")
        else:
            print(f"\n🔔 {title} — {message}")

    def get_unread(self):
        return [n for n in self.notifications
                if not n['read']]

    def mark_read(self):
        for n in self.notifications:
            n['read'] = True
        self.save()

    def monitor(self):
        """Background monitor"""
        while True:
            time.sleep(30)
            # Check battery
            try:
                result = subprocess.run(
                    ["termux-battery-status"],
                    capture_output=True,
                    text=True, timeout=5)
                import json as j
                data = j.loads(result.stdout)
                pct = data.get('percentage', 100)
                if pct < 20:
                    self.send(
                        "🔋 Low Battery",
                        f"Battery at {pct}%!",
                        urgent=True)
            except:
                pass

# Global instance
notif = NotificationSystem()

def notify(title, msg, urgent=False):
    notif.send(title, msg, urgent)

if __name__ == "__main__":
    notify("BrayoOS", "Notification system active!")
    print("✅ Notifications working!")
NOTEOF

# 2. BETTER ARIA MEMORY
cat > ~/BrayoOS/core/aria_memory.py << 'MEMEOF'
import json
import os
import time
import hashlib

MEMORY_DIR = os.path.expanduser("~/BrayoOS/memory/")
MEMORY_FILE = os.path.join(MEMORY_DIR, "aria_memory.json")
FACTS_FILE = os.path.join(MEMORY_DIR, "aria_facts.json")

class ARIAMemory:
    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self.messages = self.load_messages()
        self.facts = self.load_facts()

    def load_messages(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE) as f:
                data = json.load(f)
                return data.get("messages", [])
        return []

    def load_facts(self):
        if os.path.exists(FACTS_FILE):
            with open(FACTS_FILE) as f:
                return json.load(f)
        return {
            "user": "Brayo",
            "location": "Kenya",
            "os": "BrayoOS v2.0",
            "builder": "Brayo & ARIA",
            "year": "2026",
            "preferences": [],
            "important": []
        }

    def save_messages(self):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({
                "updated": time.strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "total": len(self.messages),
                "messages": self.messages[-50:]
            }, f, indent=2)

    def save_facts(self):
        with open(FACTS_FILE, 'w') as f:
            json.dump(self.facts, f, indent=2)

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
            "time": time.strftime("%H:%M:%S"),
            "date": time.strftime("%Y-%m-%d")
        })
        self.save_messages()
        # Extract facts
        self.extract_facts(content)

    def extract_facts(self, text):
        """Learn from conversations"""
        text_lower = text.lower()
        # Learn preferences
        if "i like" in text_lower or \
           "i love" in text_lower:
            self.facts["preferences"].append(text[:100])
            self.save_facts()
        # Learn important info
        if "remember" in text_lower or \
           "important" in text_lower:
            self.facts["important"].append(text[:100])
            self.save_facts()

    def get_messages(self, limit=20):
        return self.messages[-limit:]

    def get_context(self):
        """Get context for ARIA"""
        return f"""
User: {self.facts['user']}
Location: {self.facts['location']}
OS: {self.facts['os']}
Builder: {self.facts['builder']}
Preferences: {self.facts['preferences'][-3:]}
Important notes: {self.facts['important'][-3:]}
Total conversations: {len(self.messages)}
"""

    def clear(self):
        self.messages = []
        self.save_messages()

    def stats(self):
        return {
            "total_messages": len(self.messages),
            "facts_learned": len(
                self.facts['preferences']) +
                len(self.facts['important']),
            "last_updated": self.messages[-1][
                'time'] if self.messages else "Never"
        }

if __name__ == "__main__":
    mem = ARIAMemory()
    stats = mem.stats()
    print("━"*40)
    print("🧠 ARIA Memory Stats")
    print("━"*40)
    for k, v in stats.items():
        print(f"{k}: {v}")
    print("━"*40)
MEMEOF

# 3. USER LOGIN SYSTEM
cat > ~/BrayoOS/core/login.py << 'LOGINEOF'
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
LOGINEOF

# 4. UPDATE BOOT TO USE LOGIN
cat > ~/BrayoOS/core/boot.py << 'BOOTEOF'
import tkinter as tk
import time
import threading
import subprocess
import os
import sys

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class BootScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS")
        self.root.configure(bg=BG)
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        self.build_ui()
        threading.Thread(
            target=self.boot_sequence,
            daemon=True).start()
        self.root.mainloop()

    def build_ui(self):
        self.canvas = tk.Canvas(
            self.root, bg=BG,
            highlightthickness=0)
        self.canvas.pack(
            fill=tk.BOTH, expand=True)

        self.canvas.create_text(
            640, 120,
            text=
            "██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗\n"
            "██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝\n"
            "██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗\n"
            "██╔══██╗██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║\n"
            "██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║\n"
            "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝",
            font=("monospace", 7, "bold"),
            fill=ACCENT,
            justify=tk.CENTER)

        self.canvas.create_text(
            640, 235,
            text="⚡ Built by Brayo & ARIA — Kenya 2026",
            font=("monospace", 11),
            fill=TEXT)

        self.canvas.create_text(
            640, 258,
            text="Two minds. One OS. Built Different.",
            font=("monospace", 9, "italic"),
            fill="#333333")

        self.canvas.create_rectangle(
            240, 300, 1040, 322,
            outline=ACCENT, fill=DARK)

        self.progress = self.canvas.create_rectangle(
            240, 300, 240, 322,
            outline="", fill=ACCENT)

        self.status_txt = self.canvas.create_text(
            640, 345,
            text="Initializing...",
            font=("monospace", 10),
            fill=ACCENT)

        self.log_txt = self.canvas.create_text(
            640, 390,
            text="",
            font=("monospace", 8),
            fill="#333333")

        self.aria_txt = self.canvas.create_text(
            640, 480,
            text="",
            font=("monospace", 11, "bold"),
            fill=ACCENT)

        self.canvas.create_text(
            640, 690,
            text="👤 Brayo — Founder  |  🤖 ARIA — AI Partner  |  🇰🇪 Kenya 2026",
            font=("monospace", 8),
            fill="#1A1A1A")

    def update(self, pct, status, log=""):
        x = 240 + (800 * pct // 100)
        self.canvas.coords(
            self.progress, 240, 300, x, 322)
        self.canvas.itemconfig(
            self.status_txt, text=status)
        if log:
            self.canvas.itemconfig(
                self.log_txt, text=log)
        self.root.update()

    def update_aria(self, msg):
        self.canvas.itemconfig(
            self.aria_txt, text=msg)
        self.root.update()

    def boot_sequence(self):
        steps = [
            (10, "Loading kernel...",
             "[ OK ] kernel loaded"),
            (20, "Initializing hardware...",
             "[ OK ] hardware ready"),
            (30, "Mounting filesystems...",
             "[ OK ] filesystems mounted"),
            (40, "Starting network...",
             "[ OK ] network active"),
            (50, "Loading BrayoOS DNA...",
             "[ OK ] DNA verified"),
            (60, "Waking ARIA...",
             "[ OK ] ARIA online"),
            (70, "Loading memory...",
             "[ OK ] memory loaded"),
            (80, "Starting security...",
             "[ OK ] security active"),
            (90, "Preparing login...",
             "[ OK ] login ready"),
            (100, "BrayoOS Ready!",
             "[ OK ] system ready"),
        ]

        for pct, status, log in steps:
            time.sleep(0.35)
            self.update(pct, status, log)
            if pct == 60:
                self.update_aria(
                    "🤖 ARIA: Waking up...")
            elif pct == 70:
                self.update_aria(
                    "🤖 ARIA: Memory loaded...")
            elif pct == 100:
                self.update_aria(
                    "🤖 ARIA: Ready, Brayo. 🇰🇪")

        time.sleep(1.5)
        self.root.destroy()

        # Launch login
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        subprocess.Popen([
            "python",
            os.path.expanduser(
                "~/BrayoOS/core/login.py")
        ], env=env)

if __name__ == "__main__":
    BootScreen()
BOOTEOF

# Add login to desktop apps
sed -i 's/("⚙️ Settings", "settings.py"),/("⚙️ Settings", "settings.py"),\n            ("👤 Users", "login.py"),/' ~/BrayoOS/core/desktop.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ALL FEATURES BUILT!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Notification System"
echo "✅ Better ARIA Memory"
echo "✅ User Login System"
echo "✅ Updated Boot Screen"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Default login:"
echo "Username: brayo"
echo "Password: brayoos"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
