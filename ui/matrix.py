from rich.console import Console
import random
import time

console = Console()

def matrix_rain():

    chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for _ in range(20):

        line = "".join(
            random.choice(chars) for _ in range(70)
        )

        console.print(f"[green]{line}[/green]")

        time.sleep(0.03)
