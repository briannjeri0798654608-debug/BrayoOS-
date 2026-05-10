# BrayoOS — Built by Brayo & Virgy — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class MusicPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎵 Music Player")
        self.root.configure(bg=BG)
        self.root.geometry("600x500")
        self.build_ui()
        self.load_music()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🎵 Music Player",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)
        self.listbox = tk.Listbox(self.root, bg=DARK, fg=TEXT,
                                 font=("monospace", 11),
                                 selectbackground=ACCENT,
                                 selectforeground=BG)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10)
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=10)
        for text, cmd in [("▶ Play", self.play),
                          ("⏸ Pause", self.pause),
                          ("⏹ Stop", self.stop)]:
            tk.Button(btn_frame, text=text, bg=DARK,
                     fg=ACCENT, font=("monospace", 11),
                     command=cmd, relief=tk.FLAT).pack(
                         side=tk.LEFT, padx=3)
        self.status = tk.Label(self.root, text="No track",
                              bg=DARK, fg=ACCENT,
                              font=("monospace", 10))
        self.status.pack(fill=tk.X)

    def load_music(self):
        paths = ["/sdcard/Music", "/sdcard/Download"]
        for path in paths:
            if os.path.exists(path):
                for f in os.listdir(path):
                    if f.endswith(('.mp3','.wav','.ogg','.m4a')):
                        self.listbox.insert(tk.END,
                            os.path.join(path, f))

    def play(self):
        if self.listbox.curselection():
            track = self.listbox.get(self.listbox.curselection())
            subprocess.Popen(["termux-media-player", "play", track])
            self.status.config(text=f"▶ {os.path.basename(track)}")

    def pause(self):
        subprocess.Popen(["termux-media-player", "pause"])
        self.status.config(text="⏸ Paused")

    def stop(self):
        subprocess.Popen(["termux-media-player", "stop"])
        self.status.config(text="⏹ Stopped")

if __name__ == "__main__":
    MusicPlayer()
