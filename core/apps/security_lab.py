import tkinter as tk
import subprocess
import os

BG = "#080810"
FG = "#44FF88"

TOOLS = [
    "network_scanner.py",
    "osint_suite.py",
    "wifi_auditor.py",
    "firewall.py",
    "vpn_engine.py",
    "hack_terminal.py",
    "file_encryptor.py",
    "live_threat_map.py",
    "wifi_passwords.py"
]

BASE = os.path.expanduser("~/BrayoOS/core/apps")

root = tk.Tk()
root.title("🔐 Security Lab")
root.geometry("600x500")
root.configure(bg=BG)

tk.Label(
    root,
    text="🔐 BRAYOOS SECURITY LAB",
    bg=BG,
    fg=FG,
    font=("Courier",16,"bold")
).pack(pady=10)

def launch(app):
    path = os.path.join(BASE, app)

    env = os.environ.copy()
    env["DISPLAY"] = ":1"

    subprocess.Popen(
        ["python3", path],
        env=env
    )

for app in TOOLS:

    tk.Button(
        root,
        text=app.replace(".py",""),
        command=lambda a=app: launch(a),
        bg="#101020",
        fg=FG,
        font=("Courier",10)
    ).pack(fill="x", padx=20, pady=3)

root.mainloop()
