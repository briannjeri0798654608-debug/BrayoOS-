#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ Magisk Root Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p ~/BrayoOS/phase3/root
echo "Downloading Magisk..."
wget -O ~/BrayoOS/phase3/root/Magisk.apk \
    "https://github.com/topjohnwu/Magisk/releases/latest/download/Magisk-v27.0.apk"
echo "✅ Magisk downloaded!"
echo "Install via: adb install ~/BrayoOS/phase3/root/Magisk.apk"
