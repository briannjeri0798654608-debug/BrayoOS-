#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ BrayoOS Bootloader Unlock Tool"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Step 1: Enable OEM Unlock"
adb shell settings put global oem_unlock_enabled 1
echo ""
echo "Step 2: Check unlock status"
adb shell getprop ro.boot.flash.locked
echo ""
echo "Step 3: Reboot to fastboot"
adb reboot bootloader
echo ""
echo "Step 4: Unlock bootloader"
fastboot flashing unlock
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
