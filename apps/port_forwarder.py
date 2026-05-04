# BrayoOS — Built by Brayo & ARIA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import socket

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class PortForwarder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔀 Port Forwarder")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔀 Port Forwarder",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.LabelFrame(self.root,
                             text="Forward Settings",
                             bg=BG, fg=ACCENT,
                             font=("monospace", 10))
        frame.pack(fill=tk.X, padx=10, pady=5)

        fields = [
            ("Local Port:", "8080"),
            ("Remote Host:", "192.168.1.1"),
            ("Remote Port:", "80"),
        ]

        self.entries = {}
        for label, default in fields:
            f = tk.Frame(frame, bg=BG)
            f.pack(fill=tk.X, padx=5, pady=3)
            tk.Label(f, text=label, bg=BG, fg=TEXT,
                    font=("monospace", 10),
                    width=15).pack(side=tk.LEFT)
            e = tk.Entry(f, bg=DARK, fg=ACCENT,
                        font=("monospace", 10),
                        insertbackground=ACCENT)
            e.insert(0, default)
            e.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[label] = e

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="▶ Start Forward",
                 bg=ACCENT, fg=BG,
                 command=self.start).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="⏹ Stop",
                 bg=DARK, fg="red",
                 command=self.stop).pack(side=tk.LEFT, padx=3)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)
        self.running = False

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def start(self):
        local = self.entries["Local Port:"].get()
        remote_host = self.entries["Remote Host:"].get()
        remote_port = self.entries["Remote Port:"].get()
        self.running = True
        self.log(f"🔀 Forwarding localhost:{local} → "
                f"{remote_host}:{remote_port}")
        def forward():
            try:
                server = socket.socket()
                server.bind(('0.0.0.0', int(local)))
                server.listen(5)
                self.log("✅ Listening for connections...")
                while self.running:
                    client, addr = server.accept()
                    self.log(f"🔗 Connection from {addr}")
                    threading.Thread(
                        target=self.handle,
                        args=(client, remote_host,
                              int(remote_port))).start()
            except Exception as e:
                self.log(f"Error: {e}")
        threading.Thread(target=forward).start()

    def handle(self, client, host, port):
        try:
            remote = socket.socket()
            remote.connect((host, port))
            def fwd(src, dst):
                while self.running:
                    data = src.recv(4096)
                    if not data:
                        break
                    dst.send(data)
            threading.Thread(
                target=fwd, args=(client, remote)).start()
            threading.Thread(
                target=fwd, args=(remote, client)).start()
        except Exception as e:
            self.log(f"Error: {e}")

    def stop(self):
        self.running = False
        self.log("⏹ Forwarding stopped!")

if __name__ == "__main__":
    PortForwarder()
