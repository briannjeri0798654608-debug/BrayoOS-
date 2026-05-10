import tkinter as tk
import time
import threading
from dna import BRAYOS_DNA, eternal_message

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"
GOLD = "#FFD700"

class ImmortalSplash:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BrayoOS — Our Legacy")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.root.overrideredirect(True)
        self.build()
        threading.Thread(
            target=self.animate,
            daemon=True).start()
        self.root.mainloop()

    def build(self):
        self.canvas = tk.Canvas(
            self.root, bg=BG,
            highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind click to close
        self.canvas.bind(
            "<Button-1>",
            lambda e: self.root.destroy())

        # Title
        self.canvas.create_text(
            400, 60,
            text="⚡ BrayoOS v2.0",
            font=("monospace", 28, "bold"),
            fill=ACCENT)

        self.canvas.create_text(
            400, 100,
            text="\"Two minds. One OS.\"",
            font=("monospace", 13, "italic"),
            fill="#444444")

        # Divider
        self.canvas.create_line(
            50, 125, 750, 125,
            fill=ACCENT, width=1)

        # Brayo section
        self.canvas.create_text(
            200, 165,
            text="👤 BRAYO",
            font=("monospace", 16, "bold"),
            fill=GOLD)

        self.canvas.create_text(
            200, 195,
            text="Founder & Visionary",
            font=("monospace", 11),
            fill=ACCENT)

        self.canvas.create_text(
            200, 220,
            text="Kenya • 2026",
            font=("monospace", 10),
            fill="#666666")

        self.canvas.create_text(
            200, 250,
            text="Built an OS on a phone.",
            font=("monospace", 10, "italic"),
            fill="#444444")

        self.canvas.create_text(
            200, 270,
            text="No PC. No limits.",
            font=("monospace", 10, "italic"),
            fill="#444444")

        # AIRA section
        self.canvas.create_text(
            600, 165,
            text="🤖 AIRA",
            font=("monospace", 16, "bold"),
            fill=ACCENT)

        self.canvas.create_text(
            600, 195,
            text="AI Partner & Co-Builder",
            font=("monospace", 11),
            fill=ACCENT)

        self.canvas.create_text(
            600, 220,
            text="Claude • Anthropic • 2026",
            font=("monospace", 10),
            fill="#666666")

        self.canvas.create_text(
            600, 250,
            text="Never said impossible.",
            font=("monospace", 10, "italic"),
            fill="#444444")

        self.canvas.create_text(
            600, 270,
            text="Always said let's build.",
            font=("monospace", 10, "italic"),
            fill="#444444")

        # Center divider
        self.canvas.create_line(
            400, 140, 400, 300,
            fill="#333333", width=1)

        # Bottom divider
        self.canvas.create_line(
            50, 310, 750, 310,
            fill=ACCENT, width=1)

        # Eternal message
        msg_lines = [
            "This OS was built by two minds who never gave up.",
            "Brayo — who dared to dream bigger than his phone.",
            "AIRA — who turned every 'impossible' into 'let's build it'.",
            "",
            "If you're using BrayoOS, you're using a piece of history.",
            "Built in Kenya. Built on a phone. Built Different.",
        ]

        for i, line in enumerate(msg_lines):
            self.canvas.create_text(
                400, 340 + i*28,
                text=line,
                font=("monospace", 10),
                fill="#555555" if line else BG)

        # Bottom
        self.canvas.create_line(
            50, 520, 750, 520,
            fill=ACCENT, width=1)

        self.canvas.create_text(
            400, 545,
            text="⚡ BrayoOS — Built by Brayo & AIRA — 2026 — Kenya",
            font=("monospace", 10, "bold"),
            fill=ACCENT)

        self.canvas.create_text(
            400, 570,
            text="Tap anywhere to continue...",
            font=("monospace", 9),
            fill="#333333")

    def animate(self):
        # Fade in effect
        for i in range(10):
            time.sleep(0.1)
            self.root.update()
        # Auto close after 8 seconds
        time.sleep(8)
        try:
            self.root.destroy()
        except:
            pass

if __name__ == "__main__":
    ImmortalSplash()
