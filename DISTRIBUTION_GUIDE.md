# Outlook Auto Attach - Distribution Guide

## Overview

This is a local application solution that consists of:
1. **Chrome Extension** - Detects file downloads and communicates with local server
2. **Server Application (GUI)** - Simple desktop app that users click to start/stop the server

## What Users Get

### For End Users:
- **Simple GUI Application** - Just double-click to run
- **Start/Stop Button** - Easy control
- **Status Display** - Shows if server is running
- **Activity Log** - See what's happening
- **No Terminal Required** - User-friendly interface

### For Administrators:
- Standalone executables (no Python installation needed)
- Easy distribution via ZIP package
- Works on Mac and Windows
- Auto-start capability (optional)

## Building the Distribution Package

### Step 1: Build Server Launcher

**For Mac:**
```bash
cd server
./build-launcher-mac.sh
```

This creates: `server/dist/Outlook Auto Attach Server`

**For Windows:**
```bash
cd server
build-launcher-windows.bat
```

This creates: `server/dist/Outlook Auto Attach Server.exe`

### Step 2: Build Chrome Extension

The extension files are already in `dist/extension/` or the root directory:
- `manifest.json`
- `background.js`
- `popup.html`
- `popup.js`
- `confirm.html`
- `icons/` folder

### Step 3: Create Distribution Package

```bash
./create-distribution-package.sh
```

This creates a ZIP file with:
```
outlook-auto-attach-package-1.0.1-YYYYMMDD-HHMMSS.zip
├── Chrome Extension/
│   ├── manifest.json
│   ├── background.js
│   ├── popup.html
│   ├── popup.js
│   ├── confirm.html
│   └── icons/
├── Server/
│   ├── Mac/
│   │   └── Outlook Auto Attach Server
│   └── Windows/
│       └── Outlook Auto Attach Server.exe
└── Documentation/
    ├── INSTALLATION.md
    └── README.txt
```

## User Installation

1. **Install Chrome Extension**
   - Open Chrome → `chrome://extensions/`
   - Enable Developer mode
   - Click "Load unpacked"
   - Select the `Chrome Extension` folder

2. **Start Server Application**
   - Mac: Double-click `Outlook Auto Attach Server` (in Server/Mac folder)
   - Windows: Double-click `Outlook Auto Attach Server.exe` (in Server/Windows folder)
   - Click "Start Server" button
   - Window can be minimized - server keeps running

## Optional: Auto-Start on Login

### Mac:
1. Move `Outlook Auto Attach Server` to `/Applications`
2. System Settings → Users & Groups → Login Items
3. Add "Outlook Auto Attach Server"

### Windows:
1. Press `Win + R`, type `shell:startup`, press Enter
2. Create shortcut to `Outlook Auto Attach Server.exe`
3. Move shortcut to Startup folder

## How It Works

1. User downloads a file containing "Orderbekräftelse", "Inköp", or "1000322"
2. Chrome extension detects the download
3. Extension shows notification and badge
4. User clicks extension icon to confirm
5. Extension sends file path to local server (localhost:8765)
6. Server opens Outlook and attaches the file
7. User can complete the email in Outlook

## Advantages of This Approach

✅ **User-Friendly** - Simple GUI application, no command line
✅ **Standalone** - No Python installation needed
✅ **Local** - All data stays on user's computer
✅ **Reliable** - Works with Outlook desktop app
✅ **Easy Distribution** - Single ZIP package

## Technical Details

- **Server Port**: 8765 (localhost only)
- **Platform**: macOS (AppleScript) and Windows (COM automation)
- **UI Framework**: tkinter (included with Python, bundled in executable)
- **Build Tool**: PyInstaller (creates standalone executables)

## Files Created

### Server Files:
- `server/outlook-attach-launcher.py` - GUI launcher application
- `server/build-launcher-mac.sh` - Build script for Mac
- `server/build-launcher-windows.bat` - Build script for Windows

### Distribution Files:
- `create-distribution-package.sh` - Creates complete ZIP package
- `DISTRIBUTION_GUIDE.md` - This file

## Next Steps

1. Build launchers for both platforms
2. Test on Mac and Windows
3. Create distribution package
4. Distribute to users
5. Collect feedback and iterate

