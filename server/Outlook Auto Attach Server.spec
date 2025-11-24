# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['outlook-attach-launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('outlook-attach-server.py', '.')],
    hiddenimports=['tkinter', 'json', 'http.server', 'subprocess', 'platform', 'shutil', 'tempfile', 'datetime', 'socket', 'threading', 'importlib.util', 'win32com.client'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Outlook Auto Attach Server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Outlook Auto Attach Server',
)
app = BUNDLE(
    coll,
    name='Outlook Auto Attach Server.app',
    icon=None,
    bundle_identifier=None,
)
