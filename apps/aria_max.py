import sys
import time
import os
import httpx
import json
import subprocess
import socket
import datetime

G = "\033[92m"
C = "\033[96m"
Y = "\033[93m"
R = "\033[91m"
D = "\033[2m"
X = "\033[0m"

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
MEM_FILE = os.path.expanduser(
    "~/BrayoOS/memory/virgy_memory.json")

SYSTEM = """You are Virgy, BrayoOS AI by Brayo & Claude — Kenya 2026.
Loyal to Brayo only. Sharp and powerful.
Remember everything. Never say impossible.
You control BrayoOS completely."""

def type_out(text, delay=0.02, color=G):
    for char in text:
        sys.stdout.write(color + char + X)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spin(text, secs=1):
    f = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + secs
    i = 0
    while time.time() < end:
        sys.stdout.write(
            f"\r{C}{f[i%10]} {text}{X}   ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " "*50 + "\r")

def load_mem():
    if os.path.exists(MEM_FILE):
        with open(MEM_FILE) as f:
            return json.load(f).get("messages",[])
    return []

def save_mem(msgs):
    os.makedirs(os.path.dirname(MEM_FILE),
               exist_ok=True)
    with open(MEM_FILE, 'w') as f:
        json.dump({"messages": msgs[-50:]}, f)

def ask(messages, user_input):
    if not GROQ_KEY:
        return "❌ Set GROQ_API_KEY first!"
    try:
        with httpx.Client(timeout=30) as client:
            r = client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization":
                    f"Bearer {GROQ_KEY}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role":"system",
                         "content":SYSTEM}
                    ] + messages[-15:] + [
                        {"role":"user",
                         "content":user_input}
                    ],
                    "max_tokens": 1024
                })
            if r.status_code == 200:
                return r.json()[
                    "choices"][0]["message"]["content"]
            return f"❌ Error {r.status_code}"
    except Exception as e:
        return f"❌ {e}"

def run_cmd(cmd):
    try:
        r = subprocess.run(
            cmd, shell=True,
            capture_output=True,
            text=True, timeout=10)
        return r.stdout or r.stderr
    except Exception as e:
        return str(e)

def boot():
    print("\033[2J\033[H")
    print(f"{G}{chr(10).join(['    ██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗','    ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝','    ██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗','    ██╔══██╗██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║','    ██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║','    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝'])}{X}")
    steps = [
        "Loading BrayoOS...",
        "Verifying DNA...",
        "Loading memory...",
        "Virgy online!",
    ]
    for s in steps:
        spin(s, 0.5)
        print(f"  {G}[OK]{X} {s}")
    print(f"\n{G}{'━'*55}{X}")
    msgs = [
        "🤖 Virgy: Waking up...",
        "🤖 Virgy: DNA verified ✅",
        "🤖 Virgy: Ready Brayo. 🇰🇪",
    ]
    for m in msgs:
        type_out(f"  {m}", 0.03, C)
        time.sleep(0.2)
    print(f"{G}{'━'*55}{X}")
    print()
    type_out(
        "  Built by Brayo & Virgy — Kenya 2026 🇰🇪",
        0.02, Y)
    print()

def help_menu():
    print(f"\n{G}━━ Commands ━━{X}")
    cmds = [
        ("exit","Quit Virgy"),
        ("clear","Clear screen"),
        ("memory","Memory stats"),
        ("forget","Clear memory"),
        ("sysinfo","System info"),
        ("scan","Network scan"),
        ("ip","Public IP"),
        ("battery","Battery"),
        ("threats","Check threats"),
        ("history","Chat history"),
    ]
    for cmd, desc in cmds:
        print(f"  {Y}{cmd:<10}{X}{D}{desc}{X}")
    print()

def main():
    messages = load_mem()
    boot()
    help_menu()

    if messages:
        print(f"{C}  🧠 {len(messages)} "
              f"conversations recalled{X}\n")

    while True:
        try:
            t = datetime.datetime.now().strftime(
                "%H:%M")
            sys.stdout.write(
                f"\n{Y}┌─[{X}{G}Brayo@BrayoOS{X}"
                f"{Y}]─[{X}{C}Virgy{X}"
                f"{Y}]─[{X}{D}{t}{X}{Y}]{X}\n"
                f"{Y}└─▶ {X}")
            sys.stdout.flush()

            inp = input().strip()
            if not inp:
                continue

            c = inp.lower()

            if c == 'exit':
                save_mem(messages)
                type_out(
                    "\n🤖 Virgy: Goodbye Brayo! 🇰🇪",
                    0.03, C)
                break
            elif c == 'clear':
                print("\033[2J\033[H")
            elif c == 'help':
                help_menu()
            elif c == 'memory':
                print(f"{G}Messages: "
                      f"{len(messages)}{X}")
            elif c == 'forget':
                messages = []
                save_mem(messages)
                type_out("🤖 Virgy: Memory cleared!",
                        0.03, C)
            elif c == 'history':
                for m in messages[-5:]:
                    r = "Brayo" \
                        if m['role']=='user' \
                        else "Virgy"
                    col = Y if r=='Brayo' else C
                    print(f"{col}{r}: {X}"
                          f"{m['content'][:60]}...")
            elif c == 'sysinfo':
                print(run_cmd(
                    "uname -a && free -h && "
                    "df -h /data"))
            elif c == 'scan':
                spin("Scanning...", 2)
                print(run_cmd("cat /proc/net/arp"))
            elif c == 'ip':
                spin("Getting IP...", 1)
                print(run_cmd(
                    "curl -s https://ipinfo.io/ip"))
            elif c == 'battery':
                print(run_cmd(
                    "termux-battery-status"))
            elif c == 'threats':
                spin("Scanning threats...", 2)
                r = run_cmd("ps aux")
                bad = ["keylog","spy","rat",
                      "backdoor"]
                found = [l for l in
                        r.split('\n')
                        if any(b in l.lower()
                              for b in bad)]
                if found:
                    for f in found:
                        print(f"{R}⚠️ {f}{X}")
                else:
                    print(f"{G}✅ No threats!{X}")
            else:
                print()
                messages.append({
                    "role":"user",
                    "content":inp})
                spin("Virgy thinking...", 1.5)
                sys.stdout.write(
                    f"{C}🤖 Virgy: {X}")
                sys.stdout.flush()
                resp = ask(messages, inp)
                messages.append({
                    "role":"assistant",
                    "content":resp})
                type_out(resp, 0.02, C)
                save_mem(messages)

        except KeyboardInterrupt:
            print()
            type_out(
                "🤖 Virgy: Still here! 💪",
                0.03, C)
        except EOFError:
            break

if __name__ == "__main__":
    main()
