
# AIM Flow

Free, open-source, fully local speech-to-text for macOS. No cloud, no API keys, no subscriptions.

AIM Flow lives in your menu bar. Press a hotkey, speak, and your words get typed automatically into whatever app you're using.

Built by Jordi Lopez for the Artificial Intelligence Multidisciplinary Society (AIM).

## How it works
1. The little AIMS "A" logo sits in your menu bar.
2. Press Ctrl + Shift + Space to start recording; you'll see a live waveform.
3. Press Ctrl + Shift + Space again to stop.
4. Whisper transcribes everything locally on your Mac.
5. The text is automatically pasted where you were typing.

## Requirements
- macOS 12 or later
- Python 3.11 or 3.12 (3.12 is best)
- [Homebrew](https://brew.sh)

## How to install and use it

### Step 1: Clone the repo
```bash
git clone https://github.com/jangel19/aim-flow.git
cd aim-flow
```

### Step 2: Run the installer
```bash
./install.sh
```
This installs ffmpeg and portaudio with Homebrew, sets up a virtual environment, and installs everything you need.

### Step 3: Build the app
```bash
./scripts/build_app.sh
```
This creates dist/AIM Flow.app.

### Step 4: Install the app
Move the app to your Applications folder:
```bash
cp -r "dist/AIM Flow.app" /Applications/
```
Or just drag dist/AIM Flow.app into /Applications using Finder.

### Step 5: Launch it
Open /Applications/AIM Flow.app. The A logo should appear in your menu bar.

### Step 6: Grant permissions (very important)
This is the most important step. Without these, the hotkey and paste will not work.

Go to System Settings → Privacy & Security and turn on these three permissions for AIM Flow:

| Permission          | Why it's needed                                      |
|---------------------|------------------------------------------------------|
| Accessibility       | Lets AIM Flow detect the global hotkey and paste text |
| Input Monitoring    | Lets AIM Flow listen for Ctrl+Shift+Space system-wide |
| Microphone          | Lets AIM Flow record your voice (macOS will usually prompt automatically) |

After turning on Accessibility and Input Monitoring, quit AIM Flow completely and launch it again. macOS only applies permission changes when the app restarts.

Tip: If AIM Flow doesn't show up in the Accessibility or Input Monitoring list, try using the hotkey or the "Toggle Recording" menu item once. macOS will add it to the list automatically.

## Quick usage
| Action                    | How                                              |
|---------------------------|--------------------------------------------------|
| Start recording           | Ctrl + Shift + Space                             |
| Stop recording and paste  | Ctrl + Shift + Space again                       |
| Toggle via menu           | Click the A logo → Toggle Recording              |
| Quit                      | Click the A logo → Quit                          |

The first time you use it, it will download the Whisper base model (about 140 MB). After that it runs instantly from cache.

## Run directly from source (no need to build)
```bash
./run.sh
```
If you run it this way, you'll need to give Accessibility and Input Monitoring permissions to your Terminal app (or whichever terminal app you use) instead of AIM Flow.

## Auto-start on login
Go to System Settings → General → Login Items, click the + button, and add /Applications/AIM Flow.app.

## Tech stack
- rumps (menu bar app)
- openai-whisper (local transcription)
- PyAudio (microphone)
- pynput (hotkey + paste)
- pyobjc (AppKit image rendering)
- PyInstaller (for the .app bundle)

## Troubleshooting

**Hotkey does nothing**  
1. Go to System Settings → Privacy & Security → Accessibility and make sure AIM Flow is toggled ON.  
2. Go to System Settings → Privacy & Security → Input Monitoring and make sure AIM Flow is toggled ON.  
3. Quit and relaunch AIM Flow after changing permissions.  
4. If you just reinstalled the app, macOS often revokes permissions; re-grant them.

**Text is transcribed but not pasted**  
Same as above: Accessibility permission is required for the paste. Make sure it's enabled and that you restarted AIM Flow.

**Multiple A icons appear in the menu bar**  
Only one instance should run at a time. Quit all of them and relaunch just once. Newer versions try to prevent this automatically.

**"ffmpeg not found" error**  
```bash
brew install ffmpeg
```

**Microphone access denied**  
Go to System Settings → Privacy & Security → Microphone and enable AIM Flow.

**Whisper model download is slow**  
The first run downloads the base model (about 140 MB). This only happens once.

**Permissions were granted but still not working after reinstall**  
macOS ties permissions to the specific app binary. Remove the old AIM Flow entry in Privacy & Security if it exists, relaunch the app, and grant the permissions again.

## Project layout
```
aim-flow/
├── launch_aim_flow.py      Convenience launcher
├── install.sh              One-command setup
├── run.sh                  Run from source
├── requirements.txt        Runtime dependencies
├── requirements-build.txt  PyInstaller (build only)
├── AIM Flow.spec           PyInstaller spec (icon + Info.plist)
├── status_logo.png         Menu bar icon source (18×18 PNG)
├── assets/
│   └── aim-flow.icns       Generated app bundle icon
├── scripts/
│   ├── build_app.sh        Build AIM Flow.app
│   └── create_icns.sh      Convert status_logo.png → .icns
└── src/aim_flow/
    ├── app.py              Menu bar app
    ├── audio.py            Microphone recording
    ├── automation.py       Clipboard + paste
    ├── config.py           Constants + resource path helper
    ├── hotkey.py           Global hotkey listener
    ├── permissions.py      Accessibility check + guidance dialog
    ├── transcription.py    Whisper engine
    └── visuals.py          Menu bar icon rendering
```

## License
MIT; see LICENSE.
```
