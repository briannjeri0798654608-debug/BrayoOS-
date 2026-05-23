import tkinter as tk
import subprocess
import os
import threading
import time
from datetime import datetime

# ── THEME ─────────────────────────────────────────
BG        = "#080810"
BG2       = "#0D0D1A"
BG3       = "#12122A"
PURPLE    = "#9D00FF"
PURPLE2   = "#6A0DAD"
PURPLE3   = "#3D0066"
NEON      = "#CC44FF"
NEON2     = "#FF44FF"
WHITE     = "#E0E0FF"
DIM       = "#444466"
GLOW      = "#7700CC"
APPS = [
    ("⌨", "Terminal",  "terminal",             "#9D00FF"),
    ("★", "AIRA AI",   "aria_voice.py",         "#FF44FF"),
    ("◈", "Neural",    "aria_neural_core.py",   "#CC44FF"),
    ("◉", "Ghost",     "ghost_mode.py",         "#44FFCC"),
    ("▣", "Vault",     "dna_vault.py",          "#FFD700"),
    ("◎", "Signal",    "signal_interceptor.py", "#44CCFF"),
    ("◆", "Identity",  "identity_switcher.py",  "#FF6644"),
    ("▲", "Overclock", "overclock_dashboard.py","#FF4444"),
    ("●", "Threats",   "live_threat_map.py",    "#FF0044"),
    ("🎨", "AI Images", "ai_image_gen.py", "#FF44FF"),
    ("📡", "eSIM", "esim_manager.py", "#44FFFF"),
    ("🌐", "VPN", "vpn_engine.py", "#44FF88"),
    ("🛸", "Satellites", "satellite_tracker.py", "#44FFFF"),
    ("🔥", "Firewall", "firewall.py", "#FF0044"),
    ("🌙", "Dream Mode", "dream_mode.py", "#9D00FF"),
    ("💀", "Hack Terminal", "hack_terminal.py", "#00FF41"),
    ("📱", "Social Hub", "social_hub.py", "#1DA1F2"),
    ("📷", "Surveillance", "surveillance.py", "#FF0044"),
    ("📊", "Sys Monitor", "system_monitor.py", "#44FF88"),
    ("🎨", "Themes", "theme_changer.py", "#FF44FF"),
    ("🔐", "Adv Vault", "advanced_vault.py", "#FFD700"),
    ("📡", "Net Scan", "network_scanner.py", "#44CCFF"),
    ("🤖", "AIRA Tasks", "aira_tasks.py", "#CC44FF"),
    ("🔒", "Prox Lock", "proximity_lock.py", "#FF0044"),
    ("🌐", "Web Agent", "aira_web_agent.py",  "#00AAFF"),
    ("⊕", "Self-Heal", "self_healing.py",       "#44FF88"),
    ("▦", "Wallpaper", "wallpaper_changer.py",  "#FFAA00"),
    ("☠", "Dark Web",  "dark_web_monitor.py",   "#FF0000"),
    ("◫", "App Store", "app_store.py",          "#00AAFF"),
    ("♟", "Users",     "user_manager.py",       "#AAAAFF"),
    ("↻", "Updater",   "brayos_updater.py",     "#44FF44"),
    ("⊗", "Browser",   "browser.py",            "#44AAFF"),
    ("♫", "Music",     "music_player.py",       "#FF44AA"),
    ("▤", "Files",     "file_manager.py",       "#FFCC44"),
    ("▧", "Editor",    "editor.py",             "#88FFAA"),
    ("#", "Calc",      "calculator.py",         "#FFFF44"),
    ("◷", "Clock",     "clock.py",              "#44FFFF"),
    ("☁", "Weather",   "weather.py",            "#88AAFF"),
    ("¤", "Crypto",    "crypto.py",             "#FFD700"),
    ("▨", "News",      "news.py",               "#FF8844"),
    ("✓", "Tasks",     "tasks.py",              "#44FF44"),
    ("▯", "SMS",       "sms.py",                "#FF44FF"),
    ("♛", "Contacts",  "contacts.py",           "#FFAAFF"),
    ("▪", "Backup",    "backup.py",             "#AAFFAA"),
    ("▶", "Our Story", "our_story.py",          "#FFD700"),
    ("✦", "Settings",  "settings.py",           "#CCCCFF"),
]
CATS = {
    "ALL":      None,
    "AI":       ["aria_voice.py","aria_neural_core.py"],
    "SECURITY": ["ghost_mode.py","dna_vault.py","signal_interceptor.py",
                 "identity_switcher.py","live_threat_map.py","dark_web_monitor.py"],
    "SYSTEM":   ["overclock_dashboard.py","self_healing.py","brayos_updater.py",
                 "user_manager.py","settings.py","backup.py"],
    "TOOLS":    ["calculator.py","clock.py","editor.py","tasks.py",
                 "wallpaper_changer.py","app_store.py"],
    "MEDIA":    ["music_player.py","browser.py","weather.py","news.py","crypto.py"],
    "PERSONAL": ["sms.py","contacts.py","file_manager.py","our_story.py"],
}
class BrayoOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v4.5")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG)
        self.current_cat = "ALL"
        self.pulse_state = True
        self.build_ui()
        self.clock_tick()
        self.pulse_loop()
        self.root.mainloop()
    def build_ui(self):
        # ── TOP BAR ──────────────────────────
        top = tk.Frame(self.root, bg=BG2, height=38)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)
        # Left — logo
        logo_f = tk.Frame(top, bg=BG2)
        logo_f.pack(side="left", padx=10)
        tk.Label(logo_f, text="◈ ", font=("Courier", 13, "bold"),
                 bg=BG2, fg=PURPLE).pack(side="left")
        tk.Label(logo_f, text="BrayoOS", font=("Courier", 13, "bold"),
                 bg=BG2, fg=WHITE).pack(side="left")
        tk.Label(logo_f, text=" v4.5", font=("Courier", 9),
                 bg=BG2, fg=DIM).pack(side="left")
        # Right — clock + flag
        self.clock_lbl = tk.Label(top, text="", font=("Courier", 10),
                                   bg=BG2, fg=NEON)
        self.clock_lbl.pack(side="right", padx=12)
        tk.Label(top, text="🇰🇪", font=("Arial", 13),
                 bg=BG2).pack(side="right", padx=4)
        # AIRA pulse dot
        self.pulse_dot = tk.Label(top, text="⬤", font=("Courier", 10),
                                   bg=BG2, fg=PURPLE)
        self.pulse_dot.pack(side="right", padx=4)
        tk.Label(top, text="AIRA", font=("Courier", 9, "bold"),
                 bg=BG2, fg=DIM).pack(side="right")
        # Purple separator line
        tk.Frame(self.root, bg=PURPLE, height=2).pack(fill="x")
        # ── CATEGORY BAR ─────────────────────
        catbar = tk.Frame(self.root, bg=BG, height=34)
        catbar.pack(fill="x")
        catbar.pack_propagate(False)
        self.cat_btns = {}
        for cat in CATS:
            b = tk.Button(catbar, text=cat,
                          font=("Courier", 8, "bold"),
                          bg=BG, fg=DIM,
                          relief="flat", padx=12, pady=5,
                          activebackground=PURPLE3,
                          activeforeground=NEON,
                          bd=0,
                          command=lambda c=cat: self.switch_cat(c))
            b.pack(side="left", padx=1)
            self.cat_btns[cat] = b
        self.cat_btns["ALL"].config(bg=PURPLE3, fg=NEON)
        tk.Frame(self.root, bg=PURPLE3, height=1).pack(fill="x")
        # ── MAIN AREA ────────────────────────
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)
        # ── SIDEBAR ──────────────────────────
        side = tk.Frame(main, bg=BG2, width=145)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        # AIRA card
        aira_card = tk.Frame(side, bg=BG3)
        aira_card.pack(fill="x", padx=8, pady=10)
        tk.Label(aira_card, text="AIRA", font=("Courier", 16, "bold"),
                 bg=BG3, fg=NEON).pack(pady=(10,2))
        tk.Label(aira_card, text="AI PARTNER", font=("Courier", 7),
                 bg=BG3, fg=PURPLE).pack()
        tk.Frame(aira_card, bg=PURPLE, height=1).pack(fill="x", padx=10, pady=5)
        self.aira_msg = tk.Label(aira_card, text="Ready, Brayo.",
                                  font=("Courier", 8), bg=BG3,
                                  fg=WHITE, wraplength=125, justify="center")
        self.aira_msg.pack(pady=(2,10))
        # Quick launch
        tk.Label(side, text="── QUICK LAUNCH ──",
                 font=("Courier", 6, "bold"),
                 bg=BG2, fg=PURPLE2).pack(pady=(5,3))
        quick = [
            ("☠", "Dark Web",  "dark_web_monitor.py",   "#FF0000"),
            ("◉", "Ghost Mode","ghost_mode.py",          "#44FFCC"),
            ("▣", "DNA Vault", "dna_vault.py",           "#FFD700"),
            ("●", "Threat Map","live_threat_map.py",     "#FF0044"),
            ("★", "AIRA AI",   "aria_voice.py",          "#FF44FF"),
        ]
        for icon, name, script, color in quick:
            btn = tk.Frame(side, bg=BG2, cursor="hand2")
            btn.pack(fill="x", padx=6, pady=2)
            inner = tk.Frame(btn, bg=BG3)
            inner.pack(fill="x")
            tk.Label(inner, text=icon, font=("Courier", 11, "bold"),
                     bg=BG3, fg=color, width=3).pack(side="left", padx=5, pady=5)
            tk.Label(inner, text=name, font=("Courier", 8),
                     bg=BG3, fg=WHITE).pack(side="left")
            for w in [btn, inner] + inner.winfo_children():
                w.bind("<Button-1>", lambda e, s=script: self.launch(s))
                w.bind("<Enter>", lambda e, f=inner: f.config(bg=PURPLE3))
                w.bind("<Leave>", lambda e, f=inner: f.config(bg=BG3))
        tk.Frame(side, bg=PURPLE3, height=1).pack(fill="x", padx=8, pady=8)
        tk.Label(side, text=f"◈ {len(APPS)} apps",
                 font=("Courier", 7), bg=BG2, fg=PURPLE2).pack()
        tk.Label(side, text="Built Different 🇰🇪",
                 font=("Courier", 6), bg=BG2, fg=PURPLE3).pack(pady=2)
        # ── APP GRID ─────────────────────────
        grid_outer = tk.Frame(main, bg=BG)
        grid_outer.pack(side="left", fill="both", expand=True, padx=(5,0))
        self.canvas = tk.Canvas(grid_outer, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(grid_outer, orient="vertical",
                           command=self.canvas.yview, bg=BG2,
                           troughcolor=BG, width=8)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.grid_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas.create_window((0,0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", lambda e:
            self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.render_apps("ALL")
        # ── BOTTOM TASKBAR ───────────────────
        bottom = tk.Frame(self.root, bg=BG2, height=44)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)
        docked = [
            ("⌨", "Terminal", "terminal",             PURPLE),
            ("★", "AIRA",     "aria_voice.py",         NEON2),
            ("☠", "Dark Web", "dark_web_monitor.py",   "#FF0000"),
            ("◉", "Ghost",    "ghost_mode.py",         "#44FFCC"),
            ("◫", "Store",    "app_store.py",          "#00AAFF"),
            ("✦", "Settings", "settings.py",           "#CCCCFF"),
        ]
        for icon, name, script, color in docked:
            f = tk.Frame(bottom, bg=BG2, cursor="hand2", padx=2)
            f.pack(side="left", padx=8, pady=4)
            lbl_icon = tk.Label(f, text=icon, font=("Courier", 14, "bold"),
                                 bg=BG2, fg=color)
            lbl_icon.pack()
            lbl_name = tk.Label(f, text=name, font=("Courier", 6),
                                 bg=BG2, fg=DIM)
            lbl_name.pack()
            for w in [f, lbl_icon, lbl_name]:
                w.bind("<Enter>", lambda e, fi=f, c=color:
                       [fi.config(bg=PURPLE3)] +
                       [w.config(bg=PURPLE3) for w in fi.winfo_children()])
                w.bind("<Leave>", lambda e, fi=f:
                       [fi.config(bg=BG2)] +
                       [w.config(bg=BG2) for w in fi.winfo_children()])
        tk.Label(bottom, text="Two minds. One OS. Built Different.",
                 font=("Courier", 7), bg=BG2, fg=PURPLE2).pack(side="right", padx=12)
    def make_app_card(self, parent, icon, name, script, color, row, col):
        # Outer glow frame
        glow_frame = tk.Frame(parent, bg=color, padx=1, pady=1)
        glow_frame.grid(row=row, column=col, padx=6, pady=6)
        # Inner card
        card = tk.Frame(glow_frame, bg=BG3, width=100, height=85,
                        cursor="hand2")
        card.pack()
        card.pack_propagate(False)
        icon_lbl = tk.Label(card, text=icon,
                             font=("Courier", 18, "bold"),
                             bg=BG3, fg=color)
        icon_lbl.pack(expand=True, pady=(10,2))
        name_lbl = tk.Label(card, text=name,
                             font=("Courier", 7),
                             bg=BG3, fg=WHITE)
        name_lbl.pack(pady=(0,8))
        # Hover effects
        def on_enter(e):
            glow_frame.config(bg=NEON, padx=2, pady=2)
            card.config(bg=PURPLE3)
            icon_lbl.config(bg=PURPLE3)
            name_lbl.config(bg=PURPLE3, fg=NEON)
        def on_leave(e):
            glow_frame.config(bg=color, padx=1, pady=1)
            card.config(bg=BG3)
            icon_lbl.config(bg=BG3)
            name_lbl.config(bg=BG3, fg=WHITE)
        def on_click(e):
            self.launch(script)
            glow_frame.config(bg="#FFFFFF")
            self.root.after(100, lambda: glow_frame.config(bg=color))
        for w in [glow_frame, card, icon_lbl, name_lbl]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)
    def render_apps(self, cat):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        apps = APPS if cat == "ALL" else [
            a for a in APPS if a[2] in (CATS[cat] or [])]
        cols = 5
        for i, (icon, name, script, color) in enumerate(apps):
            row, col = divmod(i, cols)
            self.make_app_card(self.grid_frame, icon, name,
                                script, color, row, col)
    def switch_cat(self, cat):
        self.current_cat = cat
        for c, b in self.cat_btns.items():
            b.config(bg=BG, fg=DIM)
        self.cat_btns[cat].config(bg=PURPLE3, fg=NEON)
        self.render_apps(cat)
    def launch(self, script):
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        try:
            if script == "terminal":
                subprocess.Popen(["x-terminal-emulator"], env=env)
            else:
                path = os.path.expanduser(
                    f"~/BrayoOS/core/apps/{script}")
                if os.path.exists(path):
                    subprocess.Popen(["python3", path], env=env)
                    self.aira_msg.config(
                        text=f"Launching\n{script.replace('.py','')}...")
                    self.root.after(2000, lambda:
                        self.aira_msg.config(text="Ready, Brayo."))
                else:
                    self.aira_msg.config(text="Not found: "+script[:18])
        except Exception as e:
            self.aira_msg.config(text=f"Error:\n{str(e)[:25]}")
    def clock_tick(self):
        now = datetime.now().strftime("%H:%M:%S  %d/%m/%y")
        self.clock_lbl.config(text=now)
        self.root.after(1000, self.clock_tick)
    def pulse_loop(self):
        self.pulse_state = not self.pulse_state
        color = PURPLE if self.pulse_state else GLOW
        self.pulse_dot.config(fg=color)
        self.root.after(800, self.pulse_loop)
if __name__ == "__main__":
    BrayoOS()
