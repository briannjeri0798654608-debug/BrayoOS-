import tkinter as tk
from tkinter import scrolledtext
import httpx
import threading
import re

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class MiniBrowser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌐 Mini Browser")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.history = []
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🌐 BrayoOS Browser",
                bg=BG, fg=ACCENT,
                font=("monospace", 14, "bold")).pack(pady=5)

        nav = tk.Frame(self.root, bg=BG)
        nav.pack(fill=tk.X, padx=10)

        tk.Button(nav, text="◀ Back", bg=DARK, fg=TEXT,
                 command=self.go_back).pack(side=tk.LEFT)
        tk.Button(nav, text="🔄 Refresh", bg=DARK, fg=TEXT,
                 command=self.reload).pack(side=tk.LEFT, padx=2)

        self.url_entry = tk.Entry(nav, bg=DARK, fg=ACCENT,
                                 font=("monospace", 10),
                                 insertbackground=ACCENT)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X,
                           expand=True, padx=5)
        self.url_entry.insert(0, "https://example.com")
        self.url_entry.bind("<Return>", lambda e: self.load())

        tk.Button(nav, text="Go", bg=ACCENT, fg=BG,
                 command=self.load).pack(side=tk.LEFT)

        # Quick links
        links = tk.Frame(self.root, bg=BG)
        links.pack(fill=tk.X, padx=10, pady=3)

        for name, url in [("Google", "google.com"),
                          ("News", "news.ycombinator.com"),
                          ("GitHub", "github.com")]:
            tk.Button(links, text=name, bg=DARK, fg=TEXT,
                     font=("monospace", 8),
                     command=lambda u=url: self.goto(u),
                     relief=tk.FLAT).pack(side=tk.LEFT, padx=2)

        self.content = scrolledtext.ScrolledText(
            self.root, bg=DARK, fg=TEXT,
            font=("monospace", 9), wrap=tk.WORD)
        self.content.pack(fill=tk.BOTH, expand=True,
                         padx=10, pady=5)

    def goto(self, url):
        self.url_entry.delete(0, tk.END)
        if not url.startswith("http"):
            url = "https://" + url
        self.url_entry.insert(0, url)
        self.load()

    def load(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http"):
            url = "https://" + url
        self.history.append(url)
        self.content.delete(1.0, tk.END)
        self.content.insert(tk.END, f"Loading {url}...\n")
        def run():
            try:
                with httpx.Client(follow_redirects=True,
                                 timeout=10,
                                 headers={"User-Agent": "BrayoOS/2.0"}) as client:
                    r = client.get(url)
                    text = r.text
                    # Remove HTML tags
                    clean = re.sub(r'<[^>]+>', '', text)
                    clean = re.sub(r'\n\s*\n', '\n\n', clean)
                    clean = clean.replace('&nbsp;', ' ')
                    clean = clean.replace('&amp;', '&')
                    self.content.delete(1.0, tk.END)
                    self.content.insert(1.0, clean[:50000])
            except Exception as e:
                self.content.delete(1.0, tk.END)
                self.content.insert(1.0, f"❌ Error: {e}")
        threading.Thread(target=run).start()

    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.goto(self.history[-1])

    def reload(self):
        self.load()

if __name__ == "__main__":
    MiniBrowser()
