#!/bin/bash
echo "⚡ Building BrayoOS Portable Package..."

# Create portable directory
mkdir -p ~/BrayoOS_Portable/{windows,linux,android}

# Copy all BrayoOS files
cp -r ~/BrayoOS/apps ~/BrayoOS_Portable/
cp -r ~/BrayoOS/core ~/BrayoOS_Portable/
cp -r ~/BrayoOS/assets ~/BrayoOS_Portable/

# Create Windows launcher
cat > ~/BrayoOS_Portable/windows/START_BRAYOS.bat << 'WINEOF'
@echo off
title BrayoOS Portable
echo Starting BrayoOS...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Installing...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
    python_installer.exe /quiet InstallAllUsers=0 PrependPath=1
)
pip install httpx requests flask tkinter -q
python core\desktop.py
WINEOF

# Create Linux launcher
cat > ~/BrayoOS_Portable/linux/start_brayos.sh << 'LINEOF'
#!/bin/bash
echo "⚡ Starting BrayoOS on Linux..."
# Check dependencies
command -v python3 >/dev/null 2>&1 || { sudo apt install -y python3; }
pip3 install httpx requests flask -q
python3 core/desktop.py
LINEOF
chmod +x ~/BrayoOS_Portable/linux/start_brayos.sh

# Create README
cat > ~/BrayoOS_Portable/README.txt << 'READEOF'
⚡ BrayoOS Portable v2.0
Built by Brayo

HOW TO RUN:
-----------
Windows: Double click START_BRAYOS.bat
Linux: bash linux/start_brayos.sh
Android/Termux: bash core/start.sh

REQUIREMENTS:
-------------
- Python 3.8+
- Internet connection (for AI features)
- Set GROQ_API_KEY environment variable

FEATURES:
---------
- AI Chat (Groq LLaMA 3.3 70B)
- Network Scanner
- File Manager
- Code Editor
- System Monitor
- Telegram Bot
READEOF

echo "✅ Portable package created at ~/BrayoOS_Portable"
