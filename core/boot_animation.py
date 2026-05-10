import tkinter as tk
import threading
import time
import os
import math
import subprocess

class BrayoOSBoot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#000000")
        self.root.title("BrayoOS")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.phase = 0
        self.glow_angle = 0
        self.build_ui()
        threading.Thread(target=self.sequence, daemon=True).start()
        self.root.mainloop()

    def build_ui(self):
        # Full canvas for drawing
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height,
                                bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Bottom text labels over canvas
        self.powered_lbl = tk.Label(self.root, text="",
                                     font=("Courier", 10), bg="#000000",
                                     fg="#888888")
        self.powered_lbl.place(relx=0.5, rely=0.88, anchor="center")

        self.aira_lbl = tk.Label(self.root, text="",
                                  font=("Courier", 9), bg="#000000",
                                  fg="#004400")
        self.aira_lbl.place(relx=0.5, rely=0.93, anchor="center")

        self.status_lbl = tk.Label(self.root, text="",
                                    font=("Courier", 8), bg="#000000",
                                    fg="#003300")
        self.status_lbl.place(relx=0.5, rely=0.96, anchor="center")

    def draw_logo(self, glow_radius=120, alpha=1.0, scale=1.0):
        self.canvas.delete("all")
        cx = self.width // 2
        cy = int(self.height * 0.38)
        r = int(80 * scale)

        # Outer glow rings — gold
        glow_colors = ["#1a1100", "#2a1e00", "#3d2d00", "#5c4400",
                       "#856200", "#B8860B", "#DAA520", "#FFD700"]
        for i, color in enumerate(glow_colors):
            gr = r + glow_radius - (i * glow_radius // len(glow_colors))
            self.canvas.create_oval(cx-gr, cy-gr, cx+gr, cy+gr,
                                     outline=color, width=1)

        # Rotating glow arc — green
        for i in range(12):
            angle = math.radians(self.glow_angle + i * 30)
            gr2 = r + 30
            x1 = cx + gr2 * math.cos(angle)
            y1 = cy + gr2 * math.sin(angle)
            intensity = int(255 * (i / 12))
            color = f"#00{intensity:02x}00" if intensity > 15 else "#001100"
            self.canvas.create_oval(x1-4, y1-4, x1+4, y1+4,
                                     fill=color, outline="")

        # Main orb — dark green fill with gold border
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                 fill="#001a00", outline="#FFD700", width=3)

        # Inner orb glow
        for ir, ic in [(r-8, "#002200"), (r-18, "#003300"),
                        (r-28, "#004400"), (r-38, "#005500")]:
            self.canvas.create_oval(cx-ir, cy-ir, cx+ir, cy+ir,
                                     fill=ic, outline="")

        # Center bright spot
        self.canvas.create_oval(cx-15, cy-15, cx+15, cy+15,
                                 fill="#00FF41", outline="#FFD700", width=2)

        # B letter in center
        self.canvas.create_text(cx, cy, text="B",
                                 font=("Courier", int(42*scale), "bold"),
                                 fill="#FFD700")

        # Circuit lines radiating out
        for i in range(8):
            angle = math.radians(i * 45 + self.glow_angle * 0.3)
            x1 = cx + (r+5) * math.cos(angle)
            y1 = cy + (r+5) * math.sin(angle)
            x2 = cx + (r+40) * math.cos(angle)
            y2 = cy + (r+40) * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2,
                                     fill="#FFD700", width=1)
            # Circuit dot at end
            self.canvas.create_oval(x2-3, y2-3, x2+3, y2+3,
                                     fill="#00FF41", outline="")

        # OS Name
        name_y = cy + r + 55
        self.canvas.create_text(cx, name_y, text="BrayoOS",
                                 font=("Courier", int(32*scale), "bold"),
                                 fill="#00FF41")

        # Version
        self.canvas.create_text(cx, name_y + 38,
                                 text="v3.5",
                                 font=("Courier", 14),
                                 fill="#FFD700")

    def draw_progress_bar(self, pct):
        cx = self.width // 2
        by = int(self.height * 0.75)
        bar_w = 200
        bar_h = 4

        # Background bar
        self.canvas.create_rectangle(cx - bar_w//2, by,
                                      cx + bar_w//2, by + bar_h,
                                      fill="#111111", outline="")
        # Fill
        fill_w = int(bar_w * pct / 100)
        if fill_w > 0:
            self.canvas.create_rectangle(cx - bar_w//2, by,
                                          cx - bar_w//2 + fill_w, by + bar_h,
                                          fill="#00FF41", outline="")
        # Dot at end
        dot_x = cx - bar_w//2 + fill_w
        self.canvas.create_oval(dot_x-4, by-2, dot_x+4, by+6,
                                 fill="#FFD700", outline="")

    def sequence(self):
        # PHASE 1 — Black screen (like a phone booting)
        time.sleep(0.8)

        # PHASE 2 — Logo fade in from tiny to full
        for scale in [0.2, 0.4, 0.6, 0.8, 1.0, 1.05, 1.0]:
            self.root.after(0, self.draw_logo, 120, 1.0, scale)
            time.sleep(0.08)

        # PHASE 3 — Glow rotation animation
        for frame in range(60):
            self.glow_angle += 6
            self.root.after(0, self.draw_logo, 120, 1.0, 1.0)
            time.sleep(0.03)

        # PHASE 4 — "Powered by BrayoOS" appears
        self.root.after(0, self.powered_lbl.config,
                        {"text": "Powered by BrayoOS"})
        time.sleep(0.5)

        # PHASE 5 — AIRA appears
        self.root.after(0, self.aira_lbl.config,
                        {"text": "✦  AIRA  •  AI Partner  •  Always Watching  ✦"})
        time.sleep(0.5)

        # PHASE 6 — Progress bar loads
        boot_msgs = [
            "Initializing kernel...",
            "Loading AIRA neural core...",
            "Arming security modules...",
            "Encrypting DNA Vault...",
            "Activating Ghost Mode...",
            "Scanning dark web...",
            "All systems ready...",
        ]
        for i, msg in enumerate(boot_msgs):
            pct = int((i+1) * 100 / len(boot_msgs))
            self.root.after(0, self.status_lbl.config, {"text": msg})
            self.root.after(0, self.draw_logo, 120, 1.0, 1.0)
            self.root.after(0, self.draw_progress_bar, pct)
            self.glow_angle += 15
            time.sleep(0.4)

        # PHASE 7 — Flash white like phone boot
        for bg in ["#001100", "#003300", "#006600", "#00FF41",
                   "#ffffff", "#00FF41", "#003300", "#000000"]:
            self.root.after(0, self.canvas.configure, {"bg": bg})
            time.sleep(0.06)

        self.root.after(0, self.canvas.configure, {"bg": "#000000"})
        time.sleep(0.3)

        # PHASE 8 — Launch desktop
        self.root.after(0, self.launch_desktop)

    def launch_desktop(self):
        self.root.destroy()
        env = os.environ.copy()
        env["DISPLAY"] = ":1"
        subprocess.Popen(
            ["python3", os.path.expanduser("~/BrayoOS/core/desktop.py")],
            env=env)

if __name__ == "__main__":
    BrayoOSBoot()
