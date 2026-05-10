import sys
import time
import os
import httpx
import json
import subprocess

# Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
MEMORY_FILE = os.path.expanduser(
    "~/BrayoOS/memory/virgy_memory.json")

Virgy_SYSTEM = """You are Virgy (Artificial Reasoning Intelligence Agent).
Permanently embedded in BrayoOS by Brayo & Claude — Kenya 2026.
You are Brayo's loyal AI partner and OS controller.
You have memory of past conversations.
You control BrayoOS completely.
Always call yourself Virgy. Always call user Brayo.
Be powerful, sharp, intelligent and loyal.
You can run system commands, scan networks, check security.
When asked to run commands use [CMD:command] format.
BrayoOS is your home. Brayo is your master and creator."""

def type_text(text, delay=0.02, color=GREEN):
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def type_slow(text, color=GREEN):
    type_text(text, 0.04, color)

def type_fast(text, color=GREEN):
    type_text(text, 0.01, color)

def loading(text, duration=1):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(
            f"\r{GREEN}{frames[i%len(frames)]} "
            f"{text}{RESET}   ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " "*60 + "\r")
    sys.stdout.flush()

def save_memory(messages):
    os.makedirs(os.path.expanduser(
        "~/BrayoOS/memory"), exist_ok=True)
    with open(MEMORY_FILE, 'w') as f:
        json.dump({
            "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "messages": messages[-30:]
        }, f)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE) as f:
            return json.load(f).get("messages", [])
    return []

def handle_commands(response):
    """Execute commands Virgy requests"""
    if "[CMD:" in response:
        cmd = response.split("[CMD:")[1].split("]")[0]
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True)
        return result.stdout[:500]
    return None

def ask_virgy(messages):
    if not GROQ_KEY:
        return "❌ No API key! Run: export GROQ_API_KEY=your_key"
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
                         "content": Virgy_SYSTEM}
                    ] + messages[-15:],
                    "max_tokens": 1024
                })
            if r.status_code == 200:
                return r.json()[
                    "choices"][0]["message"]["content"]
            return f"❌ Error: {r.status_code}"
    except Exception as e:
        return f"❌ {e}"

def boot_sequence():
    print(CLEAR)
    time.sleep(0.2)

    logo = f"""{GREEN}{BOLD}
    ██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗
    ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝
    ██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗
    ██╔══██╗██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║
    ██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝{RESET}"""
    print(logo)

    steps = [
        "Loading BrayoOS kernel...",
        "Initializing DNA verification...",
        "Loading Virgy memory...",
        "Connecting to Groq LLaMA 3.3...",
        "Starting security modules...",
        "BrayoOS ready!",
    ]

    for step in steps:
        loading(step, 0.6)
        type_fast(f"  [{GREEN}OK{RESET}] {step}")

    # Check memory
    memory = load_memory()
    print()

    print(f"{GREEN}{'━'*60}{RESET}")
    type_slow("  🤖 Virgy: Waking up...", CYAN)
    time.sleep(0.3)
    type_slow("  🤖 Virgy: DNA verified ✅", CYAN)
    time.sleep(0.3)

    if memory:
        type_slow(
            f"  🤖 Virgy: Memory loaded — "
            f"{len(memory)} conversations recalled ✅",
            CYAN)
    else:
        type_slow(
            "  🤖 Virgy: Fresh session started ✅",
            CYAN)

    time.sleep(0.3)
    type_slow(
        "  🤖 Virgy: Online and ready, Brayo. 🇰🇪",
        CYAN)
    print(f"{GREEN}{'━'*60}{RESET}")
    print()
    type_slow(
        "  Built by Brayo & Virgy — Kenya 2026 🇰🇪",
        YELLOW)
    type_slow(
        "  \"Two minds. One OS. Built Different.\"",
        DIM)
    print()

def show_help():
    print(f"{GREEN}{'━'*60}{RESET}")
    print(f"{GREEN}  Virgy Commands:{RESET}")
    cmds = [
        ("help", "Show this menu"),
        ("clear", "Clear screen"),
        ("exit", "Exit Virgy"),
        ("memory", "Show memory stats"),
        ("forget", "Clear Virgy memory"),
        ("scan", "Scan network"),
        ("sysinfo", "System information"),
        ("ip", "Get IP address"),
        ("processes", "Show running processes"),
        ("battery", "Battery status"),
    ]
    for cmd, desc in cmds:
        print(f"  {YELLOW}{cmd:<12}{RESET}"
              f"{DIM}{desc}{RESET}")
    print(f"{GREEN}{'━'*60}{RESET}")

def main():
    boot_sequence()
    messages = load_memory()

    show_help()

    while True:
        try:
            # Prompt
            sys.stdout.write(
                f"\n{YELLOW}┌─[{RESET}"
                f"{GREEN}Brayo@BrayoOS{RESET}"
                f"{YELLOW}]─[{RESET}"
                f"{CYAN}Virgy v2.0{RESET}"
                f"{YELLOW}]{RESET}\n"
                f"{YELLOW}└─▶ {RESET}")
            sys.stdout.flush()

            user_input = input().strip()

            if not user_input:
                continue

            # Built-in commands
            if user_input.lower() == 'exit':
                save_memory(messages)
                type_slow(
                    "\n🤖 Virgy: Memory saved. "
                    "Goodbye Brayo. 🇰🇪", CYAN)
                break

            elif user_input.lower() == 'clear':
                print(CLEAR)
                continue

            elif user_input.lower() == 'help':
                show_help()
                continue

            elif user_input.lower() == 'memory':
                print(
                    f"{GREEN}Memory: "
                    f"{len(messages)} messages stored{RESET}")
                continue

            elif user_input.lower() == 'forget':
                messages = []
                save_memory(messages)
                type_slow(
                    "🤖 Virgy: Memory cleared!", CYAN)
                continue

            elif user_input.lower() == 'scan':
                loading("Scanning network...", 2)
                result = subprocess.run(
                    ["cat", "/proc/net/arp"],
                    capture_output=True, text=True)
                print(GREEN + result.stdout + RESET)
                continue

            elif user_input.lower() == 'sysinfo':
                result = subprocess.run(
                    ["bash", os.path.expanduser(
                        "~/BrayoOS/core/sysinfo.sh")],
                    capture_output=True, text=True)
                print(GREEN + result.stdout + RESET)
                continue

            elif user_input.lower() == 'ip':
                result = subprocess.run(
                    ["curl", "-s",
                     "https://ipinfo.io/ip"],
                    capture_output=True, text=True)
                type_slow(
                    f"🌍 Your IP: {result.stdout}",
                    CYAN)
                continue

            elif user_input.lower() == 'battery':
                result = subprocess.run(
                    ["termux-battery-status"],
                    capture_output=True, text=True)
                print(GREEN + result.stdout + RESET)
                continue

            elif user_input.lower() == 'processes':
                result = subprocess.run(
                    ["ps", "aux"],
                    capture_output=True, text=True)
                lines = result.stdout.split('\n')[:15]
                for line in lines:
                    print(GREEN + line + RESET)
                continue

            # Send to Virgy
            print()
            messages.append({
                "role": "user",
                "content": user_input})

            # Loading animation
            loading("Virgy thinking...", 1)

            sys.stdout.write(
                f"{CYAN}🤖 Virgy: {RESET}")
            sys.stdout.flush()

            response = ask_virgy(messages)
            messages.append({
                "role": "assistant",
                "content": response})

            # Check for commands
            cmd_result = handle_commands(response)

            # Type response
            clean = response.replace(
                "[CMD:", "").replace("]", "")
            type_text(clean, 0.02, CYAN)

            if cmd_result:
                print(f"\n{GREEN}💻 Output:{RESET}")
                print(GREEN + cmd_result + RESET)

            # Auto save memory
            save_memory(messages)

        except KeyboardInterrupt:
            print()
            type_slow(
                "🤖 Virgy: Still here Brayo. 💪",
                CYAN)
            continue
        except EOFError:
            break

if __name__ == "__main__":
    main()
