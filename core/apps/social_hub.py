import tkinter as tk
import threading,httpx,os,json,subprocess,time
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"
GROQ=os.environ.get("GROQ_API_KEY","")

PLATFORMS={
    "Twitter":{"color":"#1DA1F2","icon":"🐦","url":"https://twitter.com"},
    "Facebook":{"color":"#1877F2","icon":"📘","url":"https://facebook.com"},
    "Instagram":{"color":"#E1306C","icon":"📸","url":"https://instagram.com"},
    "WhatsApp":{"color":"#25D366","icon":"💬","url":"https://wa.me"},
    "Telegram":{"color":"#0088cc","icon":"✈️","url":"https://t.me"},
    "GitHub":{"color":"#FFFFFF","icon":"💻","url":"https://github.com"},
    "TikTok":{"color":"#FF0050","icon":"🎵","url":"https://tiktok.com"},
    "LinkedIn":{"color":"#0A66C2","icon":"💼","url":"https://linkedin.com"},
}

POSTS_FILE=os.path.expanduser("~/BrayoOS/memory/social_posts.json")
os.makedirs(os.path.dirname(POSTS_FILE),exist_ok=True)

class SocialHub:
    def __init__(self,root):
        self.root=root
        self.root.title("📱 Social Hub")
        self.root.geometry("700x580")
        self.root.configure(bg=BG)
        self.posts=self.load_posts()
        self.platform_vars={}
        self.build_ui()

    def load_posts(self):
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE) as f:return json.load(f)
        return []

    def save_posts(self):
        with open(POSTS_FILE,"w") as f:json.dump(self.posts[-50:],f,indent=2)
