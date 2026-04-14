from pathlib import Path

from setuptools import setup


APP = ["launch_aim_flow.py"]
DATA_FILES = [
    ("", ["status_logo.png"]),
    ("assets", [str(path) for path in Path("assets").glob("*.svg")]),
]
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "AIM Flow",
        "CFBundleDisplayName": "AIM Flow",
        "CFBundleIdentifier": "org.aims.aim-flow",
        "CFBundleShortVersionString": "0.1.0",
        "CFBundleVersion": "0.1.0",
        "LSUIElement": True,
        "NSMicrophoneUsageDescription": "AIM Flow needs microphone access for local speech transcription.",
    },
    "packages": ["aim_flow", "whisper", "rumps", "pynput", "numpy", "pyaudio"],
    "includes": ["AppKit", "Foundation"],
    "site_packages": True,
}


setup(
    app=APP,
    name="AIM Flow",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    package_dir={"": "src"},
    packages=["aim_flow"],
)
