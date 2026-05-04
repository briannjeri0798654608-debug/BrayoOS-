import httpx
import os
import asyncio
import json

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
offset = 0

def ask_groq(prompt):
    with httpx.Client() as client:
        r = client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024
            },
            timeout=30
        )
        return r.json()["choices"][0]["message"]["content"]

def send_message(chat_id, text):
    with httpx.Client() as client:
        client.post(f"{API}/sendMessage",
                   json={"chat_id": chat_id, "text": text})

def get_updates():
    global offset
    with httpx.Client() as client:
        r = client.get(f"{API}/getUpdates",
                      params={"offset": offset, "timeout": 30},
                      timeout=35)
        return r.json().get("result", [])

def run():
    global offset
    print("🤖 BrayoOS Telegram Bot Running...")
    while True:
        try:
            updates = get_updates()
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")
                if text and chat_id:
                    print(f"Message: {text}")
                    if text == "/start":
                        send_message(chat_id, "⚡ BrayoOS Bot Active!\nSend any message to chat with AI.")
                    elif text == "/ip":
                        import socket
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(("8.8.8.8", 80))
                        ip = s.getsockname()[0]
                        send_message(chat_id, f"📍 IP: {ip}")
                    else:
                        reply = ask_groq(text)
                        send_message(chat_id, f"🤖 {reply}")
        except Exception as e:
            print(f"Error: {e}")
            import time
            time.sleep(5)

if __name__ == "__main__":
    run()
