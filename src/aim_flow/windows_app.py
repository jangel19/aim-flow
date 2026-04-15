"""Windows system tray application for AIM Flow dictation.

Provides basic recording controls via system tray icon.
Windows-only module - not imported on other platforms.
"""

import os
import sys
import logging
import threading
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)


class WindowsApp:
    """Windows system tray app for dictation."""

    def __init__(self) -> None:
        self.is_recording = False
        self.audio_recorder: Optional[object] = None
        self.temp_audio_path: Optional[str] = None
        self.last_transcript = ""

        try:
            import pystray
            from pystray import MenuItem as Item
            from PIL import Image, ImageDraw

            self.pystray = pystray
            self.Item = Item
            self.Image = Image
            self.ImageDraw = ImageDraw

            # Create tray icon
            self.icon: Optional[object] = None
            self._create_icon()

            # Setup hotkey
            from .hotkey import HotkeyManager

            self.hotkey_manager = HotkeyManager(self.toggle_recording)

        except ImportError as e:
            logger.error(f"Required Windows dependencies not installed: {e}")
            logger.info("Install with: pip install pystray pillow")
            raise

    def _create_icon(self) -> None:
        """Create system tray icon."""

        def create_image(color: str):
            """Create a simple colored circle icon."""
            width = 64
            height = 64
            image = self.Image.new("RGB", (width, height), color="white")
            dc = self.ImageDraw.Draw(image)
            dc.ellipse((8, 8, width - 8, height - 8), fill=color, outline="black")
            return image

        # Create icon with menu
        self.icon = self.pystray.Icon(
            "AIM Flow",
            create_image("gray"),
            "AIM Flow - Ready",
            menu=self.pystray.Menu(
                self.Item(
                    "Toggle Recording (Ctrl+Alt+Space)", self.toggle_recording
                ),
                self.Item("Last Transcript", self.show_last_transcript, enabled=False),
                self.Item("Exit", self.quit_app),
            ),
        )

    def toggle_recording(self, icon=None, item=None) -> None:
        """Toggle recording on/off (called by hotkey or menu)."""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self) -> None:
        """Start audio recording."""
        try:
            from .audio import AudioRecorder

            fd, self.temp_audio_path = tempfile.mkstemp(
                suffix=".wav", prefix="aim_"
            )
            os.close(fd)

            self.audio_recorder = AudioRecorder()
            self.audio_recorder.start()

            self.is_recording = True
            self.icon.icon = self._create_recording_icon()
            self.icon.title = "AIM Flow - Recording..."
            logger.info("Recording started")

        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self._show_notification("Recording Failed", str(e))

    def _stop_recording(self) -> None:
        """Stop recording and transcribe."""
        if not self.is_recording:
            return

        try:
            # Stop audio capture
            self.audio_recorder.stop()
            self.audio_recorder.save(self.temp_audio_path)

            self.is_recording = False
            self.icon.icon = self._create_processing_icon()
            self.icon.title = "AIM Flow - Processing..."

            # Transcribe in background thread
            threading.Thread(target=self._process_audio, daemon=True).start()

        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            self._show_notification("Processing Failed", str(e))
            self._reset_ui()

    def _process_audio(self) -> None:
        """Transcribe audio and paste result."""
        try:
            from .transcription import process_transcription
            from .automation import copy_and_paste, open_ai_service

            # Transcribe with Whisper
            transcript = process_transcription(self.temp_audio_path)

            if not transcript:
                self._show_notification("Transcription Failed", "No speech detected")
                self._reset_ui()
                return

            self.last_transcript = transcript
            logger.info(f"Transcript: {transcript}")

            # Check for wake words
            transcript_lower = transcript.lower()
            if "claude" in transcript_lower and transcript_lower.startswith(
                ("hey claude", "hey ai", "hey")
            ):
                # Open Claude
                open_ai_service("claude", transcript)
                self._show_notification("Opening Claude", transcript[:50])
            elif "open" in transcript_lower or "chatgpt" in transcript_lower:
                # Open ChatGPT
                open_ai_service("chatgpt", transcript)
                self._show_notification("Opening ChatGPT", transcript[:50])
            elif "grok" in transcript_lower or transcript_lower.startswith("hey x"):
                # Open Grok
                open_ai_service("grok", transcript)
                self._show_notification("Opening Grok", transcript[:50])
            elif "gemini" in transcript_lower or "google" in transcript_lower:
                # Open Gemini
                open_ai_service("gemini", transcript)
                self._show_notification("Opening Gemini", transcript[:50])
            else:
                # Paste into active window
                copy_and_paste(transcript)
                self._show_notification("Text Pasted", transcript[:50])

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            self._show_notification("Error", str(e))
        finally:
            # Cleanup
            if self.temp_audio_path and os.path.exists(self.temp_audio_path):
                try:
                    os.remove(self.temp_audio_path)
                except Exception:
                    pass
            self._reset_ui()

    def _reset_ui(self) -> None:
        """Reset icon to idle state."""
        self.icon.icon = self._create_idle_icon()
        self.icon.title = "AIM Flow - Ready"

    def _create_idle_icon(self):
        """Create gray idle icon."""
        return self._create_colored_icon("gray")

    def _create_recording_icon(self):
        """Create red recording icon."""
        return self._create_colored_icon("red")

    def _create_processing_icon(self):
        """Create blue processing icon."""
        return self._create_colored_icon("blue")

    def _create_colored_icon(self, color: str):
        """Create a simple colored circle icon."""
        width = 64
        height = 64
        image = self.Image.new("RGB", (width, height), color="white")
        dc = self.ImageDraw.Draw(image)
        dc.ellipse((8, 8, width - 8, height - 8), fill=color, outline="black")
        return image

    def _show_notification(self, title: str, message: str) -> None:
        """Show Windows notification."""
        try:
            self.icon.notify(message, title)
        except Exception as e:
            logger.warning(f"Could not show notification: {e}")

    def show_last_transcript(self, icon=None, item=None) -> None:
        """Show last transcript in message box."""
        if self.last_transcript:
            try:
                import tkinter as tk
                from tkinter import messagebox

                root = tk.Tk()
                root.withdraw()  # Hide main window
                messagebox.showinfo("Last Transcript", self.last_transcript)
                root.destroy()
            except Exception as e:
                logger.error(f"Could not show transcript dialog: {e}")
                self._show_notification("Error", "Could not show transcript")
        else:
            self._show_notification("No Transcript", "Record something first")

    def quit_app(self, icon=None, item=None) -> None:
        """Exit application."""
        logger.info("Quitting AIM Flow")
        if hasattr(self, "hotkey_manager"):
            self.hotkey_manager.stop()
        icon.stop()

    def run(self) -> None:
        """Start the application."""
        logger.info("Starting AIM Flow (Windows mode)")

        # Start hotkey listener
        self.hotkey_manager.start()

        # Run system tray (blocking)
        self.icon.run()


def main() -> None:
    """Entry point for Windows app."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    app = WindowsApp()
    app.run()


if __name__ == "__main__":
    main()
