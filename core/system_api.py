import os
import subprocess

BASE = os.path.expanduser("~/BrayoOS")
APPS_DIR = os.path.join(BASE, "core", "apps")


def list_apps():
    apps = []

    if not os.path.exists(APPS_DIR):
        return apps

    for file in sorted(os.listdir(APPS_DIR)):
        if file.endswith(".py"):
            apps.append(file)

    return apps


def launch_app(app_name):
    path = os.path.join(APPS_DIR, app_name)

    if not os.path.exists(path):
        return False, f"{app_name} not found"

    try:
        env = os.environ.copy()
        env["DISPLAY"] = ":1"

        subprocess.Popen(
            ["python3", path],
            env=env
        )

        return True, f"Launched {app_name}"

    except Exception as e:
        return False, str(e)


def app_exists(app_name):
    return os.path.exists(
        os.path.join(APPS_DIR, app_name)
    )
