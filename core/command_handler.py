from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from ui.matrix import matrix_rain
from ui.dashboard import show_dashboard
from core.ai_engine import thinking
import os
import time
import datetime

console = Console()

history = []

def show_time():
    now = datetime.datetime.now()
    console.print(f"[green]{now}[/green]")

def package_manager():
    console.print("""
[bold cyan]BrayoOS Package Manager[/bold cyan]

ai-tools
network-utils
security-suite
matrix-engine
""")

def run():
    while True:

        cmd = Prompt.ask("\n[bold green]BrayoOS[/bold green]")
        history.append(cmd)

        if cmd == "help":
            console.print("""
[green]
help
status
matrix
linux
time
history
packages
hack
clear
exit
[/green]
""")

        elif cmd == "status":
            show_dashboard()

        elif cmd == "matrix":
            matrix_rain()

        elif cmd == "time":
            show_time()

        elif cmd == "history":
            table = Table(title="COMMAND HISTORY")
            table.add_column("Commands")

            for item in history:
                table.add_row(item)

            console.print(table)

        elif cmd == "packages":
            package_manager()

        elif cmd == "hack":
            thinking()
            console.print("[red]ACCESSING SECURE SYSTEM...[/red]")
            time.sleep(2)
            console.print("[green]ACCESS GRANTED[/green]")

        elif cmd == "linux":
            linux_cmd = Prompt.ask("[cyan]Linux Command[/cyan]")
            os.system(linux_cmd)

        elif cmd == "clear":
            os.system("clear")

        elif cmd == "exit":
            console.print("[bold red]SYSTEM SHUTDOWN[/bold red]")
            break

        else:
            console.print(f"[red]Unknown command:[/red] {cmd}")
