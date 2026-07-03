import tkinter as tk
import threading, json, os, time
try:
    import httpx
except:
    httpx = None

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";GREEN="#44FF88"
CYAN="#44FFFF";RED="#FF0044";AMBER="#FFB300"
WHITE="#E0E0FF";DIM="#444466"

class PhoneTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("☎ Phone Tracker — BrayoOS")
        self.root.geometry("700x520")
        self.root.configure(bg=BG)
        self._build()
        self.root.mainloop()

    def _build(self):
        # Header
        hdr = tk.Frame(self.root, bg=RED, height=3)
        hdr.pack(fill="x")
        tk.Label(self.root, text="☎ PHONE NUMBER TRACKER",
                font=("Courier",14,"bold"), bg=BG, fg=RED).pack(pady=(12,2))
        tk.Label(self.root, text="Carrier · Region · Timezone · Line Type",
                font=("Courier",8), bg=BG, fg=DIM).pack()
        tk.Frame(self.root, bg=PURPLE, height=1).pack(fill="x", pady=8)

        # Input
        inf = tk.Frame(self.root, bg=BG)
        inf.pack(fill="x", padx=20, pady=4)
        tk.Label(inf, text="NUMBER:", font=("Courier",10,"bold"),
                bg=BG, fg=NEON, width=10).pack(side="left")
        self.num_var = tk.StringVar()
        self.entry = tk.Entry(inf, textvariable=self.num_var,
                font=("Courier",12), bg=BG3, fg=GREEN,
                insertbackground=NEON, relief="flat", width=25)
        self.entry.pack(side="left", ipady=6, ipadx=8)
        tk.Label(inf, text="e.g. +254712345678",
                font=("Courier",7), bg=BG, fg=DIM).pack(side="left", padx=8)
        self.entry.bind("<Return>", lambda e: self._track())

        tk.Button(self.root, text="⚡ TRACK NUMBER",
                font=("Courier",10,"bold"), bg=RED, fg=WHITE,
                relief="flat", padx=20, pady=8,
                command=self._track).pack(pady=8)

        tk.Frame(self.root, bg=PURPLE, height=1).pack(fill="x", padx=20)

        # Results area
        self.res_frame = tk.Frame(self.root, bg=BG2)
        self.res_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.status = tk.Label(self.root, text="Enter a number and press TRACK",
                font=("Courier",8), bg=BG, fg=DIM)
        self.status.pack(pady=4)

        self._show_placeholder()

    def _show_placeholder(self):
        for w in self.res_frame.winfo_children(): w.destroy()
        tk.Label(self.res_frame, text="☎",
                font=("Courier",40), bg=BG2, fg=PURPLE).pack(expand=True)
        tk.Label(self.res_frame, text="Results will appear here",
                font=("Courier",9), bg=BG2, fg=DIM).pack(pady=4)

    def _track(self):
        num = self.num_var.get().strip().replace(" ","").replace("-","")
        if not num:
            self.status.config(text="⚠ Enter a phone number first", fg=AMBER)
            return
        if not num.startswith("+"): num = "+" + num
        self.status.config(text="⟳ Tracking...", fg=CYAN)
        for w in self.res_frame.winfo_children(): w.destroy()
        tk.Label(self.res_frame, text="⟳ Querying databases...",
                font=("Courier",10), bg=BG2, fg=CYAN).pack(expand=True)
        threading.Thread(target=self._do_track, args=(num,), daemon=True).start()

    def _do_track(self, num):
        results = {}
        try:
            if httpx:
                r = httpx.get(f"https://phonevalidation.abstractapi.com/v1/?api_key=trial&phone={num}", timeout=6)
                if r.status_code == 200:
                    d = r.json()
                    results["valid"] = str(d.get("valid", "Unknown"))
                    results["number"] = d.get("phone", num)
                    results["country"] = d.get("country", {}).get("name", "Unknown")
                    results["country_code"] = d.get("country", {}).get("code", "??")
                    results["carrier"] = d.get("carrier", "Unknown")
                    results["line_type"] = d.get("type", "Unknown")
                    results["region"] = d.get("location", "Unknown")
        except: pass

        # Fallback: parse locally
        if not results:
            results = self._local_parse(num)

        self.root.after(0, self._show_results, num, results)

    def _local_parse(self, num):
        # Basic country code lookup
        codes = {
            "+254":"Kenya 🇰🇪","+1":"USA/Canada 🇺🇸","+44":"UK 🇬🇧",
            "+91":"India 🇮🇳","+27":"South Africa 🇿🇦","+234":"Nigeria 🇳🇬",
            "+255":"Tanzania 🇹🇿","+256":"Uganda 🇺🇬","+251":"Ethiopia 🇪🇹",
            "+49":"Germany 🇩🇪","+33":"France 🇫🇷","+86":"China 🇨🇳",
            "+7":"Russia 🇷🇺","+55":"Brazil 🇧🇷","+61":"Australia 🇦🇺",
        }
        country = "Unknown"
        for code, name in sorted(codes.items(), key=lambda x: -len(x[0])):
            if num.startswith(code):
                country = name
                break

        ke_carriers = {
            "70":"Safaricom","71":"Safaricom","72":"Safaricom",
            "74":"Airtel","75":"Airtel","76":"Airtel",
            "77":"Airtel","78":"Airtel",
            "79":"Telkom","73":"Faiba",
        }
        carrier = "Unknown"
        if num.startswith("+254") and len(num) >= 6:
            prefix = num[4:6]
            carrier = ke_carriers.get(prefix, "Unknown Kenyan Carrier")

        return {
            "number": num,
            "country": country,
            "carrier": carrier,
            "line_type": "Mobile (estimated)",
            "region": "Parsed locally",
            "valid": "Format OK",
        }

    def _show_results(self, num, data):
        for w in self.res_frame.winfo_children(): w.destroy()

        fields = [
            ("📱 NUMBER", data.get("number", num), GREEN),
            ("🌍 COUNTRY", data.get("country","Unknown"), CYAN),
            ("📡 CARRIER", data.get("carrier","Unknown"), NEON),
            ("📶 LINE TYPE", data.get("line_type","Unknown"), AMBER),
            ("📍 REGION", data.get("region","Unknown"), PURPLE),
            ("✓  VALID", data.get("valid","Unknown"), GREEN),
        ]

        for label, value, color in fields:
            row = tk.Frame(self.res_frame, bg=BG3)
            row.pack(fill="x", padx=8, pady=3)
            tk.Frame(row, bg=color, width=3).pack(side="left", fill="y")
            tk.Label(row, text=f"  {label}",
                    font=("Courier",8,"bold"), bg=BG3, fg=color,
                    width=16, anchor="w").pack(side="left", pady=8)
            tk.Label(row, text=value,
                    font=("Courier",10), bg=BG3, fg=WHITE).pack(side="left", padx=8)

        self.status.config(text="✓ Track complete", fg=GREEN)

if __name__ == "__main__":
    PhoneTracker()
