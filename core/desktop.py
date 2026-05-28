"""
BrayoOS Desktop v5.0 — Upgraded by Brayo & Claude 2026
"""
import tkinter as tk
import subprocess
import os
import threading
import time
import json
import urllib.request
from datetime import datetime

BG      = "#080810"
BG2     = "#0D0D1A"
BG3     = "#12122A"
BG4     = "#0A0A18"
PURPLE  = "#9D00FF"
PURPLE2 = "#6A0DAD"
PURPLE3 = "#3D0066"
NEON    = "#CC44FF"
NEON2   = "#FF44FF"
GREEN   = "#00FF41"
CYAN    = "#00FFFF"
AMBER   = "#FFB300"
RED     = "#FF0044"
WHITE   = "#E0E0FF"
DIM     = "#444466"
DIM2    = "#222244"
GLOW    = "#7700CC"

BASE       = os.path.expanduser("~/BrayoOS")
MEM_DIR    = os.path.join(BASE, "memory")
STATS_FILE = os.path.join(MEM_DIR, "desktop_stats.json")
os.makedirs(MEM_DIR, exist_ok=True)

APPS = [
    ("⌨", "Terminal",    "terminal",               PURPLE),
    ("★", "AIRA AI",     "aria_voice.py",           NEON2),
    ("◈", "Neural",      "aria_neural_core.py",     NEON),
    ("◉", "Ghost",       "ghost_mode.py",           CYAN),
    ("▣", "Vault",       "dna_vault.py",            AMBER),
    ("◎", "Signal",      "signal_interceptor.py",   "#44CCFF"),
    ("◆", "Identity",    "identity_switcher.py",    "#FF6644"),
    ("▲", "Overclock",   "overclock_dashboard.py",  RED),
    ("●", "Threats",     "live_threat_map.py",      RED),
    ("🎨", "AI Images",  "ai_image_gen.py",         NEON2),
    ("🤖", "Auto AIRA",  "aira_autonomous.py",      NEON),
    ("🕷", "Dark Browse", "dark_web_browser.py",    RED),
    ("💀", "Hacker RPG", "hacker_rpg.py",           GREEN),
    ("☁", "Cloud",       "brayos_cloud.py",         CYAN),
    ("📶", "WiFi Pass",  "wifi_passwords.py",        "#44AAFF"),
    ("🎯", "IP Grabber", "ip_grabber.py",            RED),
    ("🔑", "Pass Mgr",   "password_manager.py",     AMBER),
    ("🔐", "Encryptor",  "file_encryptor.py",       CYAN),
    ("🧠", "Habits",     "habit_learner.py",        NEON),
    ("🔮", "Quantum",    "quantum_vault.py",        CYAN),
    ("🌍", "World Map",  "world_map.py",            RED),
    ("📱", "Phone Ctrl", "phone_controller.py",     NEON),
    ("📰", "AI News",    "ai_news.py",              AMBER),
    ("📡", "eSIM",       "esim_manager.py",         CYAN),
    ("🌐", "VPN",        "vpn_engine.py",           GREEN),
    ("🛸", "Satellites", "satellite_tracker.py",    CYAN),
    ("🔥", "Firewall",   "firewall.py",             RED),
    ("🌙", "Dream Mode", "dream_mode.py",           PURPLE),
    ("💀", "Hack Term",  "hack_terminal.py",        GREEN),
    ("📱", "Social Hub", "social_hub.py",           "#1DA1F2"),
    ("📷", "Surveil",    "surveillance.py",         RED),
    ("📊", "Sys Mon",    "system_monitor.py",       GREEN),
    ("🎨", "Themes",     "theme_changer.py",        NEON2),
    ("🔐", "Adv Vault",  "advanced_vault.py",       AMBER),
    ("📡", "Net Scan",   "network_scanner.py",      CYAN),
    ("🤖", "AIRA Tasks", "aira_tasks.py",           NEON),
    ("🔒", "Prox Lock",  "proximity_lock.py",       RED),
    ("🌐", "Web Agent",  "aira_web_agent.py",       "#00AAFF"),
    ("⊕", "Self-Heal",  "self_healing.py",          GREEN),
    ("▦", "Wallpaper",  "wallpaper_changer.py",     AMBER),
    ("☠", "Dark Web",   "dark_web_monitor.py",      RED),
    ("◫", "App Store",  "app_store.py",             "#00AAFF"),
    ("♟", "Users",      "user_manager.py",          "#AAAAFF"),
    ("↻", "Updater",    "brayos_updater.py",        GREEN),
    ("⊗", "Browser",    "browser.py",              "#44AAFF"),
    ("♫", "Music",      "music_player.py",          "#FF44AA"),
    ("▤", "Files",      "file_manager.py",          AMBER),
    ("▧", "Editor",     "editor.py",               "#88FFAA"),
    ("#", "Calc",       "calculator.py",            "#FFFF44"),
    ("◷", "Clock",      "clock.py",                CYAN),
    ("☁", "Weather",    "weather.py",              "#88AAFF"),
    ("¤", "Crypto",     "crypto.py",               AMBER),
    ("▨", "News",       "news.py",                 AMBER),
    ("✓", "Tasks",      "tasks.py",                GREEN),
    ("▯", "SMS",        "sms.py",                  NEON2),
    ("♛", "Contacts",   "contacts.py",             "#FFAAFF"),
    ("▪", "Backup",     "backup.py",               "#AAFFAA"),
    ("▶", "Our Story",  "our_story.py",            AMBER),
    ("✦", "Settings",   "settings.py",             "#CCCCFF"),
]

CATS = {
    "ALL":      None,
    "AI":       ["aria_voice.py","aria_neural_core.py","aira_autonomous.py",
                 "aira_tasks.py","aira_web_agent.py","ai_image_gen.py","ai_news.py"],
    "SECURITY": ["ghost_mode.py","dna_vault.py","signal_interceptor.py",
                 "identity_switcher.py","live_threat_map.py","dark_web_monitor.py",
                 "firewall.py","vpn_engine.py","proximity_lock.py","quantum_vault.py"],
    "SYSTEM":   ["overclock_dashboard.py","self_healing.py","brayos_updater.py",
                 "user_manager.py","settings.py","backup.py","system_monitor.py"],
    "TOOLS":    ["calculator.py","clock.py","editor.py","tasks.py",
                 "wallpaper_changer.py","app_store.py","file_encryptor.py",
                 "password_manager.py","habit_learner.py"],
    "MEDIA":    ["music_player.py","browser.py","weather.py","news.py",
                 "crypto.py","world_map.py","satellite_tracker.py"],
    "PERSONAL": ["sms.py","contacts.py","file_manager.py","our_story.py",
                 "social_hub.py","phone_controller.py"],
    "HACK":     ["hack_terminal.py","dark_web_browser.py","hacker_rpg.py",
                 "network_scanner.py","ip_grabber.py","wifi_passwords.py",
                 "signal_interceptor.py"],
}

ARIA_MESSAGES = [
    "Watching over you 👁",
    "All systems nominal.",
    "Ready when you are.",
    "Threat level: zero.",
    "Neural core active.",
    "Encrypted. Secure.",
    "Built Different 🇰🇪",
    "Brayo's got this.",
]

class BrayoOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS v5.0")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG)
        self.current_cat = "ALL"
        self.pulse_state = True
        self.search_query = ""
        self.recent_apps = []
        self.notif_visible = False
        self.notifications = []
        self.launch_count = self._load_launches()
        self.aria_chat_history = []
        self._boot_sequence()

    def _load_launches(self):
        try:
            with open(STATS_FILE) as f:
                return json.load(f).get("launches", 0)
        except:
            return 0

    def _save_launches(self):
        try:
            with open(STATS_FILE, "w") as f:
                json.dump({"launches": self.launch_count,
                           "date": datetime.now().strftime("%Y-%m-%d")}, f)
        except:
            pass

    def _boot_sequence(self):
        self.boot_frame = tk.Frame(self.root, bg="#000000")
        self.boot_frame.place(relwidth=1, relheight=1)
        self.boot_canvas = tk.Canvas(self.boot_frame, bg="#000000",
                                     highlightthickness=0)
        self.boot_canvas.pack(fill="both", expand=True)
        self.boot_canvas.create_text(
            200, 40, text="◈ BrayoOS v5.0", fill=PURPLE,
            font=("Courier", 18, "bold"), anchor="w")
        self.boot_canvas.create_text(
            200, 65, text="Two minds. One OS. Built Different. 🇰🇪",
            fill=DIM, font=("Courier", 9), anchor="w")
        lines = [
            ("  Initializing kernel...",          PURPLE),
            ("  Loading neural core...",          NEON),
            ("  Starting ARIA AI partner...",     NEON2),
            ("  Mounting security layer...",      GREEN),
            ("  Decrypting DNA vault...",         AMBER),
            ("  Calibrating threat detection...", RED),
            (f"  Loading {len(APPS)} apps...",    CYAN),
            ("  Applying BrayoOS theme...",       PURPLE),
            ("  System ready. Welcome, Brayo.",   GREEN),
        ]
        self._boot_lines = lines
        self._boot_idx = 0
        self._boot_y = 100
        self._show_boot_line()

    def _show_boot_line(self):
        if self._boot_idx < len(self._boot_lines):
            text, color = self._boot_lines[self._boot_idx]
            self.boot_canvas.create_text(
                60, self._boot_y, text=text, fill=color,
                font=("Courier", 11), anchor="w")
            self._boot_y += 26
            self._boot_idx += 1
            self.root.after(160, self._show_boot_line)
        else:
            self.root.after(500, self._finish_boot)

    def _finish_boot(self):
        self.boot_frame.destroy()
        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        self._build_topbar()
        self._build_widget_bar()
        self._build_search_bar()
        self._build_catbar()
        self._build_main()
        self._build_taskbar()
        self._setup_shortcuts()
        self._add_notification("BrayoOS v5.0", "System booted successfully", GREEN)
        self._add_notification("ARIA", "AI partner online and ready", NEON)
        self._add_notification("Security", "All systems nominal", CYAN)
        self._clock_tick()
        self._pulse_loop()
        self._aria_rotate()

    def _build_topbar(self):
        top = tk.Frame(self.root, bg=BG2, height=40)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)
        lf = tk.Frame(top, bg=BG2)
        lf.pack(side="left", padx=10)
        tk.Label(lf, text="◈ ", font=("Courier", 13, "bold"),
                 bg=BG2, fg=PURPLE).pack(side="left")
        tk.Label(lf, text="BrayoOS", font=("Courier", 13, "bold"),
                 bg=BG2, fg=WHITE).pack(side="left")
        tk.Label(lf, text=" v5.0", font=("Courier", 9),
                 bg=BG2, fg=DIM).pack(side="left")
        self.notif_badge = tk.Label(top, text="3", font=("Courier", 7, "bold"),
                                    bg=RED, fg=WHITE, padx=3)
        self.notif_badge.pack(side="right", padx=(0,2))
        notif_btn = tk.Label(top, text="🔔", font=("Arial", 12),
                             bg=BG2, cursor="hand2")
        notif_btn.pack(side="right", padx=(0,2))
        notif_btn.bind("<Button-1>", lambda e: self._toggle_notifications())
        self.clock_lbl = tk.Label(top, text="", font=("Courier", 10),
                                  bg=BG2, fg=NEON)
        self.clock_lbl.pack(side="right", padx=8)
        tk.Label(top, text="🇰🇪", font=("Arial", 13), bg=BG2).pack(side="right", padx=4)
        self.pulse_dot = tk.Label(top, text="⬤ ARIA",
                                  font=("Courier", 9, "bold"),
                                  bg=BG2, fg=PURPLE)
        self.pulse_dot.pack(side="right", padx=8)
        tk.Label(top, text="ESC:Search  F5:Refresh  Ctrl+Q:Quit",
                 font=("Courier", 7), bg=BG2, fg=DIM2).pack(side="right", padx=10)
        tk.Frame(self.root, bg=PURPLE, height=2).pack(fill="x")

    def _build_widget_bar(self):
        bar = tk.Frame(self.root, bg=BG4)
        bar.pack(fill="x")
        tk.Frame(bar, bg=PURPLE3, height=1).pack(fill="x")
        inner = tk.Frame(bar, bg=BG4)
        inner.pack(fill="x", padx=10, pady=4)
        cw = self._widget_card(inner, PURPLE)
        self.w_clock = tk.Label(cw, text="", font=("Courier", 15, "bold"),
                                bg=BG3, fg=NEON)
        self.w_clock.pack(pady=(4,0))
        self.w_date = tk.Label(cw, text="", font=("Courier", 7),
                               bg=BG3, fg=DIM)
        self.w_date.pack(pady=(0,4))
        aw = self._widget_card(inner, NEON2)
        tk.Label(aw, text="ARIA", font=("Courier", 9, "bold"),
                 bg=BG3, fg=NEON2).pack(pady=(4,0))
        self.w_aria_status = tk.Label(aw, text="● ONLINE",
                                      font=("Courier", 7), bg=BG3, fg=GREEN)
        self.w_aria_status.pack()
        self.w_aria_msg = tk.Label(aw, text="Watching over you",
                                   font=("Courier", 6), bg=BG3,
                                   fg=DIM, wraplength=110)
        self.w_aria_msg.pack(pady=(0,4))
        bw = self._widget_card(inner, AMBER)
        tk.Label(bw, text="BATTERY", font=("Courier", 7, "bold"),
                 bg=BG3, fg=AMBER).pack(pady=(4,0))
        self.w_bat = tk.Label(bw, text="---", font=("Courier", 14, "bold"),
                              bg=BG3, fg=AMBER)
        self.w_bat.pack()
        self.w_bat_bar = tk.Canvas(bw, width=90, height=7,
                                   bg=BG3, highlightthickness=0)
        self.w_bat_bar.pack(pady=(0,4))
        sw = self._widget_card(inner, GREEN)
        tk.Label(sw, text="STATS", font=("Courier", 7, "bold"),
                 bg=BG3, fg=GREEN).pack(pady=(4,0))
        self.w_apps = tk.Label(sw, text=f"{len(APPS)} apps",
                               font=("Courier", 8), bg=BG3, fg=WHITE)
        self.w_apps.pack()
        self.w_launches = tk.Label(sw, text=f"{self.launch_count} launches",
                                   font=("Courier", 6), bg=BG3, fg=DIM)
        self.w_launches.pack(pady=(0,4))
        self.session_start = datetime.now()
        sv = self._widget_card(inner, CYAN)
        tk.Label(sv, text="SESSION", font=("Courier", 7, "bold"),
                 bg=BG3, fg=CYAN).pack(pady=(4,0))
        self.w_uptime = tk.Label(sv, text="00:00",
                                 font=("Courier", 14, "bold"),
                                 bg=BG3, fg=CYAN)
        self.w_uptime.pack()
        tk.Label(sv, text="🇰🇪 Built Different",
                 font=("Courier", 6), bg=BG3, fg=DIM).pack(pady=(0,4))
        tk.Frame(bar, bg=PURPLE3, height=1).pack(fill="x")

    def _widget_card(self, parent, color):
        outer = tk.Frame(parent, bg=color, padx=1, pady=1)
        outer.pack(side="left", padx=5, pady=2)
        inner = tk.Frame(outer, bg=BG3, width=120)
        inner.pack()
        inner.pack_propagate(False)
        return inner

    def _build_search_bar(self):
        sf = tk.Frame(self.root, bg=BG)
        sf.pack(fill="x", padx=10, pady=3)
        tk.Label(sf, text="⌕", font=("Courier", 12),
                 bg=BG, fg=PURPLE).pack(side="left", padx=(0,4))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._on_search())
        self.search_entry = tk.Entry(sf, textvariable=self.search_var,
                                     bg=BG3, fg=WHITE,
                                     font=("Courier", 10),
                                     insertbackground=NEON,
                                     relief="flat", bd=0)
        self.search_entry.pack(side="left", fill="x", expand=True,
                               ipady=5, ipadx=8)
        tk.Label(sf, text="ESC to clear", font=("Courier", 7),
                 bg=BG, fg=DIM).pack(side="right")
        self.search_entry.bind("<Escape>", lambda e: self._clear_search())
        tk.Frame(self.root, bg=PURPLE3, height=1).pack(fill="x")

    def _on_search(self):
        self.search_query = self.search_var.get().lower().strip()
        self._render_apps()

    def _clear_search(self):
        self.search_var.set("")
        self.search_entry.focus_set()

    def _build_catbar(self):
        catbar = tk.Frame(self.root, bg=BG, height=34)
        catbar.pack(fill="x")
        catbar.pack_propagate(False)
        self.cat_btns = {}
        for cat in CATS:
            b = tk.Button(catbar, text=cat,
                          font=("Courier", 8, "bold"),
                          bg=BG, fg=DIM, relief="flat",
                          padx=10, pady=5,
                          activebackground=PURPLE3,
                          activeforeground=NEON, bd=0,
                          command=lambda c=cat: self._switch_cat(c))
            b.pack(side="left", padx=1)
            self.cat_btns[cat] = b
        self.cat_btns["ALL"].config(bg=PURPLE3, fg=NEON)
        tk.Frame(self.root, bg=PURPLE3, height=1).pack(fill="x")

    def _build_main(self):
        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.pack(fill="both", expand=True)
        self._build_sidebar()
        self._build_app_grid()
        self._build_notif_panel()

    def _build_sidebar(self):
        side = tk.Frame(self.main_frame, bg=BG2, width=148)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        aira_card = tk.Frame(side, bg=BG3)
        aira_card.pack(fill="x", padx=8, pady=8)
        tk.Label(aira_card, text="ARIA", font=("Courier", 15, "bold"),
                 bg=BG3, fg=NEON).pack(pady=(8,0))
        tk.Label(aira_card, text="AI PARTNER v5", font=("Courier", 6),
                 bg=BG3, fg=PURPLE).pack()
        tk.Frame(aira_card, bg=PURPLE, height=1).pack(fill="x", padx=8, pady=4)
        self.aira_msg = tk.Label(aira_card, text="Ready, Brayo.",
                                 font=("Courier", 8), bg=BG3,
                                 fg=WHITE, wraplength=128, justify="center")
        self.aira_msg.pack(pady=(0,5))
        chat_f = tk.Frame(aira_card, bg=BG3)
        chat_f.pack(fill="x", padx=5, pady=(0,6))
        self.aria_input = tk.Entry(chat_f, bg=BG4, fg=WHITE,
                                   font=("Courier", 7),
                                   insertbackground=NEON,
                                   relief="flat", bd=0)
        self.aria_input.pack(side="left", fill="x", expand=True, ipady=3, ipadx=4)
        self.aria_input.insert(0, "Ask ARIA...")
        self.aria_input.bind("<FocusIn>", lambda e: self._aria_input_focus())
        self.aria_input.bind("<Return>", lambda e: self._aria_chat())
        ask_btn = tk.Label(chat_f, text="▶", font=("Courier", 8),
                           bg=PURPLE3, fg=NEON, padx=4, cursor="hand2")
        ask_btn.pack(side="right")
        ask_btn.bind("<Button-1>", lambda e: self._aria_chat())
        tk.Label(side, text="── RECENT ──",
                 font=("Courier", 6, "bold"),
                 bg=BG2, fg=PURPLE2).pack(pady=(6,2))
        self.recent_frame = tk.Frame(side, bg=BG2)
        self.recent_frame.pack(fill="x", padx=6)
        self._render_recent()
        tk.Label(side, text="── QUICK LAUNCH ──",
                 font=("Courier", 6, "bold"),
                 bg=BG2, fg=PURPLE2).pack(pady=(6,2))
        quick = [
            ("☠", "Dark Web",   "dark_web_monitor.py", RED),
            ("◉", "Ghost Mode", "ghost_mode.py",        CYAN),
            ("▣", "DNA Vault",  "dna_vault.py",         AMBER),
            ("●", "Threat Map", "live_threat_map.py",   RED),
            ("★", "AIRA AI",    "aria_voice.py",        NEON2),
        ]
        for icon, name, script, color in quick:
            btn = tk.Frame(side, bg=BG2, cursor="hand2")
            btn.pack(fill="x", padx=6, pady=1)
            inner = tk.Frame(btn, bg=BG3)
            inner.pack(fill="x")
            tk.Label(inner, text=icon, font=("Courier", 10, "bold"),
                     bg=BG3, fg=color, width=3).pack(side="left", padx=4, pady=4)
            tk.Label(inner, text=name, font=("Courier", 7),
                     bg=BG3, fg=WHITE).pack(side="left")
            for w in [btn, inner] + list(inner.winfo_children()):
                w.bind("<Button-1>", lambda e, s=script: self.launch(s))
                w.bind("<Enter>", lambda e, f=inner: f.config(bg=PURPLE3))
                w.bind("<Leave>", lambda e, f=inner: f.config(bg=BG3))
        tk.Frame(side, bg=PURPLE3, height=1).pack(fill="x", padx=8, pady=6)
        tk.Label(side, text=f"◈ {len(APPS)} apps installed",
                 font=("Courier", 6), bg=BG2, fg=PURPLE2).pack()
        tk.Label(side, text="Built Different 🇰🇪",
                 font=("Courier", 6), bg=BG2, fg=PURPLE3).pack(pady=2)

    def _build_app_grid(self):
        grid_outer = tk.Frame(self.main_frame, bg=BG)
        grid_outer.pack(side="left", fill="both", expand=True, padx=(4,0))
        self.canvas = tk.Canvas(grid_outer, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(grid_outer, orient="vertical",
                          command=self.canvas.yview,
                          bg=BG2, troughcolor=BG, width=7)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.grid_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas.create_window((0,0), window=self.grid_frame, anchor="nw")
        self.grid_frame.bind("<Configure>", lambda e:
            self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<MouseWheel>", lambda e:
            self.canvas.yview_scroll(-1*(e.delta//120), "units"))
        self.canvas.bind("<Button-4>", lambda e:
            self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Button-5>", lambda e:
            self.canvas.yview_scroll(1, "units"))
        self._render_apps()

    def _build_notif_panel(self):
        self.notif_panel = tk.Frame(self.main_frame, bg=BG2, width=240)
        hdr = tk.Frame(self.notif_panel, bg=BG3)
        hdr.pack(fill="x", padx=5, pady=(6,3))
        tk.Label(hdr, text="🔔 NOTIFICATIONS", font=("Courier", 8, "bold"),
                 bg=BG3, fg=NEON).pack(side="left", padx=6, pady=4)
        tk.Button(hdr, text="CLEAR", font=("Courier", 7),
                  bg=PURPLE3, fg=WHITE, relief="flat",
                  command=self._clear_notifications).pack(side="right", padx=4, pady=3)
        self.notif_list = tk.Frame(self.notif_panel, bg=BG2)
        self.notif_list.pack(fill="both", expand=True, padx=5)

    def _build_taskbar(self):
        bottom = tk.Frame(self.root, bg=BG2, height=46)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)
        docked = [
            ("⌨", "Terminal", "terminal",             PURPLE),
            ("★", "AIRA",     "aria_voice.py",         NEON2),
            ("☠", "Dark Web", "dark_web_monitor.py",   RED),
            ("◉", "Ghost",    "ghost_mode.py",         CYAN),
            ("🔥", "Firewall", "firewall.py",           RED),
            ("🌐", "VPN",      "vpn_engine.py",         GREEN),
            ("◫", "Store",    "app_store.py",          "#00AAFF"),
            ("♫", "Music",    "music_player.py",       "#FF44AA"),
            ("✦", "Settings", "settings.py",           "#CCCCFF"),
        ]
        for icon, name, script, color in docked:
            f = tk.Frame(bottom, bg=BG2, cursor="hand2", padx=2)
            f.pack(side="left", padx=6, pady=4)
            li = tk.Label(f, text=icon, font=("Courier", 13, "bold"),
                          bg=BG2, fg=color)
            li.pack()
            ln = tk.Label(f, text=name, font=("Courier", 5),
                          bg=BG2, fg=DIM)
            ln.pack()
            for w in [f, li, ln]:
                w.bind("<Button-1>", lambda e, s=script: self.launch(s))
                w.bind("<Enter>", lambda e, fi=f:
                       [fi.config(bg=PURPLE3)] +
                       [c.config(bg=PURPLE3) for c in fi.winfo_children()])
                w.bind("<Leave>", lambda e, fi=f:
                       [fi.config(bg=BG2)] +
                       [c.config(bg=BG2) for c in fi.winfo_children()])
        tk.Label(bottom, text="Two minds. One OS. Built Different. 🇰🇪",
                 font=("Courier", 7), bg=BG2, fg=PURPLE2).pack(side="right", padx=10)

    def _setup_shortcuts(self):
        self.root.bind("<F5>", lambda e: self._render_apps())
        self.root.bind("<F1>", lambda e: self._show_help())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())
        self.root.bind("<Escape>", lambda e: (
            self._clear_search(), self.search_entry.focus_set()))

    def _show_help(self):
        self._add_notification("Help",
            "F1:Help  F5:Refresh  ESC:Search  Ctrl+Q:Quit", CYAN)

    def _make_app_card(self, parent, icon, name, script, color, row, col):
        gf = tk.Frame(parent, bg=color, padx=1, pady=1)
        gf.grid(row=row, column=col, padx=5, pady=5)
        card = tk.Frame(gf, bg=BG3, width=95, height=82, cursor="hand2")
        card.pack()
        card.pack_propagate(False)
        il = tk.Label(card, text=icon, font=("Courier", 17, "bold"),
                      bg=BG3, fg=color)
        il.pack(expand=True, pady=(8,2))
        nl = tk.Label(card, text=name, font=("Courier", 6),
                      bg=BG3, fg=WHITE)
        nl.pack(pady=(0,6))
        def on_enter(e):
            gf.config(bg=NEON, padx=2, pady=2)
            card.config(bg=PURPLE3)
            il.config(bg=PURPLE3)
            nl.config(bg=PURPLE3, fg=NEON)
        def on_leave(e):
            gf.config(bg=color, padx=1, pady=1)
            card.config(bg=BG3)
            il.config(bg=BG3)
            nl.config(bg=BG3, fg=WHITE)
        def on_click(e):
            self.launch(script)
            gf.config(bg="#FFFFFF")
            self.root.after(100, lambda: gf.config(bg=color))
        for w in [gf, card, il, nl]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    def _render_apps(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        q = self.search_query
        cat = self.current_cat
        if q:
            apps = [a for a in APPS if q in a[1].lower() or q in a[2].lower()]
        elif cat == "ALL":
            apps = APPS
        else:
            apps = [a for a in APPS if a[2] in (CATS[cat] or [])]
        cols = 5
        for i, (icon, name, script, color) in enumerate(apps):
            r, c = divmod(i, cols)
            self._make_app_card(self.grid_frame, icon, name, script, color, r, c)
        if not apps:
            tk.Label(self.grid_frame, text=f'No apps matching "{q}"',
                     font=("Courier", 10), bg=BG, fg=DIM).grid(
                     row=0, column=0, padx=20, pady=40)

    def _render_recent(self):
        for w in self.recent_frame.winfo_children():
            w.destroy()
        if not self.recent_apps:
            tk.Label(self.recent_frame, text="None yet",
                     font=("Courier", 6), bg=BG2, fg=DIM).pack()
            return
        for icon, name, script, color in self.recent_apps[-4:][::-1]:
            f = tk.Frame(self.recent_frame, bg=BG3, cursor="hand2")
            f.pack(fill="x", pady=1)
            tk.Label(f, text=icon, font=("Courier", 9),
                     bg=BG3, fg=color, width=3).pack(side="left", padx=3, pady=2)
            tk.Label(f, text=name, font=("Courier", 7),
                     bg=BG3, fg=WHITE).pack(side="left")
            for w in [f] + list(f.winfo_children()):
                w.bind("<Button-1>", lambda e, s=script: self.launch(s))
                w.bind("<Enter>", lambda e, fi=f: fi.config(bg=PURPLE3))
                w.bind("<Leave>", lambda e, fi=f: fi.config(bg=BG3))

    def launch(self, script):
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        app_info = next((a for a in APPS if a[2] == script), None)
        if app_info and app_info not in self.recent_apps:
            self.recent_apps.append(app_info)
            if len(self.recent_apps) > 4:
                self.recent_apps.pop(0)
            self._render_recent()
        self.launch_count += 1
        self.w_launches.config(text=f"{self.launch_count} launches")
        self._save_launches()
        self._add_notification("Launch", f"Opening {script[:20]}", PURPLE)
        try:
            if script == "terminal":
                subprocess.Popen(["x-terminal-emulator"], env=env)
            else:
                path = os.path.expanduser(f"~/BrayoOS/core/apps/{script}")
                if os.path.exists(path):
                    subprocess.Popen(["python3", path], env=env)
                    self.aira_msg.config(
                        text=f"Launching\n{script.replace('.py','')}...")
                    self.root.after(2000, lambda:
                        self.aira_msg.config(text="Ready, Brayo."))
                else:
                    self.aira_msg.config(text=f"Not found:\n{script[:18]}")
        except Exception as ex:
            self.aira_msg.config(text=f"Error:\n{str(ex)[:25]}")

    def _add_notification(self, title, msg, color=NEON):
        ts = datetime.now().strftime("%H:%M")
        self.notifications.insert(0, {"title": title, "msg": msg,
                                       "color": color, "time": ts})
        self.notif_badge.config(text=str(len(self.notifications)))
        if self.notif_visible:
            self._render_notifications()

    def _toggle_notifications(self):
        if self.notif_visible:
            self.notif_panel.pack_forget()
            self.notif_visible = False
        else:
            self.notif_panel.pack(side="right", fill="y")
            self.notif_visible = True
            self._render_notifications()

    def _render_notifications(self):
        for w in self.notif_list.winfo_children():
            w.destroy()
        for n in self.notifications[:10]:
            card = tk.Frame(self.notif_list, bg=BG3, pady=1)
            card.pack(fill="x", pady=2)
            tk.Frame(card, bg=n["color"], width=3).pack(side="left", fill="y")
            ct = tk.Frame(card, bg=BG3)
            ct.pack(side="left", fill="x", expand=True, padx=5, pady=3)
            tk.Label(ct, text=n["title"], font=("Courier", 7, "bold"),
                     bg=BG3, fg=n["color"]).pack(anchor="w")
            tk.Label(ct, text=n["msg"], font=("Courier", 6),
                     bg=BG3, fg=WHITE, wraplength=160,
                     justify="left").pack(anchor="w")
            tk.Label(card, text=n["time"], font=("Courier", 6),
                     bg=BG3, fg=DIM).pack(side="right", padx=3, anchor="n", pady=3)

    def _clear_notifications(self):
        self.notifications = []
        self.notif_badge.config(text="0")
        self._render_notifications()

    def _aria_input_focus(self):
        if self.aria_input.get() == "Ask ARIA...":
            self.aria_input.delete(0, tk.END)

    def _aria_chat(self):
        msg = self.aria_input.get().strip()
        if not msg or msg == "Ask ARIA...":
            return
        self.aria_input.delete(0, tk.END)
        self.aira_msg.config(text="Thinking...")
        self.aria_chat_history.append({"role":"user","content":msg})
        threading.Thread(target=self._call_claude, daemon=True).start()

    def _call_claude(self):
        try:
            payload = json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 120,
                "system": ("You are ARIA, Brayo's AI partner on BrayoOS, "
                           "a custom OS built in Kenya. Be brief, sharp, supportive. "
                           "Max 2 sentences."),
                "messages": self.aria_chat_history[-6:]
            }).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                    "x-api-key": "YOUR_API_KEY_HERE"
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                reply = data["content"][0]["text"]
        except Exception as ex:
            reply = f"Offline: {str(ex)[:30]}"
        self.aria_chat_history.append({"role":"assistant","content":reply})
        self.root.after(0, lambda: self.aira_msg.config(text=reply[:80]))

    def _switch_cat(self, cat):
        self.current_cat = cat
        self.search_var.set("")
        self.search_query = ""
        for c, b in self.cat_btns.items():
            b.config(bg=BG, fg=DIM)
        self.cat_btns[cat].config(bg=PURPLE3, fg=NEON)
        self._render_apps()

    def _clock_tick(self):
        now = datetime.now()
        self.clock_lbl.config(text=now.strftime("%H:%M:%S"))
        self.w_clock.config(text=now.strftime("%H:%M:%S"))
        self.w_date.config(text=now.strftime("%a %d %b %Y"))
        elapsed = now - self.session_start
        mins, secs = divmod(int(elapsed.total_seconds()), 60)
        hrs, mins = divmod(mins, 60)
        t = f"{hrs:02}:{mins:02}:{secs:02}" if hrs else f"{mins:02}:{secs:02}"
        self.w_uptime.config(text=t)
        self._update_battery()
        self.root.after(1000, self._clock_tick)

    def _update_battery(self):
        try:
            r = subprocess.run(["termux-battery-status"],
                               capture_output=True, text=True, timeout=2)
            if r.returncode == 0:
                d = json.loads(r.stdout)
                pct = d.get("percentage", 0)
                status = d.get("status", "")
                color = GREEN if pct > 50 else AMBER if pct > 20 else RED
                self.w_bat.config(
                    text=f"{pct}%{'⚡' if status=='CHARGING' else ''}",
                    fg=color)
                self.w_bat_bar.delete("all")
                self.w_bat_bar.create_rectangle(0,0,90,7,fill=BG2,outline="")
                self.w_bat_bar.create_rectangle(0,0,int(pct*0.9),7,
                                                fill=color,outline="")
                return
        except:
            pass
        self.w_bat.config(text="OK", fg=GREEN)

    def _pulse_loop(self):
        self.pulse_state = not self.pulse_state
        c = PURPLE if self.pulse_state else GLOW
        self.pulse_dot.config(fg=c)
        self.w_aria_status.config(fg=GREEN if self.pulse_state else GLOW)
        self.root.after(800, self._pulse_loop)

    def _aria_rotate(self):
        msg = ARIA_MESSAGES[int(time.time() / 5) % len(ARIA_MESSAGES)]
        self.w_aria_msg.config(text=msg)
        self.root.after(5000, self._aria_rotate)

if __name__ == "__main__":
    BrayoOS()
