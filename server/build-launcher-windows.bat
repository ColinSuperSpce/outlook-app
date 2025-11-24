@echo off
REM Build Windows GUI launcher executable

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Building Windows GUI launcher...

REM Check if PyInstaller is installed
python3 -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM Build with PyInstaller
REM --windowed: No console window (GUI only)
REM --onefile: Single executable
REM --name: Output name
python3 -m PyInstaller ^
    --windowed ^
    --onefile ^
    --name "Outlook Auto Attach Server" ^
    --add-data "outlook-attach-server.py;." ^
    --hidden-import=tkinter ^
    --hidden-import=win32com.client ^
    --clean ^
    outlook-attach-launcher.py

echo.
echo Build complete!
echo Executable: dist\Outlook Auto Attach Server.exe
echo.
pause

