import tkinter as tk
import subprocess
import os
import time
import threading

BG_COLOR = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
TASKBAR_BG = "#1A1A1A"

class BrayoOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v2.0")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("1280x720+0+0")
        self.root.resizable(True, True)
        
        # Force focus
        self.root.focus_force()
        self.root.lift()
        
        self.build_desktop()
        
        # Keep alive
        self.root.protocol("WM_DELETE_WINDOW",
                          self.on_close)
        self.root.mainloop()

    def on_close(self):
        pass

    def build_desktop(self):
        # TOP BAR
        topbar = tk.Frame(self.root,
                         bg=TASKBAR_BG, height=35)
        topbar.pack(side=tk.TOP, fill=tk.X)
        topbar.pack_propagate(False)

        tk.Label(topbar, text="⚡ BrayoOS v2.0",
                bg=TASKBAR_BG, fg=ACCENT,
                font=("monospace", 11, "bold")).pack(
                    side=tk.LEFT, padx=10)

        self.clock = tk.Label(topbar, text="",
                             bg=TASKBAR_BG, fg=TEXT,
                             font=("monospace", 10))
        self.clock.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

        # MAIN AREA
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(main,
                text="⚡ BrayoOS Desktop",
                bg=BG_COLOR, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(
                    pady=10)

        # Scrollable canvas
        canvas = tk.Canvas(main, bg=BG_COLOR,
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(main,
                                orient="vertical",
                                command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH,
                   expand=True)

        # App frame inside canvas
        app_frame = tk.Frame(canvas, bg=BG_COLOR)
        canvas.create_window((0, 0),
                            window=app_frame,
                            anchor="nw")

        apps = [
            ("🖥️ Terminal", "terminal"),
            ("🤖 ARIA", "aria.py"),
            ("🌐 Browser", "mini_browser.py"),
            ("📁 Files", "files.py"),
            ("🌐 Network", "network.py"),
            ("📊 System", "system_monitor.py"),
            ("📡 WiFi", "wifi_manager.py"),
            ("🌍 IP Track", "ip_tracker.py"),
            ("🛡️ Vuln Scan", "vuln_scanner.py"),
            ("🔐 Passwords", "password_manager.py"),
            ("📦 App Store", "app_store.py"),
            ("💻 Code", "code_editor.py"),
            ("🎵 Music", "music_player.py"),
            ("📱 SMS", "sms_reader.py"),
            ("👥 Contacts", "contacts.py"),
            ("💰 Crypto", "crypto_tracker.py"),
            ("🌤️ Weather", "weather.py"),
            ("📰 News", "hackernews.py"),
            ("🤖 Telegram", "telegram_bot.py"),
            ("🔒 Security", "security_monitor.py"),
            ("🔀 Port Fwd", "port_forwarder.py"),
            ("🔑 Hash", "hash_cracker.py"),
            ("🌐 Subdomain", "subdomain_scanner.py"),
            ("🔍 DNS", "dns_lookup.py"),
            ("💣 Payloads", "payload_generator.py"),
            ("🔍 OSINT", "social_osint.py"),
            ("💀 MSF", "metasploit_helper.py"),
            ("🗺️ Net Map", "network_mapper.py"),
            ("📡 Sniffer", "packet_sniffer.py"),
            ("🔍 Procs", "process_monitor.py"),
            ("📡 WiFi+", "wifi_cracker.py"),
            ("💾 Backup", "backup.py"),
            ("🔄 Updater", "updater.py"),
            ("⚙️ Settings", "settings.py"),
            ("📖 Our Story", "our_story.py"),
            ("🛡️ Privacy", "privacy_shield.py"),
        ]

        row, col = 0, 0
        for name, script in apps:
            btn = tk.Button(app_frame,
                     text=name,
                     bg=TASKBAR_BG,
                     fg=ACCENT,
                     font=("monospace", 9),
                     relief=tk.RAISED,
                     cursor="hand2",
                     command=lambda s=script: self.launch(s),
                     width=12, height=3,
                     activebackground=ACCENT,
                     activeforeground=BG_COLOR,
                     bd=2)
            btn.grid(row=row, column=col,
                    padx=5, pady=5)
            col += 1
            if col > 4:
                col = 0
                row += 1

        # Update scroll region
        app_frame.update_idletasks()
        canvas.configure(
            scrollregion=canvas.bbox("all"))

        # BOTTOM TASKBAR
        taskbar = tk.Frame(self.root,
                          bg=TASKBAR_BG, height=45)
        taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        taskbar.pack_propagate(False)

        tk.Button(taskbar,
                 text="🤖 ARIA",
                 bg=ACCENT, fg=BG_COLOR,
                 font=("monospace", 10, "bold"),
                 relief=tk.FLAT,
                 command=lambda: self.launch("aria.py"),
                 cursor="hand2").pack(
                     side=tk.LEFT, padx=10, pady=5)

        for name, script in [
            ("🖥️ Terminal", "terminal"),
            ("🌐 Network", "network.py"),
            ("🛡️ Scan", "vuln_scanner.py"),
            ("📊 System", "system_monitor.py"),
            ("💾 Backup", "backup.py"),
        ]:
            tk.Button(taskbar, text=name,
                     bg=TASKBAR_BG, fg=ACCENT,
                     font=("monospace", 9),
                     relief=tk.FLAT,
                     command=lambda s=script: self.launch(s),
                     cursor="hand2").pack(
                         side=tk.LEFT, padx=3, pady=5)

        self.aria_label = tk.Label(
            taskbar,
            text="🤖 ARIA: Online",
            bg=TASKBAR_BG, fg=ACCENT,
            font=("monospace", 9))
        self.aria_label.pack(side=tk.RIGHT, padx=10)
        self.pulse_aria()

    def pulse_aria(self):
        current = self.aria_label.cget("fg")
        self.aria_label.config(
            fg=ACCENT if current == TASKBAR_BG
            else TASKBAR_BG)
        self.root.after(1000, self.pulse_aria)

    def update_clock(self):
        self.clock.config(
            text=time.strftime("🕐 %H:%M:%S"))
        self.root.after(1000, self.update_clock)

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
            print(f"Launch error: {e}")

if __name__ == "__main__":
    BrayoOS()
