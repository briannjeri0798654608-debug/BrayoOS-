import tkinter as tk
import threading,subprocess,os,time,json
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

COMMANDS={
    "open ghost":("ghost_mode.py","Opening Ghost Mode"),
    "open vault":("dna_vault.py","Opening DNA Vault"),
    "open threat":("live_threat_map.py","Opening Threat Map"),
    "open dark web":("dark_web_monitor.py","Opening Dark Web Monitor"),
    "open osint":("osint_suite.py","Opening OSINT Suite"),
    "open scanner":("network_scanner.py","Opening Network Scanner"),
    "open monitor":("system_monitor.py","Opening System Monitor"),
    "open aira":("aria_voice.py","Opening AIRA"),
    "open settings":("settings.py","Opening Settings"),
    "open wallpaper":("wallpaper_changer.py","Opening Wallpaper Changer"),
}

class VoiceCommands:
    def __init__(self,root):
        self.root=root
        self.root.title("🎙️ Voice Commands")
        self.root.geometry("600x520")
        self.root.configure(bg=BG)
        self.listening=False
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="🎙️ VOICE COMMAND ENGINE",font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Tell AIRA what to do — hands free",font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Mic animation
        self.mic_canvas=tk.Canvas(self.root,width=120,height=120,bg=BG,highlightthickness=0)
        self.mic_canvas.pack(pady=5)
        self._draw_mic(False)

        self.status=tk.Label(self.root,text="Tap to start listening",font=("Courier",11,"bold"),bg=BG,fg=DIM)
        self.status.pack(pady=5)

        # Command list
        tk.Label(self.root,text="◈ AVAILABLE COMMANDS",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15)
        cmd_f=tk.Frame(self.root,bg=BG3);cmd_f.pack(fill="x",padx=15,pady=3)
        cmds=['"open ghost"','"open vault"','"open threat"','"open dark web"',
              '"open osint"','"open aira"','"open settings"','"open scanner"']
        for i,c in enumerate(cmds):
            row,col=divmod(i,2)
            tk.Label(cmd_f,text=f"• {c}",font=("Courier",8),bg=BG3,fg=NEON).grid(row=row,column=col,padx=10,pady=2,sticky="w")

        # Log
        tk.Label(self.root,text="◈ COMMAND LOG",font=("Courier",9,"bold"),bg=BG,fg=PURPLE).pack(anchor="w",padx=15,pady=(8,2))
        self.log_box=tk.Text(self.root,height=7,bg=BG3,fg=WHITE,font=("Courier",9),relief="flat",state="disabled")
        self.log_box.pack(fill="both",expand=True,padx=15,pady=3)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("y",foreground=GOLD)

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        self.listen_btn=tk.Button(bf,text="🎙️ START LISTENING",font=("Courier",11,"bold"),
                                   bg=PURPLE,fg=WHITE,relief="flat",padx=15,pady=8,command=self.toggle)
        self.listen_btn.pack(side="left",padx=5)
        tk.Label(self.root,text="BrayoOS Voice Engine • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def _draw_mic(self,active):
        self.mic_canvas.delete("all")
        color=RED if active else PURPLE
        # Outer rings
        for r,opacity in [(55,0.1),(45,0.2),(35,0.3)]:
            if active:
                self.mic_canvas.create_oval(60-r,60-r,60+r,60+r,outline=color,width=1)
        # Mic body
        self.mic_canvas.create_rectangle(45,25,75,75,fill=color,outline="",width=0)
        self.mic_canvas.create_oval(45,15,75,45,fill=color,outline="")
        self.mic_canvas.create_oval(45,55,75,85,fill=color,outline="")
        # Stand
        self.mic_canvas.create_line(60,80,60,100,fill=color,width=3)
        self.mic_canvas.create_line(45,100,75,100,fill=color,width=3)
        if active:
            self.mic_canvas.create_text(60,110,text="LISTENING",fill=RED,font=("Courier",8,"bold"))

    def log(self,msg,tag="y"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def toggle(self):
        if not self.listening:
            self.listening=True
            self.listen_btn.config(text="⏹ STOP",bg=RED)
            self.status.config(text="🎙️ LISTENING...",fg=RED)
            self._draw_mic(True)
            threading.Thread(target=self.listen_loop,daemon=True).start()
        else:
            self.listening=False
            self.listen_btn.config(text="🎙️ START LISTENING",bg=PURPLE)
            self.status.config(text="Tap to start listening",fg=DIM)
            self.root.after(0,self._draw_mic,False)

    def listen_loop(self):
        self.root.after(0,self.log,"🎙️ Voice recognition active...")
        while self.listening:
            try:
                result=subprocess.check_output(
                    "termux-speech-to-text 2>/dev/null",
                    shell=True,timeout=8).decode().strip().lower()
                if result:
                    self.root.after(0,self.log,f'Heard: "{result}"',"y")
                    self.root.after(0,self.process_command,result)
            except subprocess.TimeoutExpired:
                pass
            except Exception as e:
                self.root.after(0,self.log,f"⚠️ Mic error: {e}","r")
                time.sleep(2)

    def process_command(self,text):
        for cmd,(script,msg) in COMMANDS.items():
            if cmd in text:
                self.log(f"✅ {msg}","g")
                subprocess.Popen(["python3",os.path.expanduser(f"~/BrayoOS/core/apps/{script}")],
                                env={**os.environ,"DISPLAY":":1"})
                subprocess.Popen(f'termux-tts-speak "{msg}" 2>/dev/null',shell=True)
                return
        if "backup" in text:
            self.log("💾 Backing up BrayoOS...","y")
            subprocess.Popen("cd ~/BrayoOS && git add -A && git commit -m 'Voice backup' && git push origin main",shell=True)
        elif "status" in text or "report" in text:
            self.log("📊 All systems nominal. BrayoOS v3.5 running.","g")
            subprocess.Popen('termux-tts-speak "All systems nominal. BrayoOS is running." 2>/dev/null',shell=True)
        else:
            self.log(f'⚠️ Unknown: "{text}" — try "open ghost"',"r")

if __name__=="__main__":
    root=tk.Tk();VoiceCommands(root);root.mainloop()
