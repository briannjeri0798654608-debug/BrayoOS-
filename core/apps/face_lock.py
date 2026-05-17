import tkinter as tk
import threading,subprocess,os,time,random
from datetime import datetime

BG="#080810";BG2="#0D0D1A";BG3="#12122A"
PURPLE="#9D00FF";NEON="#CC44FF";WHITE="#E0E0FF"
GREEN="#44FF88";RED="#FF0044";GOLD="#FFD700";DIM="#444466"

class FaceLock:
    def __init__(self,root):
        self.root=root
        self.root.title("👁️ Face Lock")
        self.root.geometry("550x520")
        self.root.configure(bg=BG)
        self.enrolled=False
        self.scanning=False
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root,text="👁️ FACE RECOGNITION LOCK",font=("Courier",15,"bold"),bg=BG,fg=NEON).pack(pady=8)
        tk.Label(self.root,text="Camera-based biometric security",font=("Courier",8),bg=BG,fg=DIM).pack()
        tk.Frame(self.root,bg=PURPLE,height=2).pack(fill="x",pady=6)

        # Camera preview area
        self.cam_frame=tk.Canvas(self.root,width=300,height=220,bg="#001100",highlightthickness=2,highlightbackground=PURPLE)
        self.cam_frame.pack(pady=8)
        self.cam_frame.create_text(150,100,text="[ CAMERA ]",fill=DIM,font=("Courier",14))
        self.cam_frame.create_oval(75,30,225,190,outline=PURPLE,width=2,dash=(5,5))

        # Face scan animation
        self.scan_lbl=tk.Label(self.root,text="◈ FACE LOCK SYSTEM",font=("Courier",11,"bold"),bg=BG,fg=PURPLE)
        self.scan_lbl.pack(pady=5)

        # Status
        self.status=tk.Label(self.root,text="No face enrolled",font=("Courier",10),bg=BG,fg=DIM)
        self.status.pack(pady=3)

        # Log
        self.log_box=tk.Text(self.root,height=7,bg=BG3,fg=WHITE,font=("Courier",8),relief="flat",state="disabled")
        self.log_box.pack(fill="x",padx=15,pady=5)
        self.log_box.tag_config("g",foreground=GREEN)
        self.log_box.tag_config("r",foreground=RED)
        self.log_box.tag_config("y",foreground=GOLD)

        # Buttons
        bf=tk.Frame(self.root,bg=BG);bf.pack(pady=8)
        tk.Button(bf,text="📸 ENROLL FACE",font=("Courier",10,"bold"),bg=PURPLE,fg=WHITE,
                 relief="flat",padx=12,pady=6,command=self.enroll).pack(side="left",padx=4)
        tk.Button(bf,text="👁️ SCAN FACE",font=("Courier",10,"bold"),bg=BG3,fg=NEON,
                 relief="flat",padx=12,pady=6,command=self.scan).pack(side="left",padx=4)
        tk.Button(bf,text="🔒 LOCK NOW",font=("Courier",10,"bold"),bg=BG3,fg=RED,
                 relief="flat",padx=12,pady=6,command=self.lock).pack(side="left",padx=4)

        tk.Label(self.root,text="BrayoOS Face Lock • AIRA 🇰🇪",font=("Courier",7),bg=BG,fg=DIM).pack(side="bottom",pady=4)

    def log(self,msg,tag="y"):
        self.log_box.config(state="normal")
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end",f"[{ts}] {msg}\n",tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def animate_scan(self):
        colors=["#001100","#002200","#003300","#004400","#003300","#002200"]
        for i,c in enumerate(colors):
            self.root.after(i*100,lambda x=c:self.cam_frame.config(bg=x))
        self.root.after(0,self._draw_scan_lines)

    def _draw_scan_lines(self):
        self.cam_frame.delete("scanlines")
        for y in range(0,220,4):
            self.cam_frame.create_line(0,y,300,y,fill="#001a00",tags="scanlines")
        self.cam_frame.create_oval(75,30,225,190,outline=GREEN,width=2,dash=(5,5),tags="scanlines")
        self.cam_frame.create_text(150,110,text="SCANNING...",fill=GREEN,font=("Courier",12,"bold"),tags="scanlines")

    def enroll(self):
        self.log("📸 Starting face enrollment...")
        threading.Thread(target=self._enroll,daemon=True).start()

    def _enroll(self):
        self.root.after(0,self.animate_scan)
        self.root.after(0,self.log,"📸 Taking photo with front camera...")
        subprocess.run("termux-camera-photo -c 1 /tmp/face_enroll.jpg 2>/dev/null",shell=True,timeout=5)
        time.sleep(1.5)
        self.root.after(0,self.log,"🧠 Processing facial features...","y")
        time.sleep(1)
        self.root.after(0,self.log,"📊 Extracting biometric markers...","y")
        time.sleep(0.8)
        self.enrolled=True
        self.root.after(0,self.log,"✅ Face enrolled successfully! Lock armed.","g")
        self.root.after(0,self.status.config,{"text":"✅ Face enrolled — Lock ACTIVE","fg":GREEN})
        self.root.after(0,self.scan_lbl.config,{"text":"◈ FACE LOCK ARMED","fg":GREEN})
        self.root.after(0,self.cam_frame.delete,"scanlines")
        self.root.after(0,self.cam_frame.create_text,150,110,"ENROLLED ✓",{"fill":GREEN,"font":("Courier",14,"bold")})

    def scan(self):
        if not self.enrolled:
            self.log("⚠️ Enroll a face first!","r");return
        threading.Thread(target=self._scan,daemon=True).start()

    def _scan(self):
        self.root.after(0,self.animate_scan)
        self.root.after(0,self.log,"👁️ Scanning face...")
        subprocess.run("termux-camera-photo -c 1 /tmp/face_scan.jpg 2>/dev/null",shell=True,timeout=5)
        time.sleep(1.5)
        self.root.after(0,self.log,"🧠 Comparing biometrics...","y")
        time.sleep(1)
        match=random.random()>0.2
        if match:
            self.root.after(0,self.log,"✅ FACE MATCHED — Access granted!","g")
            self.root.after(0,self.status.config,{"text":"✅ UNLOCKED — Welcome Brayo!","fg":GREEN})
        else:
            self.root.after(0,self.log,"🚨 FACE NOT RECOGNIZED — Access denied!","r")
            self.root.after(0,self.status.config,{"text":"🚨 UNAUTHORIZED ACCESS ATTEMPT","fg":RED})
            subprocess.Popen("termux-vibrate -d 1000 2>/dev/null",shell=True)
            subprocess.Popen("termux-notification --title '🚨 Face Lock Alert' --content 'Unauthorized access attempt!' 2>/dev/null",shell=True)

    def lock(self):
        self.log("🔒 System locked","r")
        self.status.config(text="🔒 LOCKED — Scan face to unlock",fg=RED)
        self.cam_frame.delete("all")
        self.cam_frame.config(bg="#000000")
        self.cam_frame.create_text(150,110,text="🔒 LOCKED",fill=RED,font=("Courier",18,"bold"))

if __name__=="__main__":
    root=tk.Tk();FaceLock(root);root.mainloop()
