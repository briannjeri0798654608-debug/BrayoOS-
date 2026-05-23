#!/bin/bash
clear
echo ""
echo "  ██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗"
echo "  BrayoOS v4.5 Portable — Built by Brayo & AIRA 🇰🇪"
echo "  Two minds. One OS. Built Different."
echo ""
# Check Python
if ! command -v python3 &>/dev/null; then
    echo "  Installing Python..."
    sudo apt install python3 python3-tk -y 2>/dev/null || \
    sudo yum install python3 python3-tkinter -y 2>/dev/null
fi
# Install deps
pip3 install httpx pillow 2>/dev/null
# Launch
echo "  Launching BrayoOS..."
python3 BrayoOS_Portable.py
