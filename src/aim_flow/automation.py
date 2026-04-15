"""Cross-platform clipboard and paste helpers.

macOS: Uses pbcopy and Cmd+V keystroke via pynput.
Windows: Uses pyperclip for clipboard and Ctrl+V keystroke.
Linux: Uses xclip/xsel for clipboard and Ctrl+V.
"""

from __future__ import annotations

import logging
import subprocess
import sys
import time

from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

_keyboard = Controller()


def copy_to_clipboard(text: str) -> None:
    """Copy text to clipboard (cross-platform)."""
    if sys.platform == "darwin":  # macOS
        subprocess.run(["pbcopy"], input=text, text=True, check=True)
        logger.debug("Copied %d characters to clipboard (macOS pbcopy)", len(text))
    elif sys.platform == "win32":  # Windows
        _copy_to_clipboard_windows(text)
    else:  # Linux
        _copy_to_clipboard_linux(text)


def _copy_to_clipboard_windows(text: str) -> None:
    """Copy to clipboard on Windows using pyperclip."""
    try:
        import pyperclip

        pyperclip.copy(text)
        logger.debug("Copied %d characters to clipboard (Windows pyperclip)", len(text))
    except ImportError:
        logger.error("pyperclip not installed - cannot copy to clipboard on Windows")
    except Exception as e:
        logger.error(f"Failed to copy to clipboard on Windows: {e}")


def _copy_to_clipboard_linux(text: str) -> None:
    """Copy to clipboard on Linux using xclip or xsel."""
    try:
        # Try xclip first
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text,
            text=True,
            check=True,
        )
        logger.debug("Copied %d characters to clipboard (Linux xclip)", len(text))
    except FileNotFoundError:
        try:
            # Fall back to xsel
            subprocess.run(
                ["xsel", "--clipboard", "--input"],
                input=text,
                text=True,
                check=True,
            )
            logger.debug("Copied %d characters to clipboard (Linux xsel)", len(text))
        except FileNotFoundError:
            logger.error("Neither xclip nor xsel found - cannot copy to clipboard")
        except Exception as e:
            logger.error(f"Failed to copy to clipboard on Linux: {e}")
    except Exception as e:
        logger.error(f"Failed to copy to clipboard on Linux: {e}")


def paste_active_field() -> None:
    """Paste from clipboard into active window (cross-platform)."""
    if sys.platform == "darwin":  # macOS
        # Small delay so the clipboard write settles before the keystroke fires.
        time.sleep(0.05)
        with _keyboard.pressed(Key.cmd):
            _keyboard.press("v")
            _keyboard.release("v")
        logger.debug("Paste keystroke sent via pynput (Cmd+V)")
    elif sys.platform == "win32":  # Windows
        _paste_windows()
    else:  # Linux
        _paste_linux()


def _paste_windows() -> None:
    """Paste on Windows using keyboard simulation."""
    try:
        time.sleep(0.1)  # Delay to ensure clipboard is ready
        with _keyboard.pressed(Key.ctrl):
            _keyboard.press("v")
            _keyboard.release("v")
        logger.debug("Paste keystroke sent via pynput (Ctrl+V)")
    except Exception as e:
        logger.error(f"Failed to paste on Windows: {e}")


def _paste_linux() -> None:
    """Paste on Linux using xdotool."""
    try:
        time.sleep(0.05)
        subprocess.run(["xdotool", "key", "ctrl+v"], check=True)
        logger.debug("Paste keystroke sent via xdotool (Ctrl+V)")
    except FileNotFoundError:
        logger.error("xdotool not installed - cannot paste on Linux")
        logger.info("Install with: sudo apt install xdotool")
    except Exception as e:
        logger.error(f"Failed to paste on Linux: {e}")


def copy_and_paste(text: str) -> None:
    copy_to_clipboard(text)
    paste_active_field()


_SERVICE_URLS: dict[str, str] = {
    "claude": "https://claude.ai/new",
    "chatgpt": "https://chatgpt.com/",
    "grok": "https://grok.com/",
    "gemini": "https://gemini.google.com/",
}


def open_ai_service(service: str, query: str) -> None:
    """Open an AI service in the default browser.

    For Claude, the query is passed as a URL parameter.
    For all other services, the browser is opened and the query is
    auto-pasted after a short delay once the page has loaded.

    Args:
        service: One of 'claude', 'chatgpt', 'grok', 'gemini'.
        query: The text to send. May be empty.
    """
    import threading
    import webbrowser
    from urllib.parse import quote

    base_url = _SERVICE_URLS.get(service, "https://claude.ai/new")

    if service == "claude" and query:
        webbrowser.open(f"{base_url}?q={quote(query)}")
    else:
        webbrowser.open(base_url)
        if query:
            copy_to_clipboard(query)

            def _delayed_paste() -> None:
                time.sleep(3.5)
                paste_active_field()

            threading.Thread(target=_delayed_paste, daemon=True).start()

    logger.debug("Opened %s with query (%d chars)", service, len(query))
