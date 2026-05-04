#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ BrayoOS Universal Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Detect platform
if [ -d "/data/data/com.termux" ]; then
    PLATFORM="android"
elif [ "$(uname)" == "Darwin" ]; then
    PLATFORM="mac"
elif grep -q "Microsoft" /proc/version 2>/dev/null; then
    PLATFORM="windows"
else
    PLATFORM="linux"
fi

echo "📱 Platform: $PLATFORM"

case $PLATFORM in
    android)
        echo "📱 Installing for Android/Termux..."
        pkg install -y python python-tkinter git
        pip install httpx pillow requests flask
        ;;
    linux)
        echo "🐧 Installing for Linux..."
        sudo apt install -y python3 python3-tk git
        pip3 install httpx pillow requests flask
        ;;
    mac)
        echo "🍎 Installing for Mac..."
        brew install python3 git
        pip3 install httpx pillow requests flask
        ;;
    windows)
        echo "🪟 Installing for Windows..."
        pip install httpx pillow requests flask
        ;;
esac

# Copy BrayoOS files
mkdir -p ~/BrayoOS
cp -r * ~/BrayoOS/ 2>/dev/null

echo "✅ BrayoOS installed for $PLATFORM!"
echo "Run: python ~/BrayoOS/core/desktop.py"
