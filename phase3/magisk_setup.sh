#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ Magisk Root Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Install Magisk APK"
echo "APK location: ~/BrayoOS/phase3/root/Magisk.apk"
ls -lh ~/BrayoOS/phase3/root/Magisk.apk
echo ""
echo "Step 2: Install on device"
adb install ~/BrayoOS/phase3/root/Magisk.apk
echo ""
echo "Step 3: Patch boot image"
echo "- Open Magisk app"
echo "- Tap Install → Select boot.img"
echo "- Copy patched_boot.img to PC"
echo "- Flash: fastboot flash boot patched_boot.img"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
