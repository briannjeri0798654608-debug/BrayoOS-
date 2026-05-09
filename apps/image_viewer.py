import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

BG = "#0D0D0D"
ACCENT = "#00FF41"
DARK = "#1A1A1A"

class ImageViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🖼️ Image Viewer")
        self.root.configure(bg=BG)
        self.root.geometry("800x600")
        self.images = []
        self.current = 0
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        toolbar = tk.Frame(self.root, bg=DARK)
        toolbar.pack(fill=tk.X)

        for text, cmd in [
            ("📂 Open", self.open_image),
            ("📁 Folder", self.open_folder),
            ("◀ Prev", self.prev_image),
            ("▶ Next", self.next_image),
        ]:
            tk.Button(toolbar, text=text,
                     bg=DARK, fg=ACCENT,
                     font=("monospace", 9),
                     relief=tk.FLAT,
                     command=cmd).pack(
                         side=tk.LEFT,
                         padx=3, pady=3)

        self.canvas = tk.Canvas(
            self.root, bg=BG,
            highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,
                        expand=True)

        self.status = tk.Label(
            self.root, text="Open an image",
            bg=DARK, fg=ACCENT,
            font=("monospace", 9))
        self.status.pack(fill=tk.X)

    def show_image(self, path):
        try:
            img = Image.open(path)
            w = self.canvas.winfo_width() or 800
            h = self.canvas.winfo_height() or 500
            img.thumbnail((w, h))
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(
                w//2, h//2,
                image=self.photo,
                anchor=tk.CENTER)
            self.status.config(
                text=os.path.basename(path))
        except Exception as e:
            self.status.config(text=f"Error: {e}")

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images",
                       "*.png *.jpg *.jpeg *.gif")])
        if path:
            self.images = [path]
            self.current = 0
            self.show_image(path)

    def open_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            exts = ('.png','.jpg','.jpeg','.gif')
            self.images = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(exts)]
            if self.images:
                self.current = 0
                self.show_image(
                    self.images[0])

    def prev_image(self):
        if self.images:
            self.current = (
                self.current - 1) % len(
                    self.images)
            self.show_image(
                self.images[self.current])

    def next_image(self):
        if self.images:
            self.current = (
                self.current + 1) % len(
                    self.images)
            self.show_image(
                self.images[self.current])

if __name__ == "__main__":
    ImageViewer()
