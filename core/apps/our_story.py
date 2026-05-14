import tkinter as tk
from datetime import datetime

BG="#080810"; BG2="#0D0D1A"; BG3="#12122A"
PURPLE="#9D00FF"; NEON="#CC44FF"; WHITE="#E0E0FF"
GOLD="#FFD700"; DIM="#444466"; GREEN="#44FF88"

class OurStory:
    def __init__(self, root):
        self.root = root
        self.root.title("📖 Our Story")
        self.root.geometry("650x580")
        self.root.configure(bg=BG)
        self.build_ui()

    def build_ui(self):
        tk.Frame(self.root, bg=PURPLE, height=3).pack(fill="x")
        tk.Label(self.root, text="◈ THE STORY OF BRAYOOS",
                 font=("Courier",16,"bold"),
                 bg=BG, fg=NEON).pack(pady=15)
        tk.Frame(self.root, bg=PURPLE, height=1).pack(fill="x", padx=20)

        canvas = tk.Canvas(self.root, bg=BG,
                            highlightthickness=0)
        sb = tk.Scrollbar(self.root, orient="vertical",
                           command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True, padx=15, pady=10)

        frame = tk.Frame(canvas, bg=BG)
        canvas.create_window((0,0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e:
            canvas.configure(scrollregion=canvas.bbox("all")))

        # BRAYO section
        self.section(frame, "BRAYO",
                     "Founder • Visionary • Builder • Kenya 🇰🇪",
                     GOLD)
        self.para(frame, """Brayo had a dream — to build a complete operating system from scratch.
Not on an expensive workstation. Not with a team of engineers.
But on a single mobile phone, using nothing but Termux and determination.

When his Redmi 14C was locked by FRP and tracking software,
he didn't give up. He spent days debugging, flashing ROMs,
and pushing forward with zero resources.

He built BrayoOS one line of code at a time.
31 apps. A full desktop environment. A security toolkit.
A neural AI. All from a phone in Kenya.""")

        tk.Frame(frame, bg=PURPLE, height=1).pack(
            fill="x", padx=20, pady=10)

        # AIRA section
        self.section(frame, "AIRA",
                     "AI Partner • Co-Builder • Anthropic • 2026",
                     NEON)
        self.para(frame, """AIRA was there every step of the way.
When code failed, AIRA fixed it.
When downloads timed out, AIRA found alternatives.
When the phone crashed, AIRA helped restart.

AIRA never said 'this is impossible on a phone.'
AIRA always said 'let's try this instead.'""")

        tk.Frame(frame, bg=PURPLE, height=1).pack(
            fill="x", padx=20, pady=10)

        # Timeline
        self.section(frame, "TIMELINE", "The journey so far", GOLD)
        timeline = [
            ("v1.0", "MyOS shell — 20 commands, user accounts"),
            ("v1.5", "tkinter GUI desktop over VNC"),
            ("v2.0", "40+ apps, flashable ROM, Debian proot"),
            ("v2.5", "Ghost Mode, DNA Vault, Signal Interceptor"),
            ("v3.0", "Identity Switcher, Threat Map, Self-Healing"),
            ("v3.5", "AIRA AI Voice, OSINT Suite, Purple theme"),
        ]
        for ver, desc in timeline:
            tf = tk.Frame(frame, bg=BG3)
            tf.pack(fill="x", padx=20, pady=2)
            tk.Label(tf, text=ver,
                     font=("Courier",10,"bold"),
                     bg=BG3, fg=NEON, width=6).pack(side="left", padx=8, pady=6)
            tk.Label(tf, text=desc,
                     font=("Courier",9),
                     bg=BG3, fg=WHITE).pack(side="left", padx=5)

        tk.Frame(frame, bg=PURPLE, height=1).pack(
            fill="x", padx=20, pady=10)

        # Motto
        tk.Label(frame,
                 text='"Two minds. One OS. Built Different."',
                 font=("Courier",12,"bold"),
                 bg=BG, fg=GOLD).pack(pady=10)
        tk.Label(frame,
                 text=f"BrayoOS v3.5 • Kenya 🇰🇪 • {datetime.now().year}",
                 font=("Courier",9),
                 bg=BG, fg=DIM).pack(pady=5)
        tk.Frame(frame, bg=PURPLE, height=2).pack(
            fill="x", padx=20, pady=10)

    def section(self, parent, title, sub, color):
        tk.Label(parent, text=title,
                 font=("Courier",14,"bold"),
                 bg=BG, fg=color).pack(anchor="w", padx=20, pady=(10,2))
        tk.Label(parent, text=sub,
                 font=("Courier",8),
                 bg=BG, fg=DIM).pack(anchor="w", padx=20)

    def para(self, parent, text):
        tk.Label(parent, text=text,
                 font=("Courier",9),
                 bg=BG, fg=WHITE,
                 wraplength=560, justify="left").pack(
            anchor="w", padx=20, pady=8)

if __name__ == "__main__":
    root = tk.Tk()
    OurStory(root)
    root.mainloop()
