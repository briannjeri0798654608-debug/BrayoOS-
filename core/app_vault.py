import tkinter as tk
from tkinter import messagebox
import hashlib
import json
import os
import subprocess

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
RED = "#FF4444"

VAULT_FILE = os.path.expanduser(
    "~/BrayoOS/memory/vault.json")

# Apps visible to everyone
PUBLIC_APPS = [
    ("🖥️\nTerminal", "terminal"),
    ("🤖\nAIRA", "aira.py"),
    ("🌐\nBrowser", "mini_browser.py"),
    ("📁\nFiles", "files.py"),
    ("🎵\nMusic", "music_player.py"),
    ("📱\nSMS", "sms_reader.py"),
    ("👥\nContacts", "contacts.py"),
    ("💰\nCrypto", "crypto_tracker.py"),
    ("🌤️\nWeather", "weather.py"),
    ("📰\nNews", "hackernews.py"),
    ("📊\nSystem", "system_monitor.py"),
    ("⚙️\nSettings", "settings.py"),
    ("📖\nOur Story", "our_story.py"),
    ("💾\nBackup", "backup.py"),
]

# Hidden hacking tools — require PIN
HIDDEN_APPS = [
    ("🛡️\nVuln Scan", "vuln_scanner.py"),
    ("🌐\nNetwork", "network.py"),
    ("📡\nWiFi", "wifi_manager.py"),
    ("🌍\nIP Track", "ip_tracker.py"),
    ("🔐\nPasswords", "password_manager.py"),
    ("📦\nApp Store", "app_store.py"),
    ("💻\nCode", "code_editor.py"),
    ("🔑\nHash", "hash_cracker.py"),
    ("💣\nPayloads", "payload_generator.py"),
    ("🌐\nSubdomain", "subdomain_scanner.py"),
    ("🔍\nDNS", "dns_lookup.py"),
    ("🔍\nOSINT", "social_osint.py"),
    ("💀\nMSF", "metasploit_helper.py"),
    ("🗺️\nNet Map", "network_mapper.py"),
    ("📡\nSniffer", "packet_sniffer.py"),
    ("🔒\nSecurity", "security_monitor.py"),
    ("🔀\nPort Fwd", "port_forwarder.py"),
    ("🕵️\nDark Web", "darkweb_monitor.py"),
    ("🛡️\nPrivacy", "privacy_shield.py"),
    ("📡\nWiFi+", "wifi_cracker.py"),
    ("🔍\nProcs", "process_monitor.py"),
]

class VaultSystem:
    def __init__(self):
        self.data = self.load()

    def load(self):
        if os.path.exists(VAULT_FILE):
            with open(VAULT_FILE) as f:
                return json.load(f)
        # Default PIN: 1337
        return {
            "pin": hashlib.sha256(
                "1337".encode()).hexdigest(),
            "hint": "Default PIN: 1337",
            "locked": True
        }

    def save(self):
        os.makedirs(os.path.dirname(VAULT_FILE),
                   exist_ok=True)
        with open(VAULT_FILE, 'w') as f:
            json.dump(self.data, f)

    def verify_pin(self, pin):
        return self.data["pin"] == \
               hashlib.sha256(
                   pin.encode()).hexdigest()

    def set_pin(self, new_pin):
        self.data["pin"] = hashlib.sha256(
            new_pin.encode()).hexdigest()
        self.save()

vault = VaultSystem()

class BrayoOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v2.0")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("1280x720+0+0")
        self.vault_unlocked = False
        self.build_desktop()
        self.root.mainloop()

BG_COLOR = "#0D0D0D"
TASKBAR_BG = "#1A1A1A"

class BrayoOSDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v2.0")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("1280x720+0+0")
        self.vault_unlocked = False
        self.build_desktop()
        self.root.mainloop()

    def build_desktop(self):
        import time

        # TOP BAR
        topbar = tk.Frame(self.root,
                         bg=TASKBAR_BG, height=35)
        topbar.pack(side=tk.TOP, fill=tk.X)
        topbar.pack_propagate(False)

        tk.Label(topbar, text="⚡ BrayoOS v2.0",
                bg=TASKBAR_BG, fg=ACCENT,
                font=("monospace", 11,
                      "bold")).pack(
                    side=tk.LEFT, padx=10)

        self.clock = tk.Label(topbar, text="",
                             bg=TASKBAR_BG,
                             fg=TEXT,
                             font=("monospace", 10))
        self.clock.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

        # MAIN
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main,
                text="⚡ BrayoOS Desktop",
                bg=BG_COLOR, fg=ACCENT,
                font=("monospace", 14,
                      "bold")).pack(pady=8)

        # Scrollable canvas
        canvas = tk.Canvas(main, bg=BG_COLOR,
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(
            main, orient="vertical",
            command=canvas.yview)
        canvas.configure(
            yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT,
                   fill=tk.BOTH, expand=True)

        self.app_frame = tk.Frame(canvas,
                                 bg=BG_COLOR)
        canvas.create_window(
            (0, 0), window=self.app_frame,
            anchor="nw")

        self.show_apps()

        self.app_frame.update_idletasks()
        canvas.configure(
            scrollregion=canvas.bbox("all"))

        # BOTTOM TASKBAR
        taskbar = tk.Frame(self.root,
                          bg=TASKBAR_BG,
                          height=50)
        taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        taskbar.pack_propagate(False)

        tk.Button(taskbar,
                 text="🤖 AIRA",
                 bg=ACCENT, fg=BG_COLOR,
                 font=("monospace", 10, "bold"),
                 relief=tk.FLAT,
                 command=lambda: self.launch(
                     "aira.py"),
                 cursor="hand2").pack(
                     side=tk.LEFT,
                     padx=10, pady=8)

        # Vault button
        self.vault_btn = tk.Button(
            taskbar,
            text="🔒 Vault",
            bg=DARK, fg=RED,
            font=("monospace", 10),
            relief=tk.FLAT,
            command=self.toggle_vault,
            cursor="hand2")
        self.vault_btn.pack(
            side=tk.LEFT, padx=5, pady=8)

        # Status
        self.vault_status = tk.Label(
            taskbar,
            text="🔒 Vault Locked",
            bg=TASKBAR_BG, fg=RED,
            font=("monospace", 9))
        self.vault_status.pack(
            side=tk.RIGHT, padx=10)

        self.aira_label = tk.Label(
            taskbar,
            text="🤖 AIRA: Online",
            bg=TASKBAR_BG, fg=ACCENT,
            font=("monospace", 9))
        self.aira_label.pack(
            side=tk.RIGHT, padx=10)
        self.pulse_aira()

    def show_apps(self):
        for w in self.app_frame.winfo_children():
            w.destroy()

        # Show public apps always
        apps = PUBLIC_APPS.copy()

        # Show hidden apps only if vault unlocked
        if self.vault_unlocked:
            apps += HIDDEN_APPS

        row, col = 0, 0
        for name, script in apps:
            # Highlight hidden apps
            is_hidden = (name, script) in HIDDEN_APPS
            bg = "#1A0A0A" if is_hidden \
                else TASKBAR_BG
            fg = RED if is_hidden else ACCENT

            btn = tk.Button(
                self.app_frame,
                text=name,
                bg=bg, fg=fg,
                font=("monospace", 8),
                relief=tk.RAISED,
                cursor="hand2",
                command=lambda s=script:
                self.launch(s),
                width=10, height=3,
                activebackground=ACCENT,
                activeforeground=BG_COLOR,
                bd=1)
            btn.grid(row=row, column=col,
                    padx=4, pady=4)
            col += 1
            if col > 5:
                col = 0
                row += 1

    def toggle_vault(self):
        if self.vault_unlocked:
            # Lock vault
            self.vault_unlocked = False
            self.vault_btn.config(
                text="🔒 Vault",
                fg=RED)
            self.vault_status.config(
                text="🔒 Vault Locked",
                fg=RED)
            self.show_apps()
        else:
            # Show PIN dialog
            self.show_pin_dialog()

    def show_pin_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("🔓 Unlock Vault")
        dialog.configure(bg=BG_COLOR)
        dialog.geometry("300x250")
        dialog.resizable(False, False)

        tk.Label(dialog,
                text="🔒 Enter Vault PIN",
                bg=BG_COLOR, fg=ACCENT,
                font=("monospace", 14,
                      "bold")).pack(pady=20)

        tk.Label(dialog,
                text=f"Hint: {vault.data['hint']}",
                bg=BG_COLOR, fg="#444444",
                font=("monospace", 9)).pack()

        pin_entry = tk.Entry(
            dialog,
            bg=DARK, fg=ACCENT,
            font=("monospace", 18),
            show="●",
            justify=tk.CENTER,
            insertbackground=ACCENT)
        pin_entry.pack(pady=15,
                      padx=20, fill=tk.X)
        pin_entry.focus()

        status = tk.Label(dialog, text="",
                         bg=BG_COLOR, fg=RED,
                         font=("monospace", 10))
        status.pack()

        def verify():
            pin = pin_entry.get()
            if vault.verify_pin(pin):
                self.vault_unlocked = True
                self.vault_btn.config(
                    text="🔓 Vault Open",
                    fg=ACCENT)
                self.vault_status.config(
                    text="🔓 Vault Unlocked",
                    fg=ACCENT)
                self.show_apps()
                dialog.destroy()
            else:
                status.config(
                    text="❌ Wrong PIN!")
                pin_entry.delete(0, tk.END)

        pin_entry.bind(
            "<Return>", lambda e: verify())

        tk.Button(dialog,
                 text="🔓 Unlock",
                 bg=ACCENT, fg=BG_COLOR,
                 font=("monospace", 11,
                       "bold"),
                 relief=tk.FLAT,
                 command=verify).pack(pady=10)

    def update_clock(self):
        import time
        self.clock.config(
            text=time.strftime("🕐 %H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def pulse_aira(self):
        current = self.aira_label.cget("fg")
        self.aira_label.config(
            fg=ACCENT if current == TASKBAR_BG
            else TASKBAR_BG)
        self.root.after(1000, self.pulse_aira)

    def launch(self, script):
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        try:
            if script == "terminal":
                subprocess.Popen(
                    ["bash"], env=env,
                    cwd=os.path.expanduser("~"))
            else:
                path = os.path.expanduser(
                    f"~/BrayoOS/apps/{script}")
                subprocess.Popen(
                    ["python", path], env=env)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    BrayoOSDesktop()
