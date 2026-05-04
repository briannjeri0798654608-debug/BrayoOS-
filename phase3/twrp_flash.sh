#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ BrayoOS TWRP Flash Tool"
echo "Device: Redmi 14C (pond)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Connect phone via USB"
echo "Step 2: Enable USB Debugging"
echo "Step 3: Running..."
adb devices
echo "Step 4: Rebooting to fastboot..."
adb reboot bootloader
sleep 5
echo "Step 5: Flashing TWRP..."
fastboot flash recovery ~/BrayoOS/phase3/recovery/twrp.img
echo "Step 6: Booting TWRP..."
fastboot boot ~/BrayoOS/phase3/recovery/twrp.img
echo "✅ TWRP flashed!"
