import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import socket

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class PacketSniffer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📡 Packet Sniffer")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.sniffing = False
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📡 Packet Sniffer",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        for text, cmd in [
            ("▶ Start", self.start),
            ("⏹ Stop", self.stop),
            ("🧹 Clear", lambda: self.output.delete(1.0, tk.END)),
            ("💾 Save", self.save),
        ]:
            tk.Button(frame, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 10),
                     command=cmd,
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=3)

        # Filter
        filter_frame = tk.Frame(self.root, bg=BG)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Filter:",
                bg=BG, fg=TEXT,
                font=("monospace", 10)).pack(side=tk.LEFT)

        self.filter = tk.Entry(filter_frame,
                              bg=DARK, fg=ACCENT,
                              font=("monospace", 10),
                              insertbackground=ACCENT)
        self.filter.pack(side=tk.LEFT, fill=tk.X,
                        expand=True, padx=5)
        self.filter.insert(0, "")

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 9))
        self.output.pack(fill=tk.BOTH, expand=True,
                        padx=10, pady=5)

        self.status = tk.Label(self.root,
                              text="● IDLE",
                              bg=DARK, fg="red",
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def start(self):
        self.sniffing = True
        self.status.config(text="● SNIFFING", fg=ACCENT)
        threading.Thread(target=self.sniff).start()

    def stop(self):
        self.sniffing = False
        self.status.config(text="● IDLE", fg="red")

    def sniff(self):
        try:
            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_RAW,
                socket.IPPROTO_TCP)
            self.log("📡 Sniffing started...")
            while self.sniffing:
                data, addr = s.recvfrom(65535)
                src_ip = addr[0]
                filt = self.filter.get()
                if filt and filt not in src_ip:
                    continue
                self.log(
                    f"📦 {src_ip} → "
                    f"Len:{len(data)} bytes")
        except PermissionError:
            self.log(
                "❌ Need root for raw sockets!\n"
                "Using tcpdump instead...")
            self.sniff_tcpdump()
        except Exception as e:
            self.log(f"Error: {e}")

    def sniff_tcpdump(self):
        try:
            proc = subprocess.Popen(
                ["tcpdump", "-l", "-n"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)
            while self.sniffing:
                line = proc.stdout.readline()
                if line:
                    self.log(line.strip())
        except Exception as e:
            self.log(f"Error: {e}")

    def save(self):
        import os, time
        fname = os.path.expanduser(
            f"~/BrayoOS/memory/capture_{time.strftime('%H%M%S')}.txt")
        with open(fname, 'w') as f:
            f.write(self.output.get(1.0, tk.END))
        self.log(f"💾 Saved to {fname}")

if __name__ == "__main__":
    PacketSniffer()
