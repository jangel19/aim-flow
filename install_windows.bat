@echo off
REM AIM Flow - Windows Installation Script

echo.
echo ================================
echo AIM Flow - Windows Installation
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo.
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    echo Make sure to check "Add python.exe to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if ffmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: ffmpeg not found
    echo.
    echo ffmpeg is required for audio transcription.
    echo.
    echo Installation steps:
    echo 1. Download from: https://ffmpeg.org/download.html
    echo 2. Extract to: C:\ffmpeg
    echo 3. Add C:\ffmpeg\bin to your PATH
    echo 4. Restart this installer
    echo.
    pause
)

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo If PyAudio installation failed, try:
    echo 1. Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    echo 2. Install with: pip install PyAudio-0.2.13-cp311-cp311-win_amd64.whl
    echo.
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.
echo ================================
echo Installation Complete!
echo ================================
echo.
echo To run AIM Flow:
echo   1. Open Command Prompt in this folder
echo   2. Run: venv\Scripts\activate
echo   3. Run: python -m aim_flow
echo.
echo Hotkey: Ctrl+Alt+Space to start/stop recording
echo.
echo For more help, visit:
echo   https://github.com/jordiangel/aim-flow
echo.
pause
