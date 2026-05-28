from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_banner():
    console.print(
        Panel.fit(
            "[bold green]BRAYOOS AI CORE[/bold green]\n[white]CYBER OPERATING ENVIRONMENT[/white]",
            border_style="green"
        )
    )

def show_dashboard():

    table = Table(title="SYSTEM STATUS")

    table.add_column("Component", style="cyan")
    table.add_column("State", style="green")

    table.add_row("AI Core", "ONLINE")
    table.add_row("Security", "ACTIVE")
    table.add_row("Plugins", "LOADED")
    table.add_row("Terminal", "READY")

    console.print(table)
