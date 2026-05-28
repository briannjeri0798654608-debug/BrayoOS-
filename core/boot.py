from rich.console import Console
from rich.progress import track
import time
import os

console = Console()

def boot():
    os.system("clear")

    boot_steps = [
        "Initializing kernel...",
        "Loading AI engine...",
        "Loading plugins...",
        "Securing environment...",
        "Connecting systems...",
        "Launching BrayoOS..."
    ]

    console.print("[bold green]BRAYOOS INITIALIZATION[/bold green]\n")

    for step in track(boot_steps, description="Booting"):
        time.sleep(1)

    os.system("clear")
