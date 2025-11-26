#!/bin/bash
# Create distribution package with extension and server launcher

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

PACKAGE_NAME="outlook-auto-attach-package"
VERSION="1.0.1"
DIST_DIR="dist-package"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "📦 Creating distribution package..."
echo ""

# Clean previous package
rm -rf "$DIST_DIR"
rm -f "${PACKAGE_NAME}-*.zip"

# Create package structure
mkdir -p "$DIST_DIR/Chrome Extension"
mkdir -p "$DIST_DIR/Server/Mac"
mkdir -p "$DIST_DIR/Server/Windows"

# Copy Chrome extension
echo "📁 Copying Chrome extension..."
if [ -d "dist/extension" ]; then
    cp -r dist/extension/* "$DIST_DIR/Chrome Extension/"
else
    # Fallback to main directory
    cp manifest.json background.js popup.html popup.js confirm.html "$DIST_DIR/Chrome Extension/" 2>/dev/null || true
    cp -r icons "$DIST_DIR/Chrome Extension/" 2>/dev/null || true
fi

# Copy server launcher (Mac) - use .app bundle
echo "🍎 Copying Mac server launcher..."
if [ -d "server/dist/Outlook Auto Attach Server.app" ]; then
    cp -R "server/dist/Outlook Auto Attach Server.app" "$DIST_DIR/Server/Mac/"
    chmod -R +x "$DIST_DIR/Server/Mac/Outlook Auto Attach Server.app"
    echo "   ✅ Copied .app bundle"
elif [ -f "server/dist/Outlook Auto Attach Server" ]; then
    cp "server/dist/Outlook Auto Attach Server" "$DIST_DIR/Server/Mac/"
    chmod +x "$DIST_DIR/Server/Mac/Outlook Auto Attach Server"
elif [ -f "dist/server/outlook-attach-server" ]; then
    cp "dist/server/outlook-attach-server" "$DIST_DIR/Server/Mac/outlook-attach-server"
    chmod +x "$DIST_DIR/Server/Mac/outlook-attach-server"
fi

# Copy server launcher (Windows)
echo "🪟 Copying Windows server launcher..."
if [ -f "server/dist/Outlook Auto Attach Server.exe" ]; then
    cp "server/dist/Outlook Auto Attach Server.exe" "$DIST_DIR/Server/Windows/"
elif [ -f "dist/server/outlook-attach-server.exe" ]; then
    cp "dist/server/outlook-attach-server.exe" "$DIST_DIR/Server/Windows/"
fi

# Create ZIP package
echo ""
echo "📦 Creating ZIP package..."
cd "$DIST_DIR"
zip -r "../${PACKAGE_NAME}-${VERSION}-${TIMESTAMP}.zip" . -x "*.DS_Store" "*.git*"
cd ..

# Cleanup
rm -rf "$DIST_DIR"

echo ""
echo "✅ Package created successfully!"
echo "📦 Package: ${PACKAGE_NAME}-${VERSION}-${TIMESTAMP}.zip"
echo ""
echo "📋 Package contents:"
echo "   - Chrome Extension folder"
echo "   - Server/Mac folder (with executable)"
echo "   - Server/Windows folder (with executable)"
echo ""

