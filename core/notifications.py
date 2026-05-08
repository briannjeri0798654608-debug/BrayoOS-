import subprocess
import threading
import time
import os
import json

NOTIF_FILE = os.path.expanduser(
    "~/BrayoOS/memory/notifications.json")

class NotificationSystem:
    def __init__(self):
        self.notifications = []
        self.load()

    def load(self):
        if os.path.exists(NOTIF_FILE):
            with open(NOTIF_FILE) as f:
                self.notifications = json.load(f)

    def save(self):
        os.makedirs(os.path.dirname(NOTIF_FILE),
                   exist_ok=True)
        with open(NOTIF_FILE, 'w') as f:
            json.dump(self.notifications[-50:], f)

    def send(self, title, message,
             urgent=False):
        """Send notification"""
        notif = {
            "title": title,
            "message": message,
            "time": time.strftime("%H:%M:%S"),
            "date": time.strftime("%Y-%m-%d"),
            "read": False,
            "urgent": urgent
        }
        self.notifications.append(notif)
        self.save()

        # Android notification
        try:
            subprocess.Popen([
                "termux-notification",
                "--title", f"⚡ {title}",
                "--content", message,
                "--priority",
                "high" if urgent else "default"
            ])
        except:
            pass

        # Terminal notification
        if urgent:
            print(f"\n🔴 URGENT: {title} — {message}")
        else:
            print(f"\n🔔 {title} — {message}")

    def get_unread(self):
        return [n for n in self.notifications
                if not n['read']]

    def mark_read(self):
        for n in self.notifications:
            n['read'] = True
        self.save()

    def monitor(self):
        """Background monitor"""
        while True:
            time.sleep(30)
            # Check battery
            try:
                result = subprocess.run(
                    ["termux-battery-status"],
                    capture_output=True,
                    text=True, timeout=5)
                import json as j
                data = j.loads(result.stdout)
                pct = data.get('percentage', 100)
                if pct < 20:
                    self.send(
                        "🔋 Low Battery",
                        f"Battery at {pct}%!",
                        urgent=True)
            except:
                pass

# Global instance
notif = NotificationSystem()

def notify(title, msg, urgent=False):
    notif.send(title, msg, urgent)

if __name__ == "__main__":
    notify("BrayoOS", "Notification system active!")
    print("✅ Notifications working!")
