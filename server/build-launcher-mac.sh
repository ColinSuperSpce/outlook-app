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

# Check if .app bundle was created
if [ -d "dist/Outlook Auto Attach Server.app" ]; then
    APP_PATH="dist/Outlook Auto Attach Server.app"
    echo "📱 Found .app bundle, signing and removing quarantine..."
    
    # Remove quarantine attribute (allows app to open without warning)
    xattr -cr "$APP_PATH" 2>/dev/null || true
    
    # Sign with ad-hoc signature (allows app to run)
    codesign --force --deep --sign - "$APP_PATH" 2>/dev/null || {
        echo "⚠️  Warning: Could not code sign app (may need to run 'xattr -cr' manually)"
    }
    
    echo "✅ Build complete!"
    echo "📦 App bundle: $APP_PATH"
elif [ -f "dist/Outlook Auto Attach Server" ]; then
    chmod +x "dist/Outlook Auto Attach Server"
    echo "✅ Build complete!"
    echo "📦 Executable: dist/Outlook Auto Attach Server"
else
    echo "❌ Error: Could not find built app!"
    exit 1
fi

