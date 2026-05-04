#!/bin/bash
echo "⚡ Completing BrayoOS Phase 1..."

# 1. Boot Animation with ARIA
cat > ~/BrayoOS/core/boot.py << 'BOOTEOF'
import tkinter as tk
import time
import threading
import subprocess
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class BootScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS Boot")
        self.root.configure(bg=BG)
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        self.build_ui()
        threading.Thread(target=self.boot_sequence,
                        daemon=True).start()
        self.root.mainloop()

    def build_ui(self):
        self.canvas = tk.Canvas(self.root, bg=BG,
                               highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Logo
        self.canvas.create_text(640, 150,
            text="██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗\n"
                 "██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝\n"
                 "██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗\n"
                 "██╔══██╗██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║\n"
                 "██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║\n"
                 "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝",
            font=("monospace", 7, "bold"),
            fill=ACCENT, justify=tk.CENTER)

        self.canvas.create_text(640, 300,
            text="⚡ Built by Brayo & ARIA (Claude) — 2026",
            font=("monospace", 13),
            fill=TEXT)

        self.canvas.create_text(640, 330,
            text="Two minds. One OS.",
            font=("monospace", 11),
            fill="#444444")

        # Progress bar background
        self.canvas.create_rectangle(
            240, 380, 1040, 405,
            outline=ACCENT, fill=DARK)

        # Progress bar fill
        self.progress = self.canvas.create_rectangle(
            240, 380, 240, 405,
            outline="", fill=ACCENT)

        # Status text
        self.status_text = self.canvas.create_text(
            640, 430,
            text="Initializing...",
            font=("monospace", 11),
            fill=ACCENT)

        # Log area
        self.log_text = self.canvas.create_text(
            640, 550,
            text="",
            font=("monospace", 9),
            fill="#333333",
            justify=tk.CENTER)

        # ARIA status
        self.aria_text = self.canvas.create_text(
            640, 620,
            text="",
            font=("monospace", 12, "bold"),
            fill=ACCENT)

    def update_progress(self, pct, status):
        x = 240 + (800 * pct // 100)
        self.canvas.coords(self.progress,
                          240, 380, x, 405)
        self.canvas.itemconfig(
            self.status_text, text=status)
        self.root.update()

    def update_log(self, msg):
        self.canvas.itemconfig(
            self.log_text, text=msg)
        self.root.update()

    def update_aria(self, msg):
        self.canvas.itemconfig(
            self.aria_text, text=msg)
        self.root.update()

    def boot_sequence(self):
        steps = [
            (5,  "Loading kernel modules...",
             "[ OK ] kernel modules loaded"),
            (15, "Initializing hardware...",
             "[ OK ] hardware initialized"),
            (25, "Mounting filesystems...",
             "[ OK ] filesystems mounted"),
            (35, "Starting network services...",
             "[ OK ] network services started"),
            (45, "Loading BrayoOS core...",
             "[ OK ] BrayoOS core loaded"),
            (55, "Initializing ARIA...",
             "[ OK ] ARIA intelligence online"),
            (65, "Loading security modules...",
             "[ OK ] security modules active"),
            (75, "Starting display server...",
             "[ OK ] display server running"),
            (85, "Loading desktop environment...",
             "[ OK ] desktop environment ready"),
            (95, "Applying user preferences...",
             "[ OK ] preferences applied"),
            (100,"Boot complete!",
             "[ OK ] BrayoOS ready"),
        ]

        for pct, status, log in steps:
            time.sleep(0.4)
            self.update_progress(pct, status)
            self.update_log(log)

            if pct == 55:
                self.update_aria(
                    "🤖 ARIA: Initializing...")
            elif pct == 65:
                self.update_aria(
                    "🤖 ARIA: Security modules loaded...")
            elif pct == 100:
                self.update_aria(
                    "🤖 ARIA: Online. Ready, Brayo.")

        time.sleep(1.5)
        self.root.destroy()
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        subprocess.Popen([
            "python",
            os.path.expanduser("~/BrayoOS/core/desktop.py")
        ], env=env)

if __name__ == "__main__":
    BootScreen()
BOOTEOF

# 2. Auto-start on Termux launch
cat > ~/.bashrc_brayos << 'AUTOEOF'
# BrayoOS Auto-start
export GROQ_API_KEY=$(grep GROQ_API_KEY ~/.bashrc | tail -1 | cut -d'"' -f2)
export DISPLAY=:1
alias brayos="bash ~/start_brayos.sh"
alias aria="DISPLAY=:1 python ~/BrayoOS/apps/aria.py"
alias bstop="pkill -f desktop.py; vncserver -kill :1"
echo "⚡ BrayoOS environment loaded!"
echo "Type 'brayos' to start | 'aria' for AI | 'bstop' to stop"
AUTOEOF

# Add to bashrc if not already there
grep -q "bashrc_brayos" ~/.bashrc || \
    echo "source ~/.bashrc_brayos" >> ~/.bashrc

# 3. Updated desktop with ARIA in taskbar
cat > ~/BrayoOS/core/desktop.py << 'DESKEOF'
import tkinter as tk
import subprocess
import os
import time
from PIL import Image, ImageTk

BG_COLOR = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
TASKBAR_BG = "#1A1A1A"
DARK = "#111111"

class BrayoOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v2.0")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("1280x720+0+0")

        # Wallpaper
        try:
            wp = os.path.expanduser(
                "~/BrayoOS/assets/wallpaper.png")
            if os.path.exists(wp):
                img = Image.open(wp).resize((1280, 720))
                self.bg = ImageTk.PhotoImage(img)
                tk.Label(self.root,
                        image=self.bg).place(
                            x=0, y=0,
                            relwidth=1, relheight=1)
        except:
            pass

        self.build_desktop()
        self.root.mainloop()

    def build_desktop(self):
        # TOP BAR
        topbar = tk.Frame(self.root,
                         bg=TASKBAR_BG, height=35)
        topbar.pack(side=tk.TOP, fill=tk.X)
        topbar.pack_propagate(False)

        tk.Label(topbar, text="⚡ BrayoOS v2.0",
                bg=TASKBAR_BG, fg=ACCENT,
                font=("monospace", 11,
                      "bold")).pack(side=tk.LEFT,
                                   padx=10)

        self.clock = tk.Label(topbar, text="",
                             bg=TASKBAR_BG, fg=TEXT,
                             font=("monospace", 10))
        self.clock.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

        # Battery/Network indicators
        tk.Label(topbar, text="📶 WiFi",
                bg=TASKBAR_BG, fg=TEXT,
                font=("monospace", 9)).pack(
                    side=tk.RIGHT, padx=5)

        # MAIN AREA
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(main,
                text="⚡ BrayoOS Desktop",
                bg=BG_COLOR, fg=ACCENT,
                font=("monospace", 16,
                      "bold")).pack(pady=10)

        # App grid
        grid = tk.Frame(main, bg=BG_COLOR)
        grid.pack(expand=True)

        apps = [
            ("🖥️\nTerminal", "terminal"),
            ("🤖\nARIA", "aria.py"),
            ("🌐\nBrowser", "mini_browser.py"),
            ("📁\nFiles", "files.py"),
            ("🌐\nNetwork", "network.py"),
            ("📊\nSystem", "system_monitor.py"),
            ("📡\nWiFi", "wifi_manager.py"),
            ("🌍\nIP Track", "ip_tracker.py"),
            ("🛡️\nVuln Scan", "vuln_scanner.py"),
            ("🔐\nPasswords", "password_manager.py"),
            ("📦\nApp Store", "app_store.py"),
            ("💻\nCode", "code_editor.py"),
            ("🎵\nMusic", "music_player.py"),
            ("📱\nSMS", "sms_reader.py"),
            ("👥\nContacts", "contacts.py"),
            ("💰\nCrypto", "crypto_tracker.py"),
            ("🌤️\nWeather", "weather.py"),
            ("📰\nNews", "hackernews.py"),
            ("🤖\nTelegram", "telegram_bot.py"),
            ("🔒\nSecurity", "security_monitor.py"),
            ("🔀\nPort Fwd", "port_forwarder.py"),
            ("🔑\nHash", "hash_cracker.py"),
            ("🌐\nSubdomain", "subdomain_scanner.py"),
            ("🔍\nDNS", "dns_lookup.py"),
            ("💣\nPayloads", "payload_generator.py"),
            ("⚙️\nSettings", "settings.py"),
        ]

        row, col = 0, 0
        for name, script in apps:
            btn = tk.Button(grid,
                     text=name,
                     bg=TASKBAR_BG,
                     fg=ACCENT,
                     font=("monospace", 8),
                     relief=tk.RAISED,
                     cursor="hand2",
                     command=lambda s=script: self.launch(s),
                     width=9, height=3,
                     activebackground=ACCENT,
                     activeforeground=BG_COLOR,
                     bd=1)
            btn.grid(row=row, column=col,
                    padx=4, pady=4)
            col += 1
            if col > 6:
                col = 0
                row += 1

        # BOTTOM TASKBAR WITH ARIA
        taskbar = tk.Frame(self.root,
                          bg=TASKBAR_BG, height=45)
        taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        taskbar.pack_propagate(False)

        # ARIA button in taskbar
        tk.Button(taskbar,
                 text="🤖 Ask ARIA",
                 bg=ACCENT, fg=BG_COLOR,
                 font=("monospace", 10, "bold"),
                 relief=tk.FLAT,
                 command=lambda: self.launch("aria.py"),
                 cursor="hand2").pack(
                     side=tk.LEFT, padx=10, pady=5)

        # Quick launch buttons
        for name, script in [
            ("🖥️ Terminal", "terminal"),
            ("🌐 Network", "network.py"),
            ("🛡️ Scan", "vuln_scanner.py"),
            ("📊 System", "system_monitor.py"),
        ]:
            tk.Button(taskbar, text=name,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     relief=tk.FLAT,
                     command=lambda s=script: self.launch(s),
                     cursor="hand2").pack(
                         side=tk.LEFT, padx=3, pady=5)

        # ARIA status indicator
        self.aria_status = tk.Label(
            taskbar,
            text="🤖 ARIA: Online",
            bg=TASKBAR_BG, fg=ACCENT,
            font=("monospace", 9))
        self.aria_status.pack(side=tk.RIGHT, padx=10)
        self.pulse_aria()

    def pulse_aria(self):
        current = self.aria_status.cget("fg")
        self.aria_status.config(
            fg=ACCENT if current == TASKBAR_BG
            else TASKBAR_BG)
        self.root.after(1000, self.pulse_aria)

    def update_clock(self):
        self.clock.config(
            text=time.strftime("🕐 %H:%M:%S  📅 %d/%m/%Y"))
        self.root.after(1000, self.update_clock)

    def launch(self, script):
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        if script == "terminal":
            subprocess.Popen(["bash"], env=env,
                           cwd=os.path.expanduser("~"))
        else:
            path = os.path.expanduser(
                f"~/BrayoOS/apps/{script}")
            subprocess.Popen(["python", path], env=env)

if __name__ == "__main__":
    BrayoOS()
DESKEOF

# 4. Backup system
cat > ~/BrayoOS/apps/backup.py << 'BAKEOF'
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os
import time

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class BackupSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💾 Backup System")
        self.root.configure(bg=BG)
        self.root.geometry("600x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="💾 BrayoOS Backup",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        for text, cmd in [
            ("💾 Backup Now", self.backup),
            ("📦 Backup To SD", self.backup_sd),
            ("🔄 Restore", self.restore),
            ("📋 List Backups", self.list_backups),
        ]:
            tk.Button(self.root, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 11),
                     command=cmd,
                     relief=tk.FLAT,
                     width=20).pack(pady=5)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def backup(self):
        self.log("💾 Creating backup...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.expanduser(
            f"~/BrayoOS/backups/backup_{timestamp}.zip")
        os.makedirs(os.path.expanduser(
            "~/BrayoOS/backups"), exist_ok=True)
        result = subprocess.run([
            "zip", "-r", backup_file,
            os.path.expanduser("~/BrayoOS/")
        ], capture_output=True, text=True)
        if result.returncode == 0:
            self.log(f"✅ Backup saved: {backup_file}")
        else:
            self.log(f"❌ Error: {result.stderr}")

    def backup_sd(self):
        self.log("📦 Backing up to SD card...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = f"/sdcard/BrayoOS_backup_{timestamp}.zip"
        result = subprocess.run([
            "zip", "-r", backup_file,
            os.path.expanduser("~/BrayoOS/")
        ], capture_output=True, text=True)
        if result.returncode == 0:
            self.log(f"✅ Backup saved to SD: {backup_file}")
        else:
            self.log(f"❌ Error: {result.stderr}")

    def restore(self):
        self.log("🔄 Listing available backups...")
        self.list_backups()
        self.log("\nTo restore, run in terminal:")
        self.log("unzip ~/BrayoOS/backups/[backup_file] -d ~/")

    def list_backups(self):
        backup_dir = os.path.expanduser("~/BrayoOS/backups")
        os.makedirs(backup_dir, exist_ok=True)
        backups = os.listdir(backup_dir)
        if backups:
            self.log("📋 Available backups:")
            for b in backups:
                self.log(f"  📦 {b}")
        else:
            self.log("❌ No backups found!")

if __name__ == "__main__":
    BackupSystem()
BAKEOF

# 5. Update system
cat > ~/BrayoOS/apps/updater.py << 'UPDEOF'
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import httpx

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

CURRENT_VERSION = "2.0"

class Updater:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔄 BrayoOS Updater")
        self.root.configure(bg=BG)
        self.root.geometry("600x400")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔄 BrayoOS Updater",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        tk.Label(self.root,
                text=f"Current Version: {CURRENT_VERSION}",
                bg=BG, fg=TEXT,
                font=("monospace", 11)).pack()

        for text, cmd in [
            ("🔍 Check Updates", self.check_updates),
            ("📦 Update Packages", self.update_packages),
            ("🐍 Update Python Libs", self.update_python),
            ("⚡ Full System Update", self.full_update),
        ]:
            tk.Button(self.root, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 11),
                     command=cmd,
                     relief=tk.FLAT,
                     width=25).pack(pady=5)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def check_updates(self):
        self.log("🔍 Checking for updates...")
        self.log(f"✅ Current: BrayoOS v{CURRENT_VERSION}")
        self.log("📡 Checking Termux packages...")
        def run():
            result = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True, text=True)
            self.log(result.stdout or "✅ All up to date!")
        threading.Thread(target=run).start()

    def update_packages(self):
        self.log("📦 Updating packages...")
        def run():
            result = subprocess.run(
                ["pkg", "upgrade", "-y"],
                capture_output=True, text=True)
            self.log(result.stdout)
            self.log("✅ Packages updated!")
        threading.Thread(target=run).start()

    def update_python(self):
        self.log("🐍 Updating Python libraries...")
        def run():
            libs = ["httpx", "requests",
                   "flask", "pillow"]
            for lib in libs:
                result = subprocess.run(
                    ["pip", "install", "--upgrade",
                     lib, "--break-system-packages"],
                    capture_output=True, text=True)
                self.log(f"✅ {lib} updated")
        threading.Thread(target=run).start()

    def full_update(self):
        self.log("⚡ Starting full system update...")
        self.check_updates()
        self.root.after(2000, self.update_packages)
        self.root.after(5000, self.update_python)

if __name__ == "__main__":
    Updater()
UPDEOF

# Add backup and updater to desktop
sed -i 's/("⚙️\\nSettings", "settings.py"),/("⚙️\\nSettings", "settings.py"),\n            ("💾\\nBackup", "backup.py"),\n            ("🔄\\nUpdater", "updater.py"),/' ~/BrayoOS/core/desktop.py

# 6. Start script
cat > ~/start_brayos.sh << 'STARTEOF'
#!/bin/bash
source ~/.bashrc
pkill -f "python.*desktop" 2>/dev/null
pkill -f "python.*boot" 2>/dev/null
pkill -f Xtigervnc 2>/dev/null
sleep 1
rm -f /data/data/com.termux/files/usr/tmp/.X1-lock
rm -f /data/data/com.termux/files/usr/tmp/.X11-unix/X1
sleep 1
vncserver :1 -geometry 1280x720 -depth 24 \
    -localhost -SecurityTypes None
sleep 3
export DISPLAY=:1
python ~/BrayoOS/core/boot.py &
sleep 1
echo "✅ BrayoOS Ready!"
echo "📱 Connect VNC → 127.0.0.1:5901"
STARTEOF
chmod +x ~/start_brayos.sh

echo "✅ Phase 1 COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Apps: 28"
echo "Features: Boot Anim, ARIA, Taskbar, Auto-start, Backup, Updater"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Type 'brayos' to launch!"
