# BrayoOS — Built by Brayo & ARIA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext, filedialog
import hashlib
import threading
import time

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class HashCracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔑 Hash Cracker")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.cracking = False
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔑 Hash Cracker",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.LabelFrame(self.root, text="Target Hash",
                             bg=BG, fg=ACCENT,
                             font=("monospace", 10))
        frame.pack(fill=tk.X, padx=10, pady=5)

        f1 = tk.Frame(frame, bg=BG)
        f1.pack(fill=tk.X, padx=5, pady=3)
        tk.Label(f1, text="Hash:", bg=BG, fg=TEXT,
                font=("monospace", 10),
                width=10).pack(side=tk.LEFT)
        self.hash_entry = tk.Entry(f1, bg=DARK, fg=ACCENT,
                                  font=("monospace", 10),
                                  insertbackground=ACCENT)
        self.hash_entry.pack(side=tk.LEFT, fill=tk.X,
                            expand=True)

        f2 = tk.Frame(frame, bg=BG)
        f2.pack(fill=tk.X, padx=5, pady=3)
        tk.Label(f2, text="Type:", bg=BG, fg=TEXT,
                font=("monospace", 10),
                width=10).pack(side=tk.LEFT)
        self.hash_type = tk.StringVar(value="md5")
        for h in ["md5", "sha1", "sha256", "sha512"]:
            tk.Radiobutton(f2, text=h,
                          variable=self.hash_type,
                          value=h, bg=BG, fg=ACCENT,
                          selectcolor=DARK,
                          font=("monospace", 10)).pack(
                              side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        for text, cmd in [
            ("🔑 Crack (Wordlist)", self.crack_wordlist),
            ("🔢 Crack (Bruteforce)", self.crack_brute),
            ("#️⃣ Generate Hash", self.generate_hash),
            ("⏹ Stop", self.stop),
        ]:
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

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def hash_it(self, text):
        h = self.hash_type.get()
        if h == "md5":
            return hashlib.md5(text.encode()).hexdigest()
        elif h == "sha1":
            return hashlib.sha1(text.encode()).hexdigest()
        elif h == "sha256":
            return hashlib.sha256(text.encode()).hexdigest()
        elif h == "sha512":
            return hashlib.sha512(text.encode()).hexdigest()

    def generate_hash(self):
        text = self.hash_entry.get()
        if text:
            result = self.hash_it(text)
            self.log(f"Hash of '{text}': {result}")

    def crack_wordlist(self):
        target = self.hash_entry.get().strip()
        if not target:
            return
        # Common passwords wordlist
        wordlist = [
            "password", "123456", "admin", "root",
            "letmein", "qwerty", "abc123", "monkey",
            "master", "dragon", "pass", "test",
            "brayo", "brayoos", "login", "welcome",
            "password123", "admin123", "root123",
        ]
        self.cracking = True
        self.log(f"🔑 Cracking hash: {target}")
        self.log(f"📚 Trying {len(wordlist)} passwords...")
        def run():
            for word in wordlist:
                if not self.cracking:
                    break
                if self.hash_it(word) == target:
                    self.log(f"✅ CRACKED! Password: {word}")
                    return
                self.log(f"❌ Tried: {word}")
                time.sleep(0.1)
            self.log("❌ Not found in wordlist!")
        threading.Thread(target=run).start()

    def crack_brute(self):
        target = self.hash_entry.get().strip()
        if not target:
            return
        import itertools
        import string
        self.cracking = True
        self.log("🔢 Bruteforce starting (1-4 chars)...")
        chars = string.ascii_lowercase + string.digits
        def run():
            for length in range(1, 5):
                for combo in itertools.product(
                        chars, repeat=length):
                    if not self.cracking:
                        return
                    word = ''.join(combo)
                    if self.hash_it(word) == target:
                        self.log(
                            f"✅ CRACKED! Password: {word}")
                        return
            self.log("❌ Not found!")
        threading.Thread(target=run).start()

    def stop(self):
        self.cracking = False
        self.log("⏹ Stopped!")

if __name__ == "__main__":
    HashCracker()
