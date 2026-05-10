import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import random
import glob

class WallpaperChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Wallpaper Changer")
        self.root.geometry("500x420")
        self.root.configure(bg="#0D0D0D")
        self.selected = None
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="🖼️ WALLPAPER CHANGER", font=("Courier", 16, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=20)
        tk.Label(self.root, text="BrayoOS • Brayo & ARIA 🇰🇪", font=("Courier", 8),
                 bg="#0D0D0D", fg="#003300").pack()

        self.status = tk.Label(self.root, text="No image selected",
                               font=("Courier", 10), bg="#0D0D0D", fg="#888888", wraplength=450)
        self.status.pack(pady=15)

        # Preview box
        self.preview = tk.Label(self.root, text="[ PREVIEW ]", font=("Courier", 9),
                                bg="#001100", fg="#004400", width=50, height=4)
        self.preview.pack(padx=20, pady=5)

        btn = {"font": ("Courier", 11, "bold"), "width": 28, "bg": "#001a00",
               "fg": "#00FF41", "activebackground": "#00FF41",
               "activeforeground": "#000", "relief": "flat", "cursor": "hand2"}

        tk.Button(self.root, text="📁  Browse Image", command=self.browse, **btn).pack(pady=6)
        tk.Button(self.root, text="🎨  Set Wallpaper", command=self.set_wp, **btn).pack(pady=6)
        tk.Button(self.root, text="🔀  Random from ~/Pictures", command=self.random_wp, **btn).pack(pady=6)
        tk.Button(self.root, text="⬛  Clear (Black)", command=self.clear_wp, **btn).pack(pady=6)

        tk.Label(self.root, text="BrayoOS Wallpaper Engine v1.0",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=8)

    def browse(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All", "*.*")])
        if path:
            self.selected = path
            self.status.config(text=f"✅ {os.path.basename(path)}", fg="#00FF41")
            self.preview.config(text=f"[ {os.path.basename(path)} ]", fg="#00FF41")

    def set_wp(self):
        if not self.selected:
            messagebox.showwarning("No Image", "Browse an image first!")
            return
        try:
            subprocess.Popen(["feh", "--bg-scale", self.selected])
            self.status.config(text=f"✅ Wallpaper set!", fg="#00FF41")
        except:
            subprocess.Popen(f"DISPLAY=:1 feh --bg-scale '{self.selected}'", shell=True)

    def random_wp(self):
        pics = glob.glob(os.path.expanduser("~/Pictures/*"))
        imgs = [p for p in pics if p.lower().endswith(('.jpg','.jpeg','.png','.bmp'))]
        if not imgs:
            os.makedirs(os.path.expanduser("~/Pictures"), exist_ok=True)
            messagebox.showinfo("Empty", "Add images to ~/Pictures/ first!")
            return
        self.selected = random.choice(imgs)
        subprocess.Popen(["feh", "--bg-scale", self.selected])
        self.status.config(text=f"🔀 {os.path.basename(self.selected)}", fg="#00FF41")

    def clear_wp(self):
        subprocess.Popen("xsetroot -solid '#0D0D0D'", shell=True)
        self.status.config(text="⬛ Cleared to black", fg="#888888")
        self.selected = None

if __name__ == "__main__":
    root = tk.Tk()
    WallpaperChanger(root)
    root.mainloop()
