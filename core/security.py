from rich.console import Console
from rich.prompt import Prompt
import os

console = Console()

USER_FILE = "data/users/user.txt"

def login():
    if not os.path.exists(USER_FILE):

        console.print("[bold green]FIRST TIME SETUP[/bold green]")

        username = Prompt.ask("Create username")
        password = Prompt.ask("Create password", password=True)

        with open(USER_FILE, "w") as f:
            f.write(f"{username}:{password}")

        console.print("[green]User created successfully.[/green]")

    else:
        with open(USER_FILE, "r") as f:
            data = f.read().split(":")
            saved_user = data[0]
            saved_pass = data[1]

        console.print("[bold cyan]LOGIN REQUIRED[/bold cyan]")

        username = Prompt.ask("Username")
        password = Prompt.ask("Password", password=True)

        if username == saved_user and password == saved_pass:
            console.print("[green]ACCESS GRANTED[/green]")
        else:
            console.print("[bold red]ACCESS DENIED[/bold red]")
            exit()
