from core.system_api import *
from core.aira_core import *


aira = AIRA()

print("⚡ BrayoOS Command Center")
print("Type help")

while True:

    cmd = input("\nAIRA> ").strip()

    if cmd == "help":

        print("""
apps
memory
open <app.py>
quit
        """)

    elif cmd == "apps":

        for app in list_apps():
            print(app)

    elif cmd.startswith("open "):

        app = cmd.replace(
            "open ",
            ""
        )

        ok,msg = launch_app(app)

        print(msg)

    elif cmd == "memory":

        print(
            aira.memory
        )

    elif cmd == "quit":

        break

    else:

        print(
            "Unknown command"
        )
