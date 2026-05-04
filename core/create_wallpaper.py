from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs(os.path.expanduser("~/BrayoOS/assets"), exist_ok=True)

# Create gradient background
img = Image.new('RGB', (1280, 720))
pixels = img.load()

for y in range(720):
    ratio = y / 720
    r = int(13 * (1 - ratio) + 30 * ratio)
    g = int(13 * (1 - ratio) + 13 * ratio)
    b = int(13 * (1 - ratio) + 50 * ratio)
    
    for x in range(1280):
        pixels[x, y] = (r, g, b)

# Add subtle grid
draw = ImageDraw.Draw(img)
for x in range(0, 1280, 80):
    draw.line([(x, 0), (x, 720)], fill=(65, 255, 65, 30), width=1)
for y in range(0, 720, 80):
    draw.line([(0, y), (1280, y)], fill=(65, 255, 65, 30), width=1)

img.save(os.path.expanduser("~/BrayoOS/assets/wallpaper.png"))
print("✅ Wallpaper created!")
