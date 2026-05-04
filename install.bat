@echo off
title BrayoOS Windows Installer
color 0A
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   ⚡ BrayoOS Windows Installer
echo   Built by Brayo ^& ARIA
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo [1] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Installing Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe' -OutFile '%TEMP%\python.exe'"
    %TEMP%\python.exe /quiet PrependPath=1
)
echo [✓] Python ready!
echo.
echo [2] Installing dependencies...
pip install httpx pillow requests flask tkinter -q
echo [✓] Dependencies ready!
echo.
echo [3] Launching BrayoOS...
python BrayoOS\core\desktop.py
pause
