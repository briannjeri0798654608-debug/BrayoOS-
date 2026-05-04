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
