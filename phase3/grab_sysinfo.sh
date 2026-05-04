#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ BrayoOS System Grabber"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 Device: $(getprop ro.product.model)"
echo "🔧 Android: $(getprop ro.build.version.release)"
echo "💻 CPU: $(getprop ro.product.cpu.abi)"
echo "🔓 Bootloader: $(getprop ro.boot.verifiedbootstate)"
echo "🔒 Encryption: $(getprop ro.crypto.state)"
echo "📡 Codename: $(getprop ro.product.device)"
echo "🏗️  Build: $(getprop ro.build.display.id)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💾 Storage:"
df -h /data /sdcard 2>/dev/null
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔋 Battery:"
cat /sys/class/power_supply/battery/capacity 2>/dev/null
echo "%"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
