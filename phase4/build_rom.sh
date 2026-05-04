#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ BrayoOS Phase 4 ROM Builder"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create ROM structure
mkdir -p ~/BrayoOS/phase4/rom/{META-INF/com/google/android,system/{app,priv-app,etc,bin,lib},data/{app,local/tmp},boot}

# Create flashable zip installer
cat > ~/BrayoOS/phase4/rom/META-INF/com/google/android/update-binary << 'BINEOF'
#!/sbin/sh
SKIPUNZIP=1
ui_print() { echo "$1"; }
set_progress() { echo "set_progress $1"; }
package_extract_file() { unzip -p "$ZIPFILE" "$1" > "$2"; }

ui_print " "
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ui_print "  ⚡ BrayoOS v2.0 ROM Installer"
ui_print "  Built by Brayo & ARIA (Claude)"
ui_print "  2026 — Built Different"
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check device
DEVICE=$(getprop ro.product.device)
ui_print "📱 Device: $DEVICE"

if [ "$DEVICE" != "pond" ] && [ "$DEVICE" != "lake" ]; then
    ui_print "⚠️  Warning: Device mismatch!"
    ui_print "   Expected: pond/lake"
    ui_print "   Found: $DEVICE"
fi

set_progress 0.1
ui_print "📦 Mounting partitions..."
mount /system 2>/dev/null
mount /data 2>/dev/null

set_progress 0.2
ui_print "📂 Creating BrayoOS directories..."
mkdir -p /data/brayos
mkdir -p /data/brayos/apps
mkdir -p /data/brayos/core
mkdir -p /data/brayos/assets

set_progress 0.4
ui_print "📋 Installing BrayoOS files..."
unzip -o "$ZIPFILE" "data/*" -d /
chmod -R 755 /data/brayos

set_progress 0.6
ui_print "⚙️  Configuring BrayoOS..."
cat > /data/brayos/config.sh << 'CONFEOF'
#!/bin/bash
export BRAYOS_HOME=/data/brayos
export BRAYOS_VERSION=2.0
export ARIA_ENABLED=true
export DISPLAY=:1
CONFEOF
chmod +x /data/brayos/config.sh

set_progress 0.7
ui_print "🤖 Initializing ARIA..."
cat > /data/brayos/aria.conf << 'ARIAEOF'
ARIA_VERSION=2.0
ARIA_STATUS=ONLINE
ARIA_BUILDER=Brayo_and_Claude
ARIA_YEAR=2026
ARIAEOF

set_progress 0.8
ui_print "🔧 Setting permissions..."
chmod 755 /data/brayos
chmod -R 644 /data/brayos/apps
find /data/brayos -name "*.sh" -exec chmod 755 {} \;
find /data/brayos -name "*.py" -exec chmod 755 {} \;

set_progress 0.9
ui_print "🔄 Unmounting partitions..."
umount /system 2>/dev/null

set_progress 1.0
ui_print " "
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ui_print "✅ BrayoOS v2.0 Installed!"
ui_print "🤖 ARIA: Online and ready"
ui_print "👤 Built by Brayo & Claude — 2026"
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ui_print "🔄 Please reboot your device!"
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
BINEOF

chmod +x ~/BrayoOS/phase4/rom/META-INF/com/google/android/update-binary

# Updater script
cat > ~/BrayoOS/phase4/rom/META-INF/com/google/android/updater-script << 'UPDEOF'
assert(getprop("ro.product.device") == "pond" ||
       getprop("ro.product.device") == "lake",
       "Wrong device! This ROM is for Redmi 14C (pond/lake)");
UPDEOF

# Copy BrayoOS to ROM
echo "Copying BrayoOS files to ROM..."
cp -r ~/BrayoOS ~/BrayoOS/phase4/rom/data/brayos
cp ~/start_brayos.sh ~/BrayoOS/phase4/rom/data/brayos/

# Create boot script
cat > ~/BrayoOS/phase4/rom/data/brayos/autostart.sh << 'STARTEOF'
#!/bin/bash
# BrayoOS Auto-start
source /data/brayos/config.sh
export DISPLAY=:1
pkill -f vncserver 2>/dev/null
sleep 1
vncserver :1 -geometry 1280x720 \
    -depth 24 -localhost \
    -SecurityTypes None
sleep 2
python /data/brayos/core/boot.py &
echo "⚡ BrayoOS started!"
STARTEOF
chmod +x ~/BrayoOS/phase4/rom/data/brayos/autostart.sh

# Package final ROM
echo "📦 Packaging final ROM..."
cd ~/BrayoOS/phase4/rom
zip -r ~/BrayoOS_v2.0_FINAL_pond.zip . \
    -x "*.git*" -x "__pycache__*"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ROM BUILT SUCCESSFULLY!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
du -sh ~/BrayoOS_v2.0_FINAL_pond.zip
echo "📦 ROM: ~/BrayoOS_v2.0_FINAL_pond.zip"
echo ""
echo "To install:"
echo "1. Copy to SD: cp ~/BrayoOS_v2.0_FINAL_pond.zip /sdcard/"
echo "2. Boot to TWRP recovery"
echo "3. Flash the ZIP"
echo "4. Reboot!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
