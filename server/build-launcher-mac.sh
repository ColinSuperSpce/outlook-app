#!/bin/bash
# Build macOS GUI launcher executable

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🔨 Building macOS GUI launcher..."

# Check if PyInstaller is installed
if ! python3 -m PyInstaller --version &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Clean previous builds
rm -rf build dist *.spec

# Build with PyInstaller
# Using --onedir instead of --onefile for better macOS compatibility
# --windowed: No console window (GUI only)
# --name: Output name
python3 -m PyInstaller \
    --windowed \
    --onedir \
    --name "Outlook Auto Attach Server" \
    --add-data "outlook-attach-server.py:." \
    --hidden-import=tkinter \
    --hidden-import=json \
    --hidden-import=http.server \
    --hidden-import=subprocess \
    --hidden-import=platform \
    --hidden-import=shutil \
    --hidden-import=tempfile \
    --hidden-import=datetime \
    --hidden-import=socket \
    --hidden-import=threading \
    --hidden-import=importlib.util \
    --hidden-import=win32com.client \
    --clean \
    outlook-attach-launcher.py

# Make executable
chmod +x "dist/Outlook Auto Attach Server"

echo ""
echo "✅ Build complete!"
echo "📦 Executable: dist/Outlook Auto Attach Server"
echo ""
echo "💡 To create a .app bundle, you can move it to /Applications or"
echo "   use 'open -a "Outlook Auto Attach Server"'"

