# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_all

datas = [
    ('status_logo.png', '.'),
    ('assets/aim-flow.icns', '.'),
]
binaries = []
hiddenimports = ['AppKit', 'Foundation']
hiddenimports += collect_submodules('aim_flow')

tmp_ret = collect_all('whisper')
datas    += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

a = Analysis(
    ['launch_aim_flow.py'],
    pathex=['src'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='AIM Flow',
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
    name='AIM Flow',
)
app = BUNDLE(
    coll,
    name='AIM Flow.app',
    icon='assets/aim-flow.icns',
    bundle_identifier='org.aims.aim-flow',
    info_plist={
        'CFBundleName': 'AIM Flow',
        'CFBundleDisplayName': 'AIM Flow',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleVersion': '0.1.0',
        'LSUIElement': True,
        'NSMicrophoneUsageDescription': (
            'AIM Flow needs microphone access to record your voice for speech-to-text.'
        ),
        'NSAppleEventsUsageDescription': (
            'AIM Flow needs accessibility access to paste transcribed text into the active field.'
        ),
        'NSAccessibilityUsageDescription': (
            'AIM Flow needs accessibility access for the global hotkey and auto-paste.'
        ),
    },
)
