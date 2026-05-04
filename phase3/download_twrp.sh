#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ BrayoOS TWRP Downloader"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Device: Redmi 14C (pond)"
echo "Downloading TWRP..."
mkdir -p ~/BrayoOS/phase3/recovery
wget -O ~/BrayoOS/phase3/recovery/twrp.img \
"https://dl.twrp.me/lake/twrp-3.7.0_12-0-lake.img" \
2>/dev/null || echo "⚠️ Download manually from twrp.me"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "After download run:"
echo "fastboot boot ~/BrayoOS/phase3/recovery/twrp.img"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
