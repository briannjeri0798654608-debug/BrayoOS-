# BrayoOS — Built by Brayo & ARIA — Kenya 2026
# Copyright (C) 2026 Brayo. GPL-3.0 License

import tkinter as tk
from tkinter import simpledialog, scrolledtext
import httpx
import threading

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class Weather:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌤️ Weather")
        self.root.configure(bg=BG)
        self.root.geometry("700x500")
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🌤️ Weather Forecast",
                bg=BG, fg=ACCENT,
                font=("monospace", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.X, padx=10)

        self.city_entry = tk.Entry(frame, bg=DARK, fg=ACCENT,
                                  font=("monospace", 11),
                                  insertbackground=ACCENT)
        self.city_entry.pack(side=tk.LEFT, fill=tk.X,
                            expand=True, padx=5)
        self.city_entry.insert(0, "London")

        tk.Button(frame, text="🔍 Search",
                 bg=ACCENT, fg=BG,
                 command=self.search).pack(side=tk.LEFT)

        self.output = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def search(self):
        city = self.city_entry.get().strip()
        if not city:
            return
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Fetching weather for {city}...\n")
        def run():
            try:
                with httpx.Client() as client:
                    r = client.get(
                        f"https://wttr.in/{city}?format=j1",
                        timeout=10)
                    data = r.json()
                    current = data['current_condition'][0]
                    
                    self.output.delete(1.0, tk.END)
                    self.output.insert(tk.END,
                        f"🌤️  Weather in {city}\n"
                        f"{'═'*50}\n"
                        f"🌡️  Temp: {current['temp_C']}°C\n"
                        f"💧 Humidity: {current['humidity']}%\n"
                        f"💨 Wind: {current['windspeedKmph']} km/h\n"
                        f"☁️  Condition: {current['weatherDesc'][0]['value']}\n")
            except Exception as e:
                self.output.insert(tk.END, f"Error: {e}\n")
        threading.Thread(target=run).start()

if __name__ == "__main__":
    Weather()
