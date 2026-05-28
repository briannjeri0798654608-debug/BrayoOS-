from rich.console import Console
import os

console = Console()

PLUGIN_DIR = "plugins"

def load_plugins():
    plugins = []

    for file in os.listdir(PLUGIN_DIR):
        if file.endswith(".py") and file != "plugin_loader.py":
            plugins.append(file)

    console.print(f"[green]{len(plugins)} plugins loaded.[/green]")
