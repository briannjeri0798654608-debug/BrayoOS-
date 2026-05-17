import tkinter as tk
import threading,subprocess,os,time
from datetime import datetime

BG="#000800";BG2="#001100";BG3="#002200"
GREEN="#00FF41";DIM="#004400";WHITE="#AAFFAA"
RED="#FF0044";GOLD="#FFD700";NEON="#CC44FF"

TOOLS={
    "nmap":"Network port scanner",
    "curl":"HTTP request tool",
    "wget":"File downloader",
    "nc":"Netcat — network Swiss knife",
    "python3":"Python interpreter",
    "git":"Version control",
    "ssh":"Secure shell",
    "ping":"Network ping test",
}

PRESETS=[
    ("🔍 Port Scan","nmap -sV --open -T4 scanme.nmap.org"),
    ("🌐 HTTP GET","curl -I https://google.com"),
    ("📡 Ping Test","ping -c 4 8.8.8.8"),
    ("💻 My IP","curl ifconfig.me"),
    ("🔎 DNS Lookup","nslookup google.com"),
    ("📊 Net Stats","cat /proc/net/if_inet6"),
    ("🔒 SSL Check","curl -vI https://github.com 2>&1 | grep SSL"),
    ("🕵️ Trace Route","traceroute google.com"),
]

class HackTerminal:
    def __init__(self,root):
        self.root=root
        self.root.title("💀 BrayoOS Hack Terminal")
        self.root.geometry("750x580")
        self.root.configure(bg=BG)
        self.history=[]
        self.hist_idx=0
        self.running_proc=None
        self.build_ui()
        self.banner()

    def build_ui(self):
        # Title bar
        tb=tk.Frame(self.root,bg=BG2,height=38)
        tb.pack(fill="x");tb.pack_propagate(False)
        tk.Label(tb,text="💀 BRAYOOS HACK TERMINAL",font=("Courier",12,"bold"),bg=BG2,fg=GREEN).pack(side="left",padx=12,pady=8)
        tk.Label(tb,text="root@BrayoOS:~#",font=("Courier",9),bg=BG2,fg=DIM).pack(side="left")
        tk.Label(tb,text="🇰🇪",font=("Arial",12),bg=BG2).pack(side="right",padx=8)
        tk.Frame(self.root,bg=GREEN,height=1).pack(fill="x")

        main=tk.Frame(self.root,bg=BG)
        main.pack(fill="both",expand=True)

        # Left — presets
        left=tk.Frame(main,bg=BG2,width=180)
        left.pack(side="left",fill="y")
        left.pack_propagate(False)

        tk.Label(left,text="◈ QUICK COMMANDS",font=("Courier",8,"bold"),bg=BG2,fg=GREEN).pack(pady=(8,4),padx=5,anchor="w")
        for label,cmd in PRESETS:
            tk.Button(left,text=label,font=("Courier",8),bg=BG3,fg=GREEN,relief="flat",
                     anchor="w",padx=8,pady=4,
                     command=lambda c=cmd:self.run_preset(c)).pack(fill="x",padx=4,pady=1)

        tk.Frame(left,bg=GREEN,height=1,width=160).pack(pady=8)
        tk.Label(left,text="◈ INSTALLED TOOLS",font=("Courier",8,"bold"),bg=BG2,fg=GREEN).pack(padx=5,anchor="w",pady=(0,4))
        for tool,desc in TOOLS.items():
            f=tk.Frame(left,bg=BG2)
            f.pack(fill="x",padx=5,pady=1)
            tk.Label(f,text=tool,font=("Courier",8,"bold"),bg=BG2,fg=GREEN,width=8,anchor="w").pack(side="left")
            # Check if installed
            exists=subprocess.run(f"which {tool} 2>/dev/null",shell=True,capture_output=True).returncode==0
            tk.Label(f,text="✓" if exists else "✗",font=("Courier",8),bg=BG2,fg=GREEN if exists else RED).pack(side="right",padx=4)

        # Right — terminal
        right=tk.Frame(main,bg=BG)
        right.pack(side="left",fill="both",expand=True)

        self.output=tk.Text(right,bg=BG,fg=GREEN,font=("Courier",9),
                           relief="flat",insertbackground=GREEN,
                           selectbackground=BG3,selectforeground=WHITE)
        self.output.pack(fill="both",expand=True,padx=5,pady=5)
        self.output.tag_config("cmd",foreground=GOLD)
        self.output.tag_config("err",foreground=RED)
        self.output.tag_config("sys",foreground=NEON)
        self.output.tag_config("ok",foreground=GREEN)

        # Input
        input_f=tk.Frame(right,bg=BG2)
        input_f.pack(fill="x",padx=5,pady=(0,5))
        tk.Label(input_f,text="root@BrayoOS:~# ",font=("Courier",10,"bold"),bg=BG2,fg=GREEN).pack(side="left",padx=5,pady=6)
        self.cmd_input=tk.Entry(input_f,font=("Courier",10),bg=BG,fg=GREEN,
                               insertbackground=GREEN,relief="flat")
        self.cmd_input.pack(side="left",fill="x",expand=True,ipady=6)
        self.cmd_input.bind("<Return>",lambda e:self.execute())
        self.cmd_input.bind("<Up>",self.hist_up)
        self.cmd_input.bind("<Down>",self.hist_down)
        self.cmd_input.bind("<Tab>",self.autocomplete)
        self.cmd_input.focus()
        tk.Button(input_f,text="▶",font=("Courier",10,"bold"),bg=GREEN,fg=BG,
                 relief="flat",padx=8,command=self.execute).pack(side="right",padx=5,pady=4)
        tk.Button(input_f,text="■",font=("Courier",10,"bold"),bg=RED,fg=WHITE,
                 relief="flat",padx=6,command=self.kill_proc).pack(side="right",pady=4)

    def banner(self):
        banner=f"""
{GREEN}  ██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗
  ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝
  ██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗
  ██╔══██╗██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║
  ██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝

  BrayoOS Hack Terminal v3.5
  Built by Brayo & AIRA 🇰🇪 | Two minds. One OS. Built Different.
  Type 'help' for commands | Use presets on the left
  WARNING: For authorized testing only!
"""
        self.write(banner,"ok")
        self.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Terminal ready.\n\n","sys")

    def write(self,text,tag="ok"):
        self.output.config(state="normal")
        self.output.insert("end",text,tag)
        self.output.see("end")
        self.output.config(state="disabled" if False else "normal")

    def run_preset(self,cmd):
        self.cmd_input.delete(0,"end")
        self.cmd_input.insert(0,cmd)
        self.execute()

    def execute(self):
        cmd=self.cmd_input.get().strip()
        if not cmd:return
        self.history.append(cmd)
        self.hist_idx=len(self.history)
        self.cmd_input.delete(0,"end")
        self.write(f"root@BrayoOS:~# {cmd}\n","cmd")

        # Built-in commands
        if cmd=="clear":
            self.output.delete("1.0","end");return
        if cmd=="help":
            self.write("""
BUILT-IN COMMANDS:
  clear       — Clear terminal
  help        — Show this help
  apps        — List BrayoOS apps
  sysinfo     — System information
  tools       — Check installed tools
  exit        — Close terminal

PRESET COMMANDS: Use left sidebar
REAL COMMANDS: nmap, curl, ping, etc.
""","sys");return
        if cmd=="apps":
            apps=os.listdir(os.path.expanduser("~/BrayoOS/core/apps/"))
            self.write(f"BrayoOS Apps ({len(apps)}):\n","sys")
            for a in sorted(apps):self.write(f"  → {a}\n","ok")
            return
        if cmd=="sysinfo":
            threading.Thread(target=self._sysinfo,daemon=True).start();return
        if cmd in["exit","quit"]:
            self.root.destroy();return

        # Run real command
        threading.Thread(target=self._run,args=(cmd,),daemon=True).start()

    def _sysinfo(self):
        try:
            info=[
                ("OS","BrayoOS v3.5"),
                ("Device","Redmi 14C (pond)"),
                ("Kernel",open("/proc/version").read().split()[2]),
                ("Uptime",open("/proc/uptime").read().split()[0]+"s"),
                ("CPU Cores",str(os.cpu_count())),
            ]
            self.write("\nSYSTEM INFO:\n","sys")
            for k,v in info:self.write(f"  {k:<12} {v}\n","ok")
            self.write("\n","ok")
        except:pass

    def _run(self,cmd):
        try:
            self.running_proc=subprocess.Popen(
                cmd,shell=True,stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,text=True,
                cwd=os.path.expanduser("~"))
            for line in self.running_proc.stdout:
                self.root.after(0,self.write,line,"ok")
            self.running_proc.wait()
            rc=self.running_proc.returncode
            tag="ok" if rc==0 else "err"
            self.root.after(0,self.write,f"\n[exit:{rc}]\n",tag)
        except Exception as e:
            self.root.after(0,self.write,f"Error: {e}\n","err")

    def kill_proc(self):
        if self.running_proc:
            self.running_proc.kill()
            self.write("\n[KILLED]\n","err")

    def hist_up(self,e):
        if self.hist_idx>0:
            self.hist_idx-=1
            self.cmd_input.delete(0,"end")
            self.cmd_input.insert(0,self.history[self.hist_idx])

    def hist_down(self,e):
        if self.hist_idx<len(self.history)-1:
            self.hist_idx+=1
            self.cmd_input.delete(0,"end")
            self.cmd_input.insert(0,self.history[self.hist_idx])
        else:
            self.hist_idx=len(self.history)
            self.cmd_input.delete(0,"end")

    def autocomplete(self,e):
        cmd=self.cmd_input.get()
        apps=os.listdir(os.path.expanduser("~/BrayoOS/core/apps/"))
        matches=[a for a in apps if a.startswith(cmd)]
        if len(matches)==1:
            self.cmd_input.delete(0,"end")
            self.cmd_input.insert(0,f"python3 ~/BrayoOS/core/apps/{matches[0]}")
        return "break"

if __name__=="__main__":
    root=tk.Tk();HackTerminal(root);root.mainloop()
