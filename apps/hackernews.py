# BrayoOS — Built by Brayo & ARIA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import scrolledtext
import httpx
import threading

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class HackerNews:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📰 Hacker News")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.load_news()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="📰 Hacker News",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill=tk.X, padx=10)

        for text, cmd in [("🔥 Top", self.load_top),
                          ("🆕 New", self.load_new),
                          ("🏆 Best", self.load_best)]:
            tk.Button(btn_frame, text=text, bg=DARK,
                     fg=ACCENT, command=cmd,
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=3)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=TEXT,
            font=("monospace", 10), wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def load_top(self):
        self.load_stories("topstories")

    def load_new(self):
        self.load_stories("newstories")

    def load_best(self):
        self.load_stories("beststories")

    def load_news(self):
        self.load_top()

    def load_stories(self, type_):
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "Loading stories...\n")
        def run():
            try:
                with httpx.Client() as client:
                    r = client.get(
                        f"https://hacker-news.firebaseio.com/v0/{type_}.json",
                        timeout=10)
                    ids = r.json()[:20]
                    
                    self.output.delete(1.0, tk.END)
                    for i, story_id in enumerate(ids, 1):
                        r2 = client.get(
                            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                            timeout=5)
                        story = r2.json()
                        self.output.insert(tk.END,
                            f"{i}. {story.get('title','')}\n"
                            f"   👤 {story.get('by','')}\n"
                            f"   ⬆️  {story.get('score',0)} points\n\n")
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}\n")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    HackerNews()
