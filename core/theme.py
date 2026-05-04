import tkinter as tk
from PIL import Image, ImageTk
import os

class ThemeEngine:
    THEMES = {
        "dark": {
            "bg": "#0D0D0D",
            "accent": "#00FF41",
            "text": "#FFFFFF",
            "dark": "#1A1A1A"
        },
        "neon": {
            "bg": "#0A0E27",
            "accent": "#00D9FF",
            "text": "#FFFFFF",
            "dark": "#1A2942"
        },
        "matrix": {
            "bg": "#000000",
            "accent": "#00FF00",
            "text": "#00AA00",
            "dark": "#001100"
        }
    }

    WALLPAPERS = {
        "default": None,
        "grid": "grid",
        "rain": "rain",
        "code": "code"
    }

    @staticmethod
    def create_gradient_wallpaper(width, height, color1, color2):
        """Create gradient wallpaper"""
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1-ratio) + color2[0] * ratio)
            g = int(color1[1] * (1-ratio) + color2[1] * ratio)
            b = int(color1[2] * (1-ratio) + color2[2] * ratio)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        return img

    @staticmethod
    def create_grid_wallpaper(width, height):
        """Create grid pattern wallpaper"""
        img = Image.new('RGB', (width, height), (13, 13, 13))
        pixels = img.load()
        grid_size = 50
        
        for x in range(0, width, grid_size):
            for y in range(height):
                pixels[x, y] = (65, 255, 65)
        
        for y in range(0, height, grid_size):
            for x in range(width):
                pixels[x, y] = (65, 255, 65)
        
        return img

    @staticmethod
    def save_wallpaper(wallpaper_type, path):
        """Save wallpaper to file"""
        if wallpaper_type == "grid":
            img = ThemeEngine.create_grid_wallpaper(1280, 720)
        else:
            img = ThemeEngine.create_gradient_wallpaper(
                1280, 720,
                (13, 13, 13),
                (25, 25, 25)
            )
        img.save(path)

if __name__ == "__main__":
    ThemeEngine.save_wallpaper(
        "grid",
        os.path.expanduser("~/BrayoOS/assets/wallpaper.png")
    )
    print("✅ Wallpaper created!")
