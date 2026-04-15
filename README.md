# AIM Flow

Free, open-source, fully local speech-to-text for macOS, Windows, and Linux — no cloud, no API keys, no subscription.

AIM Flow lives in your menu bar (macOS/Linux) or system tray (Windows). Press a hotkey, speak, and the transcribed text is automatically pasted into whatever field you were typing in.

Created by Jordi Lopez for the [Artificial Intelligence Multidisciplinary Society (AIMS)](https://github.com/jangel19).

---

## Platform Support

| Feature | macOS | Windows | Linux |
|---------|-------|---------|-------|
| Dictation (voice-to-text) | ✅ | ✅ | ✅ |
| Auto-paste into active window | ✅ | ✅ | ✅ |
| Wake-word routing (Claude/ChatGPT/Grok/Gemini) | ✅ | ✅ | ✅ |
| Meeting summarizer (Ollama) | ✅ | ❌ | ✅ |
| Menu bar UI | ✅ | ❌ (System tray) | ✅ |
| Local Whisper transcription | ✅ | ✅ | ✅ |

---

## How it works

1. The AIMS "A" logo sits in your menu bar (macOS/Linux) or system tray (Windows).
2. Press the hotkey to start recording — the logo shows a live waveform (macOS only).
3. Press the hotkey again to stop.
4. Whisper transcribes your audio locally on your machine with the `base` model by default.
5. The text is automatically pasted into the active field.

The app applies lightweight voice-focused cleanup before transcription to reduce steady background noise and trailing silence. For best results on macOS, also enable the system microphone's Voice Isolation mode when available.

---

## Requirements

### macOS
- macOS 12 or later
- Python 3.11 or 3.12 (3.12 recommended)
- [Homebrew](https://brew.sh)

### Windows
- Windows 10 or later
- Python 3.9 or 3.12
- ffmpeg (download and add to PATH)

### Linux
- Python 3.9 or later
- ffmpeg (`sudo apt install ffmpeg`)

---

## Installation

### macOS

#### Step 1 — Clone and install

```bash
git clone https://github.com/jangel19/aim-flow.git
cd aim-flow
./install.sh
```

This installs `ffmpeg` and `portaudio` via Homebrew, creates a Python virtual environment, installs all dependencies, and generates the app icon.

#### Step 2 — Build the app

```bash
./scripts/build_app.sh
```

This creates `dist/AIM Flow.app`.

#### Step 3 — Move to Applications

```bash
cp -r "dist/AIM Flow.app" /Applications/
```

Or drag `dist/AIM Flow.app` to your `/Applications` folder in Finder.

#### Step 4 — Launch AIM Flow

Open `/Applications/AIM Flow.app`. The AIMS "A" logo will appear in your menu bar.

#### Step 5 — Grant permissions (one-time setup)

This is the most important step. Without these, the hotkey and paste will not work.

Open **System Settings → Privacy & Security** and enable the following for **AIM Flow**:

| Permission | Where to find it | Why it's needed |
|---|---|---|
| **Accessibility** | Privacy & Security → Accessibility | Lets AIM Flow detect the global hotkey and paste text |
| **Input Monitoring** | Privacy & Security → Input Monitoring | Lets AIM Flow listen for `Option+Command` system-wide |
| **Microphone** | Privacy & Security → Microphone | Lets AIM Flow record your voice (macOS will prompt automatically) |

**After enabling both Accessibility and Input Monitoring, quit and relaunch AIM Flow.** macOS does not apply permission changes to a running process.

> Tip: If AIM Flow does not appear in the Accessibility or Input Monitoring list, try using the hotkey or the "Toggle Recording" menu item once — macOS will add it to the list automatically.

### Windows

#### Prerequisites

1. **Install Python 3.9+** from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add python.exe to PATH" during installation
   - ✅ Choose "Install for all users" (recommended)

2. **Install ffmpeg**
   - Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to your system PATH:
     1. Open **System Properties** (Win+Pause or Settings → About → Advanced system settings)
     2. Click **Environment Variables**
     3. Under "System variables", click **Path** → Edit
     4. Click **New** and add: `C:\ffmpeg\bin`
     5. Click OK and restart your terminal

#### Installation Steps

1. **Clone the repository**
   ```cmd
   git clone https://github.com/jangel19/aim-flow.git
   cd aim-flow
   ```

2. **Run the installer**
   ```cmd
   install_windows.bat
   ```
   
   This will:
   - Create a Python virtual environment
   - Install all dependencies (Whisper, pynput, pystray, etc.)
   - Check for ffmpeg

3. **Done!** The installer will show how to run AIM Flow.

#### Troubleshooting Windows Installation

**"Python not found"**
- Reinstall Python from python.org with "Add python.exe to PATH" checked
- Restart your terminal after installation

**"ffmpeg not found"**
- Download from ffmpeg.org/download.html
- Extract to C:\ffmpeg
- Add C:\ffmpeg\bin to system PATH
- Restart your terminal

**"PyAudio installation failed"**
- Option 1: Install from pre-built wheel:
  ```cmd
  pip install https://files.pythonhosted.org/packages/PyAudio/PyAudio-0.2.13-cp311-cp311-win_amd64.whl
  ```
- Option 2: Use a different Python version (3.9 or 3.10)

---

## Usage

### macOS

| Action | How |
|---|---|
| Start recording | `Option+Command` |
| Stop recording and paste | `Option+Command` again |
| Toggle via menu | Click the A logo → Toggle Recording |
| Start meeting recording | Click the A logo → Start Meeting Recording |
| Stop meeting recording | Click the A logo → Stop Meeting Recording |
| View meeting history | Click the A logo → View Meeting History |
| Quit | Click the A logo → Quit |

### Windows

| Action | How |
|---|---|
| Start recording | `Ctrl+Alt+Space` |
| Stop recording and paste | `Ctrl+Alt+Space` again |
| Toggle via system tray | Right-click tray icon → Toggle Recording |
| View last transcript | Right-click tray icon → Last Transcript |
| Quit | Right-click tray icon → Exit |

### Linux

| Action | How |
|---|---|
| Start recording | `Ctrl+Shift+Space` |
| Stop recording and paste | `Ctrl+Shift+Space` again |
| Toggle via menu | Click the A logo → Toggle Recording |
| Start meeting recording | Click the A logo → Start Meeting Recording |
| Stop meeting recording | Click the A logo → Stop Meeting Recording |
| Quit | Click the A logo → Quit |

---

## Whisper Model Selection

The Whisper model (`base`) is downloaded automatically on first use (~140 MB). Subsequent runs load it from cache.

To use a different model, set the environment variable before launching:

**macOS/Linux:**
```bash
export AIM_FLOW_MODEL=small  # or: base, medium, large, turbo
./run.sh
```

**Windows:**
```cmd
set AIM_FLOW_MODEL=small
python -m aim_flow
```

Available models (by size and accuracy):
- `tiny` — Smallest, fastest (39 MB)
- `base` — Default (140 MB) ⭐
- `small` — Better accuracy (466 MB)
- `medium` — High accuracy (1.5 GB)
- `large` — Highest accuracy (2.9 GB)
- `turbo` — Latest model (809 MB)

---

## AI Assistant Integration

Start your recording with a wake word and AIM Flow will open the corresponding AI service in your browser instead of pasting text.

| Say... | Opens |
|---|---|
| `Hey Claude, [your question]` | Claude |
| `Hey Open, [your question]` | ChatGPT |
| `Hey X, [your question]` | Grok |
| `Hey Google, [your question]` | Gemini |

Your question is copied to the clipboard automatically — just paste if the service doesn't pre-fill it. Without a wake word, text pastes normally.

---

## Meeting Summarizer (macOS and Linux only)

AIM Flow can record long-form meetings and generate structured summaries using local AI.

### Requirements
1. Install [Ollama](https://ollama.com/download)
2. Pull Llama 3.2 model:
    ```bash
    ollama pull llama3.2:3b
    ```

### Usage
1. Click **Start Meeting Recording** in the menu bar
2. Meeting audio is recorded continuously
3. Click **Stop Meeting Recording** when done
4. AIM Flow transcribes with Whisper and summarizes with Llama 3.2
5. The summary opens automatically in Markdown format

### Output
Summaries are saved to `~/Documents/AIM_Flow_Meetings/` with:
- Key decisions
- Discussion topics
- Action items
- Next steps
- Full transcript

**Note**: If Ollama is not running, AIM Flow saves a transcript-only Markdown file as a fallback.

---

## Run from source (no build required)

**macOS**
```bash
./run.sh
```
Grant Accessibility and Input Monitoring to **Terminal** (or whichever terminal app you use) instead of AIM Flow.

**Windows**
```cmd
venv\Scripts\activate
python -m aim_flow
```

**Linux**
```bash
./run.sh
```

---

## Auto-start on login

**macOS** — **System Settings → General → Login Items → +** and add `/Applications/AIM Flow.app`.

**Windows** — Add `python -m aim_flow` to Windows Startup folder (`C:\Users\YourUsername\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`) or create a shortcut there.

---

## Tech stack

**Cross-platform**
- [openai-whisper](https://github.com/openai/whisper) — local speech recognition
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) — microphone capture
- [pynput](https://github.com/moses-palmer/pynput) — global hotkey and paste
- [pyperclip](https://github.com/asweigart/pyperclip) — clipboard access

**macOS only**
- [rumps](https://github.com/jaredks/rumps) — menu bar framework
- [pyobjc](https://pyobjc.readthedocs.io) — AppKit image rendering
- [PyInstaller](https://pyinstaller.org) — .app bundle packaging

**Windows only**
- [pystray](https://github.com/moses-palmer/pystray) — system tray framework
- [Pillow](https://github.com/python-pillow/Pillow) — icon rendering

## Troubleshooting

### macOS: Hotkey does nothing

1. Go to **System Settings → Privacy & Security → Accessibility** and confirm AIM Flow is toggled ON.
2. Go to **System Settings → Privacy & Security → Input Monitoring** and confirm AIM Flow is toggled ON.
3. Quit and relaunch AIM Flow after changing permissions.
4. If you just reinstalled the app, macOS revokes permissions on replacement — re-grant them.

### macOS: Text is transcribed but not pasted

Same fix as above — Accessibility permission is required for the paste keystroke. Make sure it is enabled and that you restarted AIM Flow after enabling it.

### macOS: Multiple A icons appear in the menu bar

Only one instance of AIM Flow can run at a time. If you see duplicates, quit all of them (click each → Quit) and relaunch once. This is prevented automatically in newer versions.

### Windows: Hotkey not working

**Ctrl+Alt+Space** might conflict with another application. Check:
- Windows settings for global hotkeys
- Other installed applications
- Try running as Administrator if conflicts persist

### Windows: Text pastes as garbage

- Check that your text input field supports clipboard pasting (Ctrl+V)
- Some applications (games, legacy software) may not support clipboard paste
- Try pasting manually (Ctrl+V) to test clipboard

### Windows: System tray icon missing

- Check if AIM Flow is actually running (open Task Manager → Processes)
- Try restarting Windows
- Try running as Administrator

### Windows: pystray install fails

If you see errors about pystray:
```cmd
pip install --upgrade pystray pillow
```

Then restart your terminal and try again.

### All platforms: "ffmpeg not found" error

**macOS**
```bash
brew install ffmpeg
```

**Windows**
- Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Extract to `C:\ffmpeg`
- Add `C:\ffmpeg\bin` to system PATH
- Restart terminal

**Linux**
```bash
sudo apt-get install ffmpeg
```

### All platforms: Microphone access denied

**macOS** — **System Settings → Privacy & Security → Microphone** → enable AIM Flow.

**Windows** — Settings → Privacy & security → Microphone → enable AIM Flow.

**Linux** — Grant microphone access to PulseAudio or ALSA.

### All platforms: Whisper model download is slow

The first run downloads the `base` Whisper model (~140 MB). This only happens once. Subsequent launches are instant.

### macOS: Permissions were granted but still not working after reinstall

macOS ties permissions to the specific app binary. Every time you replace the `.app`, you need to re-grant Accessibility and Input Monitoring. Go to System Settings, remove the old AIM Flow entry if present, relaunch the app, and re-add it.

### Python version issues

**macOS**
```bash
brew install python@3.12
```

**Windows** — Reinstall Python from python.org with "Add python.exe to PATH" checked.

## Project layout

```
aim-flow/                         macOS application
├── launch_aim_flow.py            Convenience launcher
├── install.sh                    One-command setup (Homebrew)
├── run.sh                        Run from source
├── requirements.txt              Runtime dependencies
├── requirements-build.txt        PyInstaller (build only)
├── AIM Flow.spec                 PyInstaller spec (icon + Info.plist)
├── status_logo.png               Menu bar icon source (18×18 PNG)
├── assets/
│   └── aim-flow.icns             Generated app bundle icon
├── scripts/
│   ├── build_app.sh              Build AIM Flow.app
│   └── create_icns.sh            Convert status_logo.png → .icns
└── src/aim_flow/
    ├── app.py                    Menu bar app (macOS)
    ├── audio.py                  Microphone recording
    ├── automation.py             Clipboard + paste
    ├── config.py                 Constants + resource path helper
    ├── hotkey.py                 Global hotkey listener
    ├── permissions.py            Accessibility check + guidance dialog
    ├── transcription.py          Whisper engine
    └── visuals.py                Menu bar icon rendering (macOS/AppKit)

aim-flow-linux/                   Linux application (linux branch)
├── launch_aim_flow_linux.py      Convenience launcher
├── install_linux.sh              One-command setup (apt-get)
├── run_linux.sh                  Run from source
├── requirements_linux.txt        Runtime dependencies
└── src/aim_flow/
    ├── app_linux.py              System tray app (pystray)
    ├── audio.py                  Microphone recording (shared)
    ├── automation.py             Clipboard + paste (X11/Wayland)
    ├── config.py                 Constants + resource path helper
    ├── hotkey.py                 Global hotkey listener
    ├── transcription.py          Whisper engine (shared)
    └── visuals_linux.py          Tray icon rendering (Pillow)
```

---

## License

MIT — see [LICENSE](LICENSE).
