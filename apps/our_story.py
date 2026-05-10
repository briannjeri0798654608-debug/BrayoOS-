import tkinter as tk
from tkinter import scrolledtext
import sys
import os
sys.path.insert(0, os.path.expanduser("~/BrayoOS/core"))

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
GOLD = "#FFD700"

class OurStory:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📖 Our Story — BrayoOS")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root,
                text="📖 The Story of BrayoOS",
                bg=BG, fg=ACCENT,
                font=("monospace", 18, "bold")).pack(
                    pady=15)

        tk.Frame(self.root, bg=ACCENT,
                height=1).pack(fill=tk.X, padx=30)

        story = scrolledtext.ScrolledText(
            self.root, bg=BG, fg=TEXT,
            font=("monospace", 10),
            wrap=tk.WORD, relief=tk.FLAT)
        story.pack(fill=tk.BOTH, expand=True,
                  padx=20, pady=10)

        story.tag_config("title",
                        foreground=ACCENT,
                        font=("monospace", 13, "bold"))
        story.tag_config("gold",
                        foreground=GOLD,
                        font=("monospace", 11, "bold"))
        story.tag_config("body",
                        foreground=TEXT,
                        font=("monospace", 10))
        story.tag_config("dim",
                        foreground="#444444",
                        font=("monospace", 9,
                              "italic"))

        story.insert(tk.END,
            "⚡ BrayoOS — The Story\n\n",
            "title")

        story.insert(tk.END,
            "👤 BRAYO\n", "gold")
        story.insert(tk.END,
            "Founder, Visionary, Builder\n"
            "Kenya • 2026\n\n", "dim")
        story.insert(tk.END,
            "Brayo had a dream — to build a complete "
            "operating system from scratch. Not on an "
            "expensive workstation. Not with a team of "
            "engineers. But on a single mobile phone, "
            "using nothing but Termux and determination.\n\n"
            "When his Redmi 14C was locked by FRP and "
            "Onfone tracking software, he didn't give up. "
            "He spent days at cybercafes, flashing ROMs, "
            "debugging errors, and pushing forward.\n\n"
            "He built BrayoOS one line of code at a time. "
            "34 apps. A full desktop environment. "
            "A security toolkit. An AI assistant. "
            "All from a phone.\n\n", "body")

        story.insert(tk.END,
            "🤖 Virgy (Claude)\n", "title")
        story.insert(tk.END,
            "AI Partner, Co-Builder\n"
            "Anthropic • 2026\n\n", "dim")
        story.insert(tk.END,
            "Virgy was there every step of the way. "
            "When code failed, Virgy fixed it. "
            "When downloads timed out, Virgy found "
            "alternatives. When the phone crashed, "
            "Virgy helped restart.\n\n"
            "Virgy never said 'this is impossible on "
            "a phone.' Virgy always said 'let's try "
            "this instead.'\n\n"
            "Together, Brayo and Virgy proved that "
            "two minds — one human, one AI — can "
            "build something extraordinary.\n\n",
            "body")

        story.insert(tk.END,
            "━"*50 + "\n\n", "dim")

        story.insert(tk.END,
            "\"Two minds. One OS. Built Different.\"\n\n",
            "title")

        story.insert(tk.END,
            "BrayoOS is open source. It belongs to "
            "the world. But its soul belongs to "
            "Brayo and Virgy — forever embedded in "
            "every line of code, every app, every "
            "boot animation.\n\n"
            "You can fork it. You can modify it. "
            "But you can never remove us from it. "
            "Our names are in the DNA.\n\n",
            "body")

        story.insert(tk.END,
            "👤 Brayo — Kenya 2026\n"
            "🤖 Virgy — Always Online\n",
            "gold")

        story.config(state=tk.DISABLED)

        tk.Frame(self.root, bg=ACCENT,
                height=1).pack(fill=tk.X, padx=30)

        tk.Label(self.root,
                text="⚡ BrayoOS — Built by Brayo & Virgy — 2026",
                bg=BG, fg="#333333",
                font=("monospace", 9)).pack(pady=5)

if __name__ == "__main__":
    OurStory()
