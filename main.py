from ui.startup import startup_animation
from core.boot import boot
from ui.dashboard import show_banner, show_dashboard
from core.command_handler import run
from core.security import login
from plugins.plugin_loader import load_plugins

startup_animation()
boot()
login()
load_plugins()

show_banner()
show_dashboard()

run()
