import tkinter as tk
import time
import datetime

BG = "#0D0D0D"
ACCENT = "#00FF41"
DARK = "#1A1A1A"

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🕐 Clock")
        self.root.configure(bg=BG)
        self.root.geometry("400x300")
        self.build_ui()
        self.update()
        self.root.mainloop()

    def build_ui(self):
        self.time_label = tk.Label(
            self.root, text="",
            bg=BG, fg=ACCENT,
            font=("monospace", 48, "bold"))
        self.time_label.pack(pady=20)

        self.date_label = tk.Label(
            self.root, text="",
            bg=BG, fg="#444444",
            font=("monospace", 14))
        self.date_label.pack()

        self.day_label = tk.Label(
            self.root, text="",
            bg=BG, fg="#333333",
            font=("monospace", 12))
        self.day_label.pack(pady=5)

        tk.Label(self.root,
                text="⚡ BrayoOS — Kenya 2026",
                bg=BG, fg="#222222",
                font=("monospace", 9)).pack(
                    side=tk.BOTTOM, pady=10)

    def update(self):
        now = datetime.datetime.now()
        self.time_label.config(
            text=now.strftime("%H:%M:%S"))
        self.date_label.config(
            text=now.strftime("%d %B %Y"))
        self.day_label.config(
            text=now.strftime("%A"))
        self.root.after(1000, self.update)

if __name__ == "__main__":
    Clock()
