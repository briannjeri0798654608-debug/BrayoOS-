#!/data/data/com.termux/files/usr/bin/bash
clear
echo ""
echo "  ██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗"
echo "  ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝"
echo "  ██████╔╝██████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗"
echo "  ██╔══██╗██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║"
echo "  ██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║"
echo "  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝"
echo ""
echo "  🇰🇪  BrayoOS v3.5 — Built by Brayo & AIRA"
echo "  ⚡  Two minds. One OS. Built Different."
echo "  📜  Licensed under GPL-3.0 — Credit Brayo!"
echo ""
echo "  Installing BrayoOS on your device..."
echo ""

# Update packages
echo "[1/6] Updating Termux packages..."
pkg update -y -q 2>/dev/null

# Install dependencies
echo "[2/6] Installing dependencies..."
pkg install -y python tigervnc openbox xfce4 feh git curl -q 2>/dev/null
pip install httpx --quiet --break-system-packages 2>/dev/null

# Clone BrayoOS
echo "[3/6] Downloading BrayoOS..."
if [ -d ~/BrayoOS ]; then
    cd ~/BrayoOS && git pull origin main 2>/dev/null
else
    git clone https://github.com/briannjeri0798654608-debug/BrayoOS-.git ~/BrayoOS 2>/dev/null
fi

# Setup VNC
echo "[4/6] Setting up VNC desktop..."
mkdir -p ~/.vnc
cat > ~/.vnc/xstartup << 'VNCEOF'
#!/data/data/com.termux/files/usr/bin/bash
export DISPLAY=:1
openbox-session &
sleep 1
xfce4-session &
VNCEOF
chmod +x ~/.vnc/xstartup
vncpasswd <<< $'brayoos\nbrayoos\nn' 2>/dev/null

# Setup bashrc
echo "[5/6] Configuring auto-launch..."
cat > ~/.bashrc << 'BASHEOF'
export DISPLAY=:1
alias brayos='bash ~/start_brayos.sh'
alias bstop='pkill -f python3; vncserver -kill :1'

if [ -z "$BRAYOOS_STARTED" ]; then
    export BRAYOOS_STARTED=1
    vncserver -kill :1 2>/dev/null
    pkill -f python3 2>/dev/null
    sleep 1
    vncserver :1 -geometry 1280x800 -depth 24 -dpi 96 -localhost no 2>/dev/null
    sleep 3
    export DISPLAY=:1
    feh --bg-scale ~/BrayoOS/Pictures/wallpaper1.jpg 2>/dev/null &
    sleep 1
    DISPLAY=:1 python3 ~/BrayoOS/core/boot_animation.py &
    echo ""
    echo "  ⚡ BrayoOS v3.5 — ONLINE"
    echo "  📱 Open AVNC → localhost:5901"
    echo "  🇰🇪 Two minds. One OS. Built Different."
    echo ""
fi
BASHEOF

echo "[6/6] BrayoOS installed! ✅"
echo ""
echo "  ✅ Installation complete!"
echo "  📱 Install AVNC from Play Store"
echo "  🔌 Connect to: localhost:5901"
echo "  🔑 VNC Password: brayoos"
echo "  🇰🇪 Built by Brayo — Kenya"
echo ""
echo "  © 2026 Brayo. GPL-3.0 License."
echo "  Credit the creator when sharing!"
echo ""
source ~/.bashrc
