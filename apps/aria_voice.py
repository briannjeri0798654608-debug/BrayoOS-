import os
import subprocess
import httpx
import json
import time
import sys

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

def speak(text):
    """Text to speech"""
    try:
        subprocess.Popen(
            ["termux-tts-speak", text])
    except:
        pass

def listen():
    """Voice input via termux"""
    try:
        result = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True,
            text=True, timeout=10)
        return result.stdout.strip()
    except:
        return None

def ask_aira(text):
    if not GROQ_KEY:
        return "API key not set"
    try:
        with httpx.Client(timeout=30) as client:
            r = client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_KEY}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system",
                         "content": "You are AIRA, BrayoOS AI by Brayo. Be brief and sharp."},
                        {"role": "user",
                         "content": text}
                    ],
                    "max_tokens": 200
                })
            return r.json()[
                "choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def main():
    print(f"{GREEN}🎤 AIRA Voice Mode{RESET}")
    print(f"{CYAN}Built by Brayo & AIRA — Kenya 2026{RESET}")
    print(f"{YELLOW}Say something or type 'exit'{RESET}\n")

    speak("AIRA voice mode activated. Ready Brayo.")

    while True:
        print(f"{YELLOW}🎤 Listening...{RESET}")
        voice = listen()

        if voice:
            print(f"{GREEN}You said: {voice}{RESET}")
            if 'exit' in voice.lower():
                speak("Goodbye Brayo")
                break
            response = ask_aira(voice)
            print(f"{CYAN}🤖 AIRA: {response}{RESET}")
            speak(response)
        else:
            # Fall back to text
            sys.stdout.write(
                f"{YELLOW}Type: {RESET}")
            text = input().strip()
            if text == 'exit':
                break
            if text:
                response = ask_aira(text)
                print(f"{CYAN}🤖 AIRA: {response}{RESET}")
                speak(response)

if __name__ == "__main__":
    main()
