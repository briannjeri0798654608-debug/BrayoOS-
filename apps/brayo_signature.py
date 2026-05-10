import tkinter as tk
import time
import math

BG = "#0D0D0D"
ACCENT = "#00FF41"
GOLD = "#FFD700"

class BrayoSignature:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ BrayoOS Signature")
        self.root.configure(bg=BG)
        self.root.geometry("600x400")
        self.canvas = tk.Canvas(
            self.root, bg=BG,
            highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.animate()
        self.root.mainloop()

    def animate(self):
        self.canvas.delete("all")
        t = time.time()

        # Pulsing circle
        r = 50 + 10 * math.sin(t * 2)
        self.canvas.create_oval(
            300-r, 150-r, 300+r, 150+r,
            outline=ACCENT, width=2)

        # Title
        self.canvas.create_text(
            300, 150,
            text="⚡",
            font=("monospace", 40),
            fill=ACCENT)

        # Name
        self.canvas.create_text(
            300, 230,
            text="BrayoOS",
            font=("monospace", 32, "bold"),
            fill=ACCENT)

        self.canvas.create_text(
            300, 270,
            text="Built by Brayo & Virgy",
            font=("monospace", 14),
            fill=GOLD)

        self.canvas.create_text(
            300, 300,
            text="Kenya • 2026",
            font=("monospace", 12),
            fill="#444444")

        self.canvas.create_text(
            300, 340,
            text="\"Two minds. One OS. Built Different.\"",
            font=("monospace", 10, "italic"),
            fill="#333333")

        # Rotating dots
        for i in range(8):
            angle = t * 2 + i * math.pi / 4
            x = 300 + 80 * math.cos(angle)
            y = 150 + 80 * math.sin(angle)
            size = 3 + math.sin(t * 3 + i) * 2
            self.canvas.create_oval(
                x-size, y-size,
                x+size, y+size,
                fill=ACCENT, outline="")

        self.root.after(50, self.animate)

if __name__ == "__main__":
    BrayoSignature()
