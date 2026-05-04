#!/bin/bash
echo "⚡ BrayoOS Linux/Mac Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Install dependencies
if command -v apt &>/dev/null; then
    sudo apt install -y python3 python3-tk python3-pip git
elif command -v brew &>/dev/null; then
    brew install python3 git
elif command -v pacman &>/dev/null; then
    sudo pacman -S python python-tkinter git
fi

pip3 install httpx pillow requests flask --break-system-packages 2>/dev/null || \
pip3 install httpx pillow requests flask

echo "✅ Launching BrayoOS..."
python3 ~/BrayoOS/core/desktop.py
