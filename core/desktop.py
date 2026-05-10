import tkinter as tk
import subprocess
import os
import time

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
RED = "#FF4444"

PUBLIC_APPS = [
    ("🖥️\nTerminal", "terminal"),
    ("🤖\nVirgy", "virgy_max.py"),
    ("🌐\nBrowser", "mini_browser.py"),
    ("📁\nFiles", "files.py"),
    ("🎵\nMusic", "music_player.py"),
    ("📱\nSMS", "sms_reader.py"),
    ("👥\nContacts", "contacts.py"),
    ("💰\nCrypto", "crypto_tracker.py"),
    ("🌤️\nWeather", "weather.py"),
    ("📰\nNews", "hackernews.py"),
    ("📊\nTasks", "task_manager.py"),
    ("🔢\nCalc", "calculator.py"),
    ("📝\nEditor", "text_editor.py"),
    ("🕐\nClock", "clock.py"),
    ("🖼️\nImages", "image_viewer.py"),
    ("💾\nBackup", "backup.py"),
    ("📖\nOur Story", "our_story.py"),
    ("⚙️\nSettings", "settings.py"),
    ("🏪\nApp Store", "app_store.py"),
    ("👤\nUsers", "user_manager.py"),
    ("🔄\nUpdater", "brayos_updater.py"),
    ("🤖\nVirgy AI", "aria_voice.py"),
    ("💀\nDark Web", "dark_web_monitor.py"),
    ("🧠\nVirgy Neural", "virgy_neural_core.py"),
    ("👁️\nGhost Mode", "ghost_mode.py"),
    ("🔐\nDNA Vault", "dna_vault.py"),
    ("📡\nSignal", "signal_interceptor.py"),
    ("🎭\nIdentity", "identity_switcher.py"),
    ("⚡\nOverclock", "overclock_dashboard.py"),
    ("🔴\nThreat Map", "live_threat_map.py"),
    ("🧬\nSelf-Heal", "self_healing.py"),
    ("🖼️\nWallpaper", "wallpaper_changer.py"),
]

HIDDEN_APPS = [
    ("🛡️\nVuln Scan", "vuln_scanner.py"),
    ("🌐\nNetwork", "network.py"),
    ("📡\nWiFi", "wifi_manager.py"),
    ("🌍\nIP Track", "ip_tracker.py"),
    ("🔐\nPasswords", "password_manager.py"),
    ("📦\nPkg Mgr", "package_manager.py"),
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
    ("🔒\nHash Crack", "hash_cracker.py"),
]

class BrayoOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v2.0")
        self.root.configure(bg=BG)
        self.root.geometry("1280x720+0+0")
        self.root.focus_force()
        self.vault_open = False
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        # Top bar
        topbar = tk.Frame(self.root,
                         bg=DARK, height=35)
        topbar.pack(side=tk.TOP, fill=tk.X)
        topbar.pack_propagate(False)

        tk.Label(topbar,
                text="⚡ BrayoOS v2.0",
                bg=DARK, fg=ACCENT,
                font=("monospace", 11,
                      "bold")).pack(
                    side=tk.LEFT, padx=10)

        self.clock = tk.Label(topbar,
                             text="",
                             bg=DARK, fg=TEXT,
                             font=("monospace", 10))
        self.clock.pack(side=tk.RIGHT, padx=10)
        self.tick()

        # Main canvas with scroll
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main, bg=BG,
                               highlightthickness=0)
        scroll = tk.Scrollbar(main,
                             orient="vertical",
                             command=self.canvas.yview)
        self.canvas.configure(
            yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT,
                        fill=tk.BOTH, expand=True)

        self.app_frame = tk.Frame(
            self.canvas, bg=BG)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.app_frame,
            anchor="nw")

        self.app_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))

        # Bottom taskbar
        taskbar = tk.Frame(self.root,
                          bg=DARK, height=50)
        taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        taskbar.pack_propagate(False)

        tk.Button(taskbar,
                 text="🤖 Virgy",
                 bg=ACCENT, fg=BG,
                 font=("monospace", 10, "bold"),
                 relief=tk.FLAT,
                 command=lambda: self.launch(
                     "virgy_max.py"),
                 cursor="hand2").pack(
                     side=tk.LEFT,
                     padx=10, pady=8)

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

        for name, script in [
            ("🖥️ Terminal", "terminal"),
            ("🌐 Network", "network.py"),
            ("📊 Tasks", "task_manager.py"),
        ]:
            tk.Button(taskbar, text=name,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     relief=tk.FLAT,
                     command=lambda s=script:
                     self.launch(s),
                     cursor="hand2").pack(
                         side=tk.LEFT,
                         padx=3, pady=8)

        self.virgy_lbl = tk.Label(
            taskbar,
            text="🤖 Virgy: Online",
            bg=DARK, fg=ACCENT,
            font=("monospace", 9))
        self.virgy_lbl.pack(
            side=tk.RIGHT, padx=10)
        self.pulse()

        self.load_apps()

    def load_apps(self):
        for w in self.app_frame.winfo_children():
            w.destroy()

        apps = PUBLIC_APPS.copy()
        if self.vault_open:
            apps += HIDDEN_APPS

        row, col = 0, 0
        for name, script in apps:
            is_hidden = (name, script) in \
                       HIDDEN_APPS
            bg = "#1A0505" if is_hidden \
                else DARK
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
                width=10, height=4,
                activebackground=ACCENT,
                activeforeground=BG,
                bd=2)
            btn.grid(row=row, column=col,
                    padx=5, pady=5)
            col += 1
            if col > 5:
                col = 0
                row += 1

        self.app_frame.update_idletasks()
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"))

    def toggle_vault(self):
        if self.vault_open:
            self.vault_open = False
            self.vault_btn.config(
                text="🔒 Vault", fg=RED)
            self.load_apps()
        else:
            self.ask_pin()

    def ask_pin(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("🔓 Vault PIN")
        dialog.configure(bg=BG)
        dialog.geometry("280x200")
        dialog.focus_force()

        tk.Label(dialog,
                text="Enter PIN:",
                bg=BG, fg=ACCENT,
                font=("monospace", 14,
                      "bold")).pack(pady=15)

        pin = tk.Entry(dialog,
                      bg=DARK, fg=ACCENT,
                      font=("monospace", 18),
                      show="●",
                      justify=tk.CENTER,
                      insertbackground=ACCENT)
        pin.pack(padx=20, fill=tk.X)
        pin.focus()

        msg = tk.Label(dialog, text="",
                      bg=BG, fg=RED,
                      font=("monospace", 10))
        msg.pack(pady=5)

        def check():
            if pin.get() == "1337":
                self.vault_open = True
                self.vault_btn.config(
                    text="🔓 Vault", fg=ACCENT)
                self.load_apps()
                dialog.destroy()
            else:
                msg.config(text="❌ Wrong PIN!")
                pin.delete(0, tk.END)

        pin.bind("<Return>", lambda e: check())
        tk.Button(dialog,
                 text="🔓 Unlock",
                 bg=ACCENT, fg=BG,
                 font=("monospace", 11),
                 relief=tk.FLAT,
                 command=check).pack(pady=10)

    def tick(self):
        self.clock.config(
            text=time.strftime("🕐 %H:%M:%S"))
        self.root.after(1000, self.tick)

    def pulse(self):
        fg = self.virgy_lbl.cget("fg")
        self.virgy_lbl.config(
            fg=ACCENT if fg == DARK else DARK)
        self.root.after(1000, self.pulse)

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
    BrayoOS()

# BrayoOS Apps v2.0 — Added by Virgy
APPS_V2 = [
    ("🧠 Virgy Neural", "virgy_neural_core.py"),
    ("👁️ Ghost Mode", "ghost_mode.py"),
    ("🔐 DNA Vault", "dna_vault.py"),
    ("📡 Signal Interceptor", "signal_interceptor.py"),
    ("🎭 Identity Switcher", "identity_switcher.py"),
    ("⚡ Overclock", "overclock_dashboard.py"),
    ("🖼️ Wallpaper", "wallpaper_changer.py"),
]

import subprocess, os
for name, script in APPS_V2:
    path = os.path.expanduser(f"~/BrayoOS/core/apps/{script}")
    if os.path.exists(path):
        print(f"✅ Registered: {name}")
