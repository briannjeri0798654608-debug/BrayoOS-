#!/bin/bash
echo "⚡ BrayoOS Android Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Requirements: Termux from F-Droid"
echo ""

# Update and install
pkg update -y
pkg install -y python python-tkinter git \
    tigervnc openbox

pip install httpx pillow requests flask \
    --break-system-packages

# Setup VNC
mkdir -p ~/.vnc
cat > ~/.vnc/xstartup << 'VNCEOF'
#!/bin/bash
export DISPLAY=:1
openbox &
sleep 1
python ~/BrayoOS/core/desktop.py &
VNCEOF
chmod +x ~/.vnc/xstartup

# Create launcher
echo 'alias brayos="vncserver -kill :1 2>/dev/null; sleep 1; vncserver :1 -geometry 1280x720 -depth 24 -localhost -SecurityTypes None; sleep 3; export DISPLAY=:1; python ~/BrayoOS/core/desktop.py &"' >> ~/.bashrc

echo "✅ BrayoOS installed!"
echo "Type 'brayos' to start!"
