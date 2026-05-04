#!/bin/bash
echo "🔧 Fixing all BrayoOS apps..."

# Remove old placeholder
rm -f ~/BrayoOS/apps/settings.py

# Create working settings with theme
cat > ~/BrayoOS/apps/settings.py << 'SETEOF'
import tkinter as tk
from tkinter import messagebox
import os
import subprocess

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class Settings:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚙️ Settings")
        self.root.configure(bg=BG)
        self.root.geometry("600x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="⚙️ BrayoOS Settings",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.LabelFrame(self.root, text="System Info",
                             bg=BG, fg=ACCENT,
                             font=("monospace", 11))
        frame.pack(fill=tk.X, padx=10, pady=5)

        info = [
            ("OS", "BrayoOS v2.0"),
            ("Status", "✅ Running"),
            ("Python", "3.13"),
            ("Built by", "Brayo"),
        ]

        for key, val in info:
            f = tk.Frame(frame, bg=BG)
            f.pack(fill=tk.X, padx=5, pady=3)
            tk.Label(f, text=f"{key}:", bg=BG, fg=TEXT,
                    font=("monospace", 10),
                    width=15).pack(side=tk.LEFT)
            tk.Label(f, text=val, bg=BG, fg=ACCENT,
                    font=("monospace", 10)).pack(side=tk.LEFT)

        frame2 = tk.LabelFrame(self.root, text="Actions",
                              bg=BG, fg=ACCENT,
                              font=("monospace", 11))
        frame2.pack(fill=tk.X, padx=10, pady=5)

        for text in ["🔄 Restart", "📦 Backup", "ℹ️ About"]:
            tk.Button(frame2, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 10),
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=3, pady=5)

        tk.Label(self.root, text="✅ All systems operational!",
                bg=BG, fg="#00AA00",
                font=("monospace", 12)).pack(pady=20)

if __name__ == "__main__":
    Settings()
SETEOF

# Create wallpaper
cat > ~/BrayoOS/core/create_wallpaper.py << 'WALLEOF'
from PIL import Image, ImageDraw
import os

os.makedirs(os.path.expanduser("~/BrayoOS/assets"), exist_ok=True)

# Create dark grid wallpaper
img = Image.new('RGB', (1280, 720), (13, 13, 13))
draw = ImageDraw.Draw(img)

# Draw grid lines
grid_size = 40
for x in range(0, 1280, grid_size):
    draw.line([(x, 0), (x, 720)], fill=(65, 255, 65), width=1)
for y in range(0, 720, grid_size):
    draw.line([(0, y), (1280, y)], fill=(65, 255, 65), width=1)

img.save(os.path.expanduser("~/BrayoOS/assets/wallpaper.png"))
print("✅ Wallpaper created!")
WALLEOF

python ~/BrayoOS/core/create_wallpaper.py

# Create proper desktop with wallpaper
cat > ~/BrayoOS/core/desktop.py << 'DESKEOF'
import tkinter as tk
from tkinter import ttk
import subprocess
import os
from PIL import Image, ImageTk

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
        
        # Set wallpaper background
        try:
            wp_path = os.path.expanduser("~/BrayoOS/assets/wallpaper.png")
            if os.path.exists(wp_path):
                img = Image.open(wp_path)
                self.bg_image = ImageTk.PhotoImage(img)
                bg_label = tk.Label(self.root, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass

        self.build_desktop()
        self.root.mainloop()

    def build_desktop(self):
        # Taskbar
        self.taskbar = tk.Frame(self.root, bg=TASKBAR_BG, height=50)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(self.taskbar, text="⚡ BrayoOS v2.0",
                bg=TASKBAR_BG, fg=ACCENT,
                font=("monospace", 12, "bold")).pack(side=tk.LEFT, padx=10)

        # Desktop area
        self.desktop = tk.Frame(self.root, bg="", relief=tk.FLAT)
        self.desktop.pack(fill=tk.BOTH, expand=True)
        self.desktop.configure(bg="")

        tk.Label(self.desktop,
                text="⚡ BrayoOS Desktop",
                bg="", fg=ACCENT,
                font=("monospace", 18, "bold")).pack(pady=20)

        # App buttons
        grid = tk.Frame(self.desktop, bg="")
        grid.pack(expand=True)

        apps = [
            ("🖥️ Terminal", "terminal"),
            ("🤖 AI Chat", "ai_chat.py"),
            ("🌐 Browser", "mini_browser.py"),
            ("📁 Files", "files.py"),
            ("🌐 Network", "network.py"),
            ("📊 System", "system_monitor.py"),
            ("🔐 Passwords", "password_manager.py"),
            ("🌍 IP Tracker", "ip_tracker.py"),
            ("🎵 Music", "music_player.py"),
            ("📱 SMS", "sms_reader.py"),
            ("🛡️ Scan", "vuln_scanner.py"),
            ("⚙️ Settings", "settings.py"),
        ]

        row, col = 0, 0
        for name, script in apps:
            tk.Button(grid, text=name,
                     bg=TASKBAR_BG, fg=ACCENT,
                     font=("monospace", 10),
                     relief=tk.FLAT, cursor="hand2",
                     command=lambda s=script: self.launch(s),
                     width=14, height=3,
                     activebackground=ACCENT,
                     activeforeground=BG_COLOR).grid(
                         row=row, column=col,
                         padx=8, pady=8)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def launch(self, script):
        if script == "terminal":
            subprocess.Popen(["bash"])
        else:
            path = os.path.expanduser(f"~/BrayoOS/apps/{script}")
            subprocess.Popen(["python", path])

if __name__ == "__main__":
    BrayoOS()
DESKEOF

echo "✅ All apps fixed and wallpaper created!"
