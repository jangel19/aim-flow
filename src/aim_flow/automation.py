"""Clipboard and paste helpers for macOS.

Paste is done via pynput's keyboard controller (Cmd+V), which only requires
Accessibility permission — no Automation / System Events needed.
"""

from __future__ import annotations

import logging
import subprocess
import time

from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

_keyboard = Controller()


def copy_to_clipboard(text: str) -> None:
    subprocess.run(["pbcopy"], input=text, text=True, check=True)
    logger.debug("Copied %d characters to clipboard", len(text))


def paste_active_field() -> None:
    # Small delay so the clipboard write settles before the keystroke fires.
    time.sleep(0.05)
    with _keyboard.pressed(Key.cmd):
        _keyboard.press("v")
        _keyboard.release("v")
    logger.debug("Paste keystroke sent via pynput (Cmd+V)")


def copy_and_paste(text: str) -> None:
    copy_to_clipboard(text)
    paste_active_field()
