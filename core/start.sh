#!/bin/bash
echo "⚡ Starting BrayoOS..."
source ~/.bashrc
vncserver -kill :1 2>/dev/null
sleep 1
vncserver :1 \
  -geometry 1280x720 \
  -depth 24 \
  -localhost \
  -SecurityTypes None
export DISPLAY=:1
sleep 2
DISPLAY=:1 openbox &
sleep 1
DISPLAY=:1 python ~/BrayoOS/core/boot.py
echo "✅ BrayoOS Started!"
echo "📱 Connect AVNC to localhost:5901"
