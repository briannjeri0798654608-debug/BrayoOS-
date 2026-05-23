#!/bin/bash
cd "$(dirname "$0")"
clear
echo "BrayoOS v4.5 Portable — Built by Brayo & AIRA 🇰🇪"
# Check Python
if ! command -v python3 &>/dev/null; then
    echo "Installing Python via Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python3
fi
pip3 install httpx pillow 2>/dev/null
python3 BrayoOS_Portable.py
