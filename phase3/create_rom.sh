#!/bin/bash
echo "⚡ Creating BrayoOS Flashable ZIP..."

mkdir -p ~/BrayoOS_ROM/{META-INF/com/google/android,system/app,data/app}

# Create installer script
cat > ~/BrayoOS_ROM/META-INF/com/google/android/update-binary << 'BINEOF'
#!/sbin/sh
SKIPUNZIP=1
ui_print() { echo "$1"; }
set_progress() { echo "set_progress $1"; }

ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ui_print "  ⚡ BrayoOS v2.0 Installer"
ui_print "  Built by Brayo & ARIA"
ui_print "  2026"
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

set_progress 0.1
ui_print "📦 Extracting BrayoOS..."
unzip -o "$ZIPFILE" -x "META-INF/*" -d /

set_progress 0.5
ui_print "⚙️  Setting permissions..."
chmod -R 755 /data/brayos
chmod +x /data/brayos/start.sh

set_progress 0.8
ui_print "🤖 Initializing ARIA..."
echo "ARIA_INITIALIZED=true" > /data/brayos/aria.conf

set_progress 1.0
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ui_print "✅ BrayoOS installed!"
ui_print "🔄 Reboot to start BrayoOS"
ui_print "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
BINEOF

chmod +x ~/BrayoOS_ROM/META-INF/com/google/android/update-binary

# Create updater-script
cat > ~/BrayoOS_ROM/META-INF/com/google/android/updater-script << 'UPDEOF'
assert(getprop("ro.product.device") == "pond" ||
       getprop("ro.product.device") == "lake");
UPDEOF

# Copy BrayoOS files to ROM
cp -r ~/BrayoOS ~/BrayoOS_ROM/data/brayos

# Create start script inside ROM
cat > ~/BrayoOS_ROM/data/brayos/start.sh << 'STARTEOF'
#!/bin/bash
export DISPLAY=:1
vncserver :1 -geometry 1280x720 -depth 24 -localhost -SecurityTypes None
sleep 2
python ~/BrayoOS/core/boot.py &
STARTEOF

# Package ROM as ZIP
cd ~/BrayoOS_ROM
zip -r ~/BrayoOS_v2.0_pond.zip .
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ROM created!"
echo "📦 File: ~/BrayoOS_v2.0_pond.zip"
du -sh ~/BrayoOS_v2.0_pond.zip
echo "Copy to SD: cp ~/BrayoOS_v2.0_pond.zip /sdcard/"
