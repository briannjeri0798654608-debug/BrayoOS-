#!/bin/bash
echo "⚡ Packaging BrayoOS ROM..."
mkdir -p ~/BrayoOS_ROM/{META-INF/com/google/android,system,data}

# Create updater-script
cat > ~/BrayoOS_ROM/META-INF/com/google/android/updater-script << 'UPDEOF'
ui_print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
ui_print("  ⚡ BrayoOS v2.0 Installer");
ui_print("  Built by Brayo & ARIA (Claude)");
ui_print("  2026");
ui_print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
ui_print("Installing BrayoOS...");
run_program("/sbin/busybox", "mount", "/system");
ui_print("✅ BrayoOS installed!");
ui_print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
UPDEOF

# Create update-binary
cat > ~/BrayoOS_ROM/META-INF/com/google/android/update-binary << 'BINEOF'
#!/sbin/sh
SKIPUNZIP=1
ui_print() { echo "$1"; }
ui_print "⚡ BrayoOS Installer Starting..."
BINEOF

chmod +x ~/BrayoOS_ROM/META-INF/com/google/android/update-binary

echo "✅ ROM structure created!"
echo "📁 Location: ~/BrayoOS_ROM/"
