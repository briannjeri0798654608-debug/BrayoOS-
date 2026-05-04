#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ BrayoOS Wireless ADB Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Enable wireless debugging via ADB
echo "📱 Your IP:"
ip addr show wlan0 | grep "inet " | awk '{print $2}'

echo ""
echo "Enable Wireless Debugging:"
echo "Settings → Developer Options → Wireless Debugging"
echo ""

# Connect to self via ADB
IP=$(ip route get 8.8.8.8 | awk '{print $7}' | head -1)
echo "Your IP: $IP"

echo "Connecting ADB..."
adb connect $IP:5555 2>/dev/null || \
adb connect 127.0.0.1:5555 2>/dev/null

echo ""
adb devices
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
