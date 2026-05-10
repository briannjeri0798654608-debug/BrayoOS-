import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import random
import glob
from PIL import Image, ImageTk

class WallpaperChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Wallpaper Changer")
        self.root.geometry("520x480")
        self.root.configure(bg="#0D0D0D")
        self.selected = None
        self.build_ui()
        self.load_thumbnails()

    def build_ui(self):
        tk.Label(self.root, text="🖼️ WALLPAPER CHANGER", font=("Courier", 16, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=10)
        tk.Label(self.root, text="BrayoOS • AIRA 🇰🇪", font=("Courier", 8),
                 bg="#0D0D0D", fg="#003300").pack()

        self.status = tk.Label(self.root, text="Select a wallpaper below",
                               font=("Courier", 10), bg="#0D0D0D",
                               fg="#888888", wraplength=480)
        self.status.pack(pady=8)

        # Thumbnail grid
        tk.Label(self.root, text="◈ ~/Pictures/", font=("Courier", 9, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.thumb_frame = tk.Frame(self.root, bg="#001100")
        self.thumb_frame.pack(fill="x", padx=15, pady=5)

        btn = {"font": ("Courier", 10, "bold"), "width": 24, "bg": "#001a00",
               "fg": "#00FF41", "activebackground": "#00FF41",
               "activeforeground": "#000", "relief": "flat", "cursor": "hand2"}

        tk.Button(self.root, text="📁  Browse Any Image", command=self.browse, **btn).pack(pady=4)
        tk.Button(self.root, text="🎨  Set Selected Wallpaper", command=self.set_wp, **btn).pack(pady=4)
        tk.Button(self.root, text="🔀  Random Wallpaper", command=self.random_wp, **btn).pack(pady=4)
        tk.Button(self.root, text="⬛  Reset to Black", command=self.clear_wp, **btn).pack(pady=4)

        tk.Label(self.root, text="BrayoOS Wallpaper Engine v2.0 • AIRA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=6)

    def load_thumbnails(self):
        for w in self.thumb_frame.winfo_children():
            w.destroy()
        pics = glob.glob(os.path.expanduser("~/Pictures/*"))
        imgs = [p for p in pics if p.lower().endswith(('.jpg','.jpeg','.png','.bmp','.webp'))]
        if not imgs:
            tk.Label(self.thumb_frame, text="No images in ~/Pictures/",
                     font=("Courier", 9), bg="#001100", fg="#004400").pack(pady=10)
            return
        for i, path in enumerate(imgs[:6]):
            try:
                img = Image.open(path).resize((100, 65))
                photo = ImageTk.PhotoImage(img)
                btn = tk.Button(self.thumb_frame, image=photo,
                                command=lambda p=path: self.select_image(p),
                                bg="#001100", relief="flat", cursor="hand2")
                btn.image = photo
                btn.grid(row=i//3, column=i%3, padx=4, pady=4)
            except:
                name = os.path.basename(path)[:12]
                tk.Button(self.thumb_frame, text=name,
                          font=("Courier", 8), bg="#002200", fg="#00FF41",
                          relief="flat", command=lambda p=path: self.select_image(p),
                          width=12, height=3).grid(row=i//3, column=i%3, padx=4, pady=4)

    def select_image(self, path):
        self.selected = path
        self.status.config(text=f"✅ {os.path.basename(path)}", fg="#00FF41")

    def browse(self):
        path = filedialog.askopenfilename(
            initialdir=os.path.expanduser("~/Pictures"),
            title="Select Image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All", "*.*")])
        if path:
            self.select_image(path)
            self.load_thumbnails()

    def set_wp(self):
        if not self.selected:
            messagebox.showwarning("No Image", "Select an image first!")
            return
        result = subprocess.run(
            f"DISPLAY=:1 feh --bg-scale '{self.selected}'",
            shell=True)
        if result.returncode == 0:
            self.status.config(text=f"✅ Wallpaper applied!", fg="#00FF41")
        else:
            subprocess.run(f"DISPLAY=:1 xsetroot -solid '#0D2B0D'", shell=True)
            self.status.config(text="⚠️ Used solid color fallback", fg="#FF6600")

    def random_wp(self):
        pics = glob.glob(os.path.expanduser("~/Pictures/*"))
        imgs = [p for p in pics if p.lower().endswith(('.jpg','.jpeg','.png','.bmp'))]
        if not imgs:
            messagebox.showinfo("Empty", "Add images to ~/Pictures/ first!")
            return
        import random
        self.selected = random.choice(imgs)
        subprocess.run(f"DISPLAY=:1 feh --bg-scale '{self.selected}'", shell=True)
        self.status.config(text=f"🔀 {os.path.basename(self.selected)}", fg="#00FF41")
        self.load_thumbnails()

    def clear_wp(self):
        subprocess.run("DISPLAY=:1 xsetroot -solid '#0D0D0D'", shell=True)
        self.status.config(text="⬛ Reset to black", fg="#888888")
        self.selected = None

if __name__ == "__main__":
    root = tk.Tk()
    WallpaperChanger(root)
    root.mainloop()
