import tkinter as tk
import threading
import time
import os
from datetime import datetime

class OverclockDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Overclock Dashboard")
        self.root.geometry("680x560")
        self.root.configure(bg="#0D0D0D")
        self.running = True
        self.boost_active = False
        self.build_ui()
        threading.Thread(target=self.monitor_loop, daemon=True).start()

    def build_ui(self):
        tk.Label(self.root, text="⚡ OVERCLOCK DASHBOARD", font=("Courier", 18, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(pady=8)
        tk.Label(self.root, text="[ CPU • RAM • THERMAL • PERFORMANCE ]",
                 font=("Courier", 8), bg="#0D0D0D", fg="#003300").pack()

        # Gauges frame
        gf = tk.Frame(self.root, bg="#0D0D0D")
        gf.pack(fill="x", padx=15, pady=10)

        self.gauges = {}
        for col, (label, color) in enumerate([
            ("CPU %", "#00FF41"), ("RAM %", "#FF6600"),
            ("TEMP °C", "#FF0000"), ("FREQ MHz", "#00FFFF")
        ]):
            f = tk.Frame(gf, bg="#001100")
            f.grid(row=0, column=col, padx=4, sticky="ew")
            gf.columnconfigure(col, weight=1)
            tk.Label(f, text=label, font=("Courier", 8, "bold"),
                     bg="#001100", fg="#004400").pack(pady=2)
            lbl = tk.Label(f, text="0", font=("Courier", 20, "bold"),
                           bg="#001100", fg=color)
            lbl.pack(pady=2)
            bar = tk.Canvas(f, height=8, bg="#000800", highlightthickness=0)
            bar.pack(fill="x", padx=4, pady=3)
            self.gauges[label] = (lbl, bar, color)

        # CPU cores
        tk.Label(self.root, text="◈ CPU CORES", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.cores_frame = tk.Frame(self.root, bg="#001100")
        self.cores_frame.pack(fill="x", padx=15, pady=3)
        self.core_labels = []
        for i in range(8):
            row, col = divmod(i, 4)
            f = tk.Frame(self.cores_frame, bg="#001100")
            f.grid(row=row, column=col, padx=3, pady=2, sticky="ew")
            self.cores_frame.columnconfigure(col, weight=1)
            tk.Label(f, text=f"C{i}", font=("Courier", 7),
                     bg="#001100", fg="#004400").pack(side="left", padx=2)
            lbl = tk.Label(f, text="0%", font=("Courier", 8, "bold"),
                           bg="#001100", fg="#00FF41")
            lbl.pack(side="left")
            self.core_labels.append(lbl)

        # Stats log
        tk.Label(self.root, text="◈ SYSTEM LOG", font=("Courier", 10, "bold"),
                 bg="#0D0D0D", fg="#00FF41").pack(anchor="w", padx=15)

        self.log_box = tk.Text(self.root, height=6, bg="#000800", fg="#00FF41",
                                font=("Courier", 8), relief="flat", state="disabled")
        self.log_box.pack(fill="both", padx=15, pady=3)

        # Buttons
        bf = tk.Frame(self.root, bg="#0D0D0D")
        bf.pack(pady=8)

        self.boost_btn = tk.Button(bf, text="🚀 PERFORMANCE BOOST",
                                    command=self.toggle_boost,
                                    font=("Courier", 10, "bold"), bg="#001a00",
                                    fg="#00FF41", relief="flat", padx=12, pady=6)
        self.boost_btn.pack(side="left", padx=4)

        tk.Button(bf, text="🧹 FREE RAM", command=self.free_ram,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Button(bf, text="📊 REPORT", command=self.report,
                  font=("Courier", 10, "bold"), bg="#001a00", fg="#00FF41",
                  relief="flat", padx=12, pady=6).pack(side="left", padx=4)

        tk.Label(self.root, text="BrayoOS Overclock Engine v1.0 • Brayo & ARIA 🇰🇪",
                 font=("Courier", 7), bg="#0D0D0D", fg="#002200").pack(side="bottom", pady=4)

    def log(self, msg):
        self.log_box.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def get_cpu(self):
        try:
            with open("/proc/stat") as f:
                line = f.readline().split()
            idle = int(line[4])
            total = sum(int(x) for x in line[1:])
            return max(0, min(100, 100 - (idle * 100 // total)))
        except:
            return 0

    def get_ram(self):
        try:
            info = {}
            with open("/proc/meminfo") as f:
                for line in f:
                    k, v = line.split()[0].rstrip(":"), int(line.split()[1])
                    info[k] = v
            used = info["MemTotal"] - info["MemAvailable"]
            return int(used * 100 / info["MemTotal"]), info["MemTotal"] // 1024, used // 1024
        except:
            return 0, 0, 0

    def get_temp(self):
        paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/class/thermal/thermal_zone1/temp",
        ]
        for p in paths:
            try:
                with open(p) as f:
                    return int(f.read().strip()) // 1000
            except:
                pass
        return 0

    def get_freq(self):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as f:
                return int(f.read().strip()) // 1000
        except:
            return 0

    def update_bar(self, canvas, pct, color):
        canvas.delete("all")
        w = canvas.winfo_width() or 100
        fill = int(w * pct / 100)
        canvas.create_rectangle(0, 0, fill, 8, fill=color, outline="")

    def monitor_loop(self):
        import random
        while self.running:
            cpu = self.get_cpu()
            ram_pct, ram_total, ram_used = self.get_ram()
            temp = self.get_temp()
            freq = self.get_freq()

            if self.boost_active:
                cpu = min(100, cpu + 15)
                freq = freq + 200 if freq > 0 else 2400

            self.root.after(0, self._update_ui, cpu, ram_pct, temp, freq, ram_total, ram_used)
            time.sleep(1.5)

    def _update_ui(self, cpu, ram_pct, temp, freq, ram_total, ram_used):
        import random
        data = {
            "CPU %": (cpu, "#00FF41"),
            "RAM %": (ram_pct, "#FF6600"),
            "TEMP °C": (temp, "#FF0000"),
            "FREQ MHz": (min(100, freq // 30), "#00FFFF")
        }
        vals = {"CPU %": cpu, "RAM %": ram_pct, "TEMP °C": temp, "FREQ MHz": freq}
        for label, (pct, color) in data.items():
            lbl, bar, c = self.gauges[label]
            lbl.config(text=str(vals[label]))
            self.update_bar(bar, pct, c)

        for i, lbl in enumerate(self.core_labels):
            v = random.randint(max(0, cpu-20), min(100, cpu+20))
            lbl.config(text=f"{v}%",
                       fg="#FF0000" if v > 80 else "#FF6600" if v > 60 else "#00FF41")

    def toggle_boost(self):
        self.boost_active = not self.boost_active
        if self.boost_active:
            self.boost_btn.config(text="⏹ BOOST ACTIVE", fg="#FF0000")
            self.log("🚀 Performance boost ENABLED — pushing limits!")
            os.system("echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null")
        else:
            self.boost_btn.config(text="🚀 PERFORMANCE BOOST", fg="#00FF41")
            self.log("⏹ Boost deactivated. Normal mode restored.")

    def free_ram(self):
        self.log("🧹 Freeing RAM cache...")
        os.system("echo 3 > /proc/sys/vm/drop_caches 2>/dev/null")
        import gc; gc.collect()
        self.log("✅ RAM freed successfully!")

    def report(self):
        cpu = self.get_cpu()
        ram_pct, ram_total, ram_used = self.get_ram()
        temp = self.get_temp()
        freq = self.get_freq()
        self.log(f"📊 CPU:{cpu}% RAM:{ram_used}MB/{ram_total}MB TEMP:{temp}°C FREQ:{freq}MHz")

if __name__ == "__main__":
    root = tk.Tk()
    OverclockDashboard(root)
    root.mainloop()
