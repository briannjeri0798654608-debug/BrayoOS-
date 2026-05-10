import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import json
import subprocess
import httpx
from datetime import datetime

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
BLOGS_DIR = os.path.expanduser("~/BrayoOS/blogs/")
os.makedirs(BLOGS_DIR, exist_ok=True)

GITHUB_USER = "briannjeri0798654608-debug"
GITHUB_REPO = "BrayoOS-"

AIRA_WEB_PROMPT = """You are AIRA, AI of BrayoOS built by Brayo in Kenya.
When asked to create a blog/website, respond ONLY with valid JSON:
{
  "title": "Blog title here",
  "slug": "url-friendly-slug",
  "description": "One line description",
  "content": "Full HTML body content here with proper tags",
  "social_caption": "Social media caption with hashtags"
}
Make the HTML content beautiful, modern, dark themed with purple accents.
Include proper headings, paragraphs, and styling."""

BG = "#080810"
BG2 = "#0D0D1A"
BG3 = "#12122A"
PURPLE = "#9D00FF"
NEON = "#CC44FF"
WHITE = "#E0E0FF"
DIM = "#444466"

class AIRAWebAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 AIRA Web Agent")
        self.root.geometry("750x620")
        self.root.configure(bg=BG)
        self.blogs = []
        self.build_ui()
        self.log("🌐 AIRA Web Agent online. Ready to publish, Brayo.")
        self.log("💡 Try: 'Create a blog about BrayoOS features'")

    def build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=BG2, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="◈ AIRA WEB AGENT",
                 font=("Courier", 16, "bold"),
                 bg=BG2, fg=NEON).pack(side="left", padx=15, pady=10)
        tk.Label(hdr, text="Create • Publish • Share",
                 font=("Courier", 9),
                 bg=BG2, fg=DIM).pack(side="left")
        tk.Label(hdr, text="🇰🇪 BrayoOS v3.5",
                 font=("Courier", 9),
                 bg=BG2, fg=PURPLE).pack(side="right", padx=15)

        tk.Frame(self.root, bg=PURPLE, height=2).pack(fill="x")

        # Main area
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # Left — chat/command
        left = tk.Frame(main, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="◈ TELL AIRA WHAT TO CREATE",
                 font=("Courier", 9, "bold"),
                 bg=BG, fg=PURPLE).pack(anchor="w")

        # Quick command buttons
        qf = tk.Frame(left, bg=BG)
        qf.pack(fill="x", pady=5)
        quick_cmds = [
            "Blog about BrayoOS",
            "Tech article about hacking",
            "My portfolio website",
            "About Kenya tech scene",
        ]
        for cmd in quick_cmds:
            tk.Button(qf, text=cmd,
                      font=("Courier", 7), bg=BG3, fg=NEON,
                      relief="flat", padx=6, pady=3,
                      activebackground=PURPLE,
                      command=lambda c=cmd: self.quick_set(c)
                      ).pack(side="left", padx=2)

        # Input
        input_f = tk.Frame(left, bg=BG3)
        input_f.pack(fill="x", pady=5)
        tk.Label(input_f, text="▶", font=("Courier", 11),
                 bg=BG3, fg=PURPLE).pack(side="left", padx=8)
        self.cmd_input = tk.Entry(input_f, font=("Courier", 10),
                                   bg=BG3, fg=WHITE,
                                   insertbackground=NEON,
                                   relief="flat")
        self.cmd_input.pack(side="left", fill="x", expand=True, ipady=8)
        self.cmd_input.bind("<Return>", lambda e: self.execute())
        tk.Button(input_f, text="CREATE ▶",
                  font=("Courier", 9, "bold"),
                  bg=PURPLE, fg=WHITE, relief="flat",
                  padx=10, activebackground=NEON,
                  command=self.execute).pack(side="right", padx=5, pady=4)

        # AIRA log
        tk.Label(left, text="◈ AIRA LOG",
                 font=("Courier", 9, "bold"),
                 bg=BG, fg=PURPLE).pack(anchor="w", pady=(8,2))

        self.log_box = tk.Text(left, height=10, bg=BG3, fg=WHITE,
                                font=("Courier", 8), relief="flat",
                                state="disabled", wrap="word")
        self.log_box.pack(fill="both", expand=True)
        self.log_box.tag_config("aira", foreground=NEON)
        self.log_box.tag_config("success", foreground="#44FF88")
        self.log_box.tag_config("error", foreground="#FF4444")
        self.log_box.tag_config("info", foreground=DIM)

        # Preview
        tk.Label(left, text="◈ BLOG PREVIEW",
                 font=("Courier", 9, "bold"),
                 bg=BG, fg=PURPLE).pack(anchor="w", pady=(8,2))

        self.preview = tk.Text(left, height=6, bg=BG3, fg="#AAAACC",
                                font=("Courier", 8), relief="flat",
                                state="disabled", wrap="word")
        self.preview.pack(fill="x")

        # Right — published blogs
        right = tk.Frame(main, bg=BG2, width=200)
        right.pack(side="right", fill="y", padx=(10,0))
        right.pack_propagate(False)

        tk.Label(right, text="◈ PUBLISHED",
                 font=("Courier", 9, "bold"),
                 bg=BG2, fg=PURPLE).pack(pady=(10,5), padx=10, anchor="w")

        self.blog_list = tk.Frame(right, bg=BG2)
        self.blog_list.pack(fill="both", expand=True, padx=5)

        # Share buttons
        share_f = tk.Frame(right, bg=BG2)
        share_f.pack(fill="x", padx=5, pady=8)
        tk.Label(share_f, text="SHARE LAST POST:",
                 font=("Courier", 7),
                 bg=BG2, fg=DIM).pack(anchor="w")

        platforms = [
            ("Facebook", "#1877F2"),
            ("X/Twitter", "#1DA1F2"),
            ("Instagram", "#E1306C"),
            ("WhatsApp", "#25D366"),
        ]
        for platform, color in platforms:
            tk.Button(share_f, text=platform,
                      font=("Courier", 8), bg=BG3, fg=color,
                      relief="flat", padx=5, pady=3,
                      command=lambda p=platform: self.share(p)
                      ).pack(fill="x", pady=1)

        tk.Frame(self.root, bg=PURPLE, height=2).pack(fill="x", side="bottom")

    def quick_set(self, cmd):
        self.cmd_input.delete(0, "end")
        self.cmd_input.insert(0, f"Create a blog about {cmd}")

    def log(self, msg, tag="aira"):
        self.log_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n", tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def execute(self):
        cmd = self.cmd_input.get().strip()
        if not cmd:
            return
        self.cmd_input.delete(0, "end")
        self.log(f"Brayo: {cmd}", "info")
        threading.Thread(target=self.process, args=(cmd,), daemon=True).start()

    def process(self, cmd):
        self.log("🧠 AIRA thinking...")
        try:
            if not GROQ_KEY:
                raise Exception("No GROQ_API_KEY in environment")

            r = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}",
                         "Content-Type": "application/json"},
                json={"model": "llama-3.3-70b-versatile",
                      "messages": [
                          {"role": "system", "content": AIRA_WEB_PROMPT},
                          {"role": "user", "content": cmd}
                      ],
                      "max_tokens": 2000},
                timeout=30
            )
            raw = r.json()["choices"][0]["message"]["content"].strip()

            # Parse JSON
            import re
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not json_match:
                raise Exception("AIRA returned invalid format")

            data = json.loads(json_match.group())
            self.root.after(0, self.build_and_publish, data)

        except Exception as e:
            self.root.after(0, self.log, f"⚠️ {e}", "error")
            self.root.after(0, self.use_local_template, cmd)

    def use_local_template(self, cmd):
        self.log("📝 Using local template...", "info")
        slug = cmd.lower().replace(" ", "-")[:30]
        data = {
            "title": cmd.title(),
            "slug": slug,
            "description": f"A post about {cmd} by Brayo",
            "content": f"""
                <h1>{cmd.title()}</h1>
                <p>Written by <strong>Brayo</strong> — BrayoOS Creator 🇰🇪</p>
                <p>Built using BrayoOS v3.5 with AIRA AI on a Redmi 14C.</p>
                <p>Two minds. One OS. Built Different.</p>
            """,
            "social_caption": f"🔥 New post: {cmd.title()} #BrayoOS #BuiltDifferent #Kenya #Tech"
        }
        self.build_and_publish(data)

    def build_and_publish(self, data):
        title = data.get("title", "BrayoOS Blog")
        slug = data.get("slug", "post")
        content = data.get("content", "")
        desc = data.get("description", "")
        caption = data.get("social_caption", "")

        self.log(f"🔨 Building: {title}")

        # Generate full HTML page
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — BrayoOS Blog</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#080810; color:#E0E0FF; font-family:'Courier New',monospace; }}
  header {{ background:#0D0D1A; border-bottom:2px solid #9D00FF; padding:20px 40px; }}
  header h1 {{ color:#CC44FF; font-size:1.4em; }}
  header p {{ color:#444466; font-size:0.8em; margin-top:4px; }}
  .badge {{ display:inline-block; background:#12122A; color:#9D00FF;
            border:1px solid #9D00FF; padding:2px 10px;
            font-size:0.75em; border-radius:3px; margin-top:8px; }}
  main {{ max-width:800px; margin:40px auto; padding:0 20px; }}
  main h1 {{ color:#CC44FF; font-size:2em; margin-bottom:16px; }}
  main h2 {{ color:#9D00FF; margin:24px 0 10px; }}
  main p {{ color:#AAAACC; line-height:1.8; margin-bottom:14px; }}
  main ul {{ color:#AAAACC; padding-left:20px; margin-bottom:14px; }}
  .caption {{ background:#12122A; border-left:3px solid #9D00FF;
              padding:12px 16px; margin:24px 0; color:#CC44FF;
              font-size:0.85em; }}
  footer {{ background:#0D0D1A; border-top:2px solid #9D00FF;
            text-align:center; padding:20px; margin-top:60px;
            color:#444466; font-size:0.8em; }}
  footer span {{ color:#9D00FF; }}
</style>
</head>
<body>
<header>
  <h1>◈ BrayoOS Blog</h1>
  <p>Built by Brayo & AIRA — Kenya 🇰🇪</p>
  <span class="badge">BrayoOS v3.5</span>
</header>
<main>
  <h1>{title}</h1>
  <p style="color:#444466;font-size:0.8em;">
    {datetime.now().strftime("%B %d, %Y")} — by Brayo
  </p>
  <br>
  {content}
  <div class="caption">{caption}</div>
</main>
<footer>
  <p>Built with ❤️ by <span>Brayo</span> &
     <span>AIRA</span> — BrayoOS 🇰🇪</p>
  <p style="margin-top:6px;">Two minds. One OS. Built Different.</p>
</footer>
</body>
</html>"""

        # Save file
        filename = f"{slug}.html"
        filepath = os.path.join(BLOGS_DIR, filename)
        with open(filepath, "w") as f:
            f.write(html)

        self.log(f"✅ Blog created: {filename}", "success")

        # Show preview
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("end", f"TITLE: {title}\n\n")
        self.preview.insert("end", f"DESC: {desc}\n\n")
        self.preview.insert("end", f"SHARE: {caption}\n\n")
        self.preview.insert("end", f"FILE: {filepath}")
        self.preview.config(state="disabled")

        # Push to GitHub Pages
        self.log("📡 Pushing to GitHub Pages...")
        self.push_to_github(filepath, filename, title, caption)

        # Update blog list
        self.root.after(0, self.add_blog_card, title, slug, caption)

    def push_to_github(self, filepath, filename, title, caption):
        try:
            # Copy to github pages folder
            pages_dir = os.path.expanduser(f"~/BrayoOS/")
            dest = os.path.join(pages_dir, filename)

            subprocess.run(f"cp '{filepath}' '{dest}'", shell=True)

            # Git push
            result = subprocess.run(
                f'cd ~/BrayoOS && git add {filename} && '
                f'git commit -m "AIRA Blog: {title}" && '
                f'git push origin main',
                shell=True, capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0:
                url = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}/{filename}"
                self.root.after(0, self.log,
                    f"🌐 LIVE: {url}", "success")
                self.root.after(0, self.log,
                    f"📱 Caption: {caption}", "info")
            else:
                self.root.after(0, self.log,
                    "⚠️ Push failed — check git config", "error")
                self.root.after(0, self.log,
                    f"💾 Saved locally: {filepath}", "info")

        except Exception as e:
            self.root.after(0, self.log,
                f"⚠️ GitHub error: {str(e)[:40]}", "error")

    def add_blog_card(self, title, slug, caption):
        card = tk.Frame(self.blog_list, bg=BG3, cursor="hand2")
        card.pack(fill="x", pady=3)
        tk.Label(card, text=f"◈ {title[:22]}",
                 font=("Courier", 7, "bold"),
                 bg=BG3, fg=NEON, wraplength=180,
                 justify="left").pack(anchor="w", padx=8, pady=(6,2))
        tk.Label(card, text=f"{slug}.html",
                 font=("Courier", 6),
                 bg=BG3, fg=DIM).pack(anchor="w", padx=8, pady=(0,6))
        self.blogs.append({"title": title, "slug": slug, "caption": caption})

    def share(self, platform):
        if not self.blogs:
            self.log("⚠️ No blogs published yet!", "error")
            return
        last = self.blogs[-1]
        url = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}/{last['slug']}.html"
        caption = last["caption"]

        share_texts = {
            "Facebook": f"{caption}\n\n🔗 {url}",
            "X/Twitter": f"{caption[:200]}\n{url}",
            "Instagram": f"{caption}\n\nLink in bio 🔗",
            "WhatsApp": f"*{last['title']}*\n\n{caption}\n\n{url}",
        }

        text = share_texts.get(platform, url)

        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        self.log(f"📋 {platform} caption copied!", "success")
        self.log(f"   {text[:80]}...", "info")
        messagebox.showinfo("Copied!",
            f"✅ {platform} caption copied!\n\nPaste it in {platform} now.")

if __name__ == "__main__":
    root = tk.Tk()
    AIRAWebAgent(root)
    root.mainloop()
