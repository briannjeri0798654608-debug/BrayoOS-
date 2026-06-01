import tkinter as tk
import os,subprocess
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class QRGenerator:
    def __init__(self,root):
        self.root=root
        self.root.title("📱 QR Generator")
        self.root.geometry("600x520")
        self.root.configure(bg=BG)
        self.build_ui()
        self.check_deps()

    def build_ui(self):
        tk.Label(self.root,text="📱 QR CODE GENERATOR",
                font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Generate QR codes for anything",
                font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Quick presets
        pf=tk.Frame(self.root,bg=BG);pf.pack(fill="x",padx=15,pady=5)
        tk.Label(pf,text="Quick:",font=("Courier",8),bg=BG,fg=DIM).pack(side="left")
        presets=[
            ("BrayoOS GitHub","https://github.com/briannjeri0798654608-debug/BrayoOS-"),
            ("My WiFi","WIFI:S:BrayoOS;T:WPA;P:BrayoOS1337;;"),
            ("WhatsApp Me","https://wa.me/254"),
            ("BrayoOS v5.0","BrayoOS v5.0 — Built by Brayo Kenya 🇰🇪"),
        ]
        for label,val in presets:
            tk.Button(pf,text=label,font=("Courier",7),bg=BG3,fg=NEON,
                     relief="flat",padx=5,pady=2,
                     command=lambda v=val:self.set_text(v)).pack(side="left",padx=2)

        # Input
        if_=tk.Frame(self.root,bg=BG3);if_.pack(fill="x",padx=15,pady=5)
        tk.Label(if_,text="◈ TEXT / URL / DATA:",
                font=("Courier",9,"bold"),bg=BG3,fg=PURPLE).pack(anchor="w",padx=8,pady=(8,3))
        self.inp=tk.Text(if_,height=3,bg=BG,fg=WHITE,
                        font=("Courier",10),relief="flat",insertbackground=NEON)
        self.inp.pack(fill="x",padx=8,pady=(0,8))
        self.inp.insert("end","https://github.com/briannjeri0798654608-debug/BrayoOS-")

        # Size
        sf=tk.Frame(self.root,bg=BG);sf.pack(fill="x",padx=15,pady=3)
        tk.Label(sf,text="Size:",font=("Courier",9),bg=BG,fg=DIM).pack(side="left",padx=5)
        self.size_var=tk.StringVar(value="300")
        for s in ["150","200","300","400"]:
            tk.Radiobutton(sf,text=f"{s}px",variable=self.size_var,value=s,
                          bg=BG,fg=NEON,selectcolor=PURPLE,
                          activebackground=BG,font=("Courier",8)).pack(side="left",padx=8)

        # Generate button
        tk.Button(self.root,text="⚡ GENERATE QR CODE",
                 font=("Courier",11,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=15,pady=8,
                 command=self.generate).pack(pady=8)

        # QR display
        self.qr_canvas=tk.Canvas(self.root,width=300,height=200,
                                 bg=BG3,highlightthickness=2,
                                 highlightbackground=PURPLE)
        self.qr_canvas.pack(pady=5)
        self.qr_canvas.create_text(150,100,text="QR code appears here",
                                  fill=DIM,font=("Courier",10))

        self.status=tk.Label(self.root,text="Ready",
                            font=("Courier",8),bg=BG,fg=DIM)
        self.status.pack()
        tk.Label(self.root,text="BrayoOS QR Generator v5.0 • AIRA 🇰🇪",
                font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=3)

    def set_text(self,text):
        self.inp.delete("1.0","end")
        self.inp.insert("end",text)

    def check_deps(self):
        result=subprocess.run("python3 -c 'import qrcode' 2>/dev/null",
                             shell=True,capture_output=True)
        if result.returncode!=0:
            self.status.config(text="Installing qrcode...",fg=GOLD)
            subprocess.Popen(
                "pip install qrcode pillow --break-system-packages -q 2>/dev/null",
                shell=True)

    def generate(self):
        text=self.inp.get("1.0","end").strip()
        if not text:return
        self.status.config(text="Generating...",fg=GOLD)
        try:
            import qrcode
            from PIL import ImageTk
            size=int(self.size_var.get())
            qr=qrcode.QRCode(box_size=8,border=2)
            qr.add_data(text)
            qr.make(fit=True)
            img=qr.make_image(fill_color="#9D00FF",back_color="#080810")
            img=img.resize((size,size))
            path=os.path.expanduser("~/BrayoOS/memory/last_qr.png")
            img.save(path)
            photo=ImageTk.PhotoImage(img.resize((280,280)))
            self.qr_canvas.config(width=300,height=300)
            self.qr_canvas.delete("all")
            self.qr_canvas.create_image(150,150,image=photo)
            self.qr_canvas._photo=photo
            self.status.config(text=f"✅ QR saved to ~/BrayoOS/memory/last_qr.png",fg=GREEN)
        except ImportError:
            self.status.config(text="Run: pip install qrcode pillow --break-system-packages",fg=RED)
        except Exception as e:
            self.status.config(text=f"Error: {str(e)[:40]}",fg=RED)

if __name__=="__main__":
    root=tk.Tk();QRGenerator(root);root.mainloop()
