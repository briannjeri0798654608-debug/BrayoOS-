@echo off
title BrayoOS v4.5 Portable
color 0A
echo.
echo   ██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗
echo   ╚════██╗╚════██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔════╝
echo    █████╔╝ █████╔╝███████║ ╚████╔╝ ██║   ██║╚█████╗  ███████╗
echo   ██╔═══╝ ██╔═══╝ ██╔══██║  ╚██╔╝  ██║   ██║ ╚═══██╗ ╚════██║
echo   ███████╗███████╗██║  ██║   ██║   ╚██████╔╝██████╔╝ ███████║
echo   ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚══════╝
echo.
echo   BrayoOS v4.5 Portable Edition
echo   Built by Brayo ^& AIRA - Kenya 🇰🇪
echo   Two minds. One OS. Built Different.
echo   Copyright 2026 Brayo - GPL-3.0
echo.
echo   Checking Python...
python --version 2>nul
if errorlevel 1 (
    echo   Python not found! Download from python.org
    echo   Then run this file again.
    pause
    start https://python.org/downloads
    exit
)
echo   Launching BrayoOS...
python BrayoOS_Portable.py
if errorlevel 1 (
    echo.
    echo   Error launching. Installing requirements...
    pip install httpx pillow
    python BrayoOS_Portable.py
)
pause
