"""Global hotkey support via pynput (cross-platform)."""

from __future__ import annotations

import logging
import sys
import time
from typing import Callable

from pynput import keyboard

from . import config

logger = logging.getLogger(__name__)


class HotkeyManager:
    def __init__(self, callback: Callable[[], None]) -> None:
        self._callback = callback
        self._listener: keyboard.Listener | keyboard.GlobalHotKeys | None = None
        self._option_pressed = False
        self._command_pressed = False
        self._control_pressed = False
        self._alt_pressed = False
        self._space_pressed = False
        self._combo_active = False
        self._last_triggered_at = 0.0

    def _on_hotkey(self) -> None:
        logger.debug("Hotkey triggered: %s", config.DEFAULT_HOTKEY)
        try:
            self._callback()
        except Exception as exc:
            logger.error("Hotkey callback raised an exception: %s", exc, exc_info=True)

    def _canonical_key(self, key):
        if self._listener is not None and hasattr(self._listener, "canonical"):
            try:
                key = self._listener.canonical(key)
            except Exception:
                pass
        return key

    def _is_option_key(self, key) -> bool:
        return key in {keyboard.Key.alt, keyboard.Key.alt_r}

    def _is_command_key(self, key) -> bool:
        return key in {keyboard.Key.cmd, keyboard.Key.cmd_r}

    def _is_control_key(self, key) -> bool:
        return key in {keyboard.Key.ctrl, keyboard.Key.ctrl_r}

    def _is_space_key(self, key) -> bool:
        try:
            return key == keyboard.Key.space
        except Exception:
            return False

    def _trigger_once(self) -> None:
        now = time.monotonic()
        if now - self._last_triggered_at < 0.2:
            return
        self._last_triggered_at = now
        self._on_hotkey()

    def _on_press(self, key) -> None:
        key = self._canonical_key(key)
        if self._is_option_key(key):
            self._option_pressed = True
        elif self._is_command_key(key):
            self._command_pressed = True
        elif self._is_control_key(key):
            self._control_pressed = True
        elif self._is_alt_key(key):
            self._alt_pressed = True
        elif self._is_space_key(key):
            self._space_pressed = True

        # macOS: Option+Command
        if (
            config.IS_MACOS
            and self._option_pressed
            and self._command_pressed
            and not self._combo_active
        ):
            self._combo_active = True
            self._trigger_once()

        # Windows: Ctrl+Alt+Space
        if (
            sys.platform == "win32"
            and self._control_pressed
            and self._alt_pressed
            and self._space_pressed
            and not self._combo_active
        ):
            self._combo_active = True
            self._trigger_once()

    def _on_release(self, key) -> None:
        key = self._canonical_key(key)
        if self._is_option_key(key):
            self._option_pressed = False
        elif self._is_command_key(key):
            self._command_pressed = False
        elif self._is_control_key(key):
            self._control_pressed = False
        elif self._is_alt_key(key):
            self._alt_pressed = False
        elif self._is_space_key(key):
            self._space_pressed = False

        # Reset combo when any key is released
        if not (
            (self._option_pressed and self._command_pressed)
            or (self._control_pressed and self._alt_pressed and self._space_pressed)
        ):
            self._combo_active = False

    def _is_alt_key(self, key) -> bool:
        return key in {keyboard.Key.alt, keyboard.Key.alt_r}

    def start(self) -> None:
        try:
            if config.IS_MACOS:
                # macOS: Use custom listener for Option+Command
                self._listener = keyboard.Listener(
                    on_press=self._on_press,
                    on_release=self._on_release,
                )
                logger.info(
                    "Hotkey listener started (Option+Command). "
                    "If the hotkey does not respond, grant Accessibility and "
                    "Input Monitoring permissions in System Settings, then restart."
                )
            elif sys.platform == "win32":
                # Windows: Use custom listener for Ctrl+Alt+Space
                self._listener = keyboard.Listener(
                    on_press=self._on_press,
                    on_release=self._on_release,
                )
                logger.info("Hotkey listener started (Ctrl+Alt+Space)")
            else:
                # Linux: Use GlobalHotKeys
                self._listener = keyboard.GlobalHotKeys(
                    {config.PYNPUT_HOTKEY: self._on_hotkey}
                )
                logger.info(f"Hotkey listener started ({config.DEFAULT_HOTKEY})")

            self._listener.start()
        except Exception as exc:
            logger.error(
                "Failed to start hotkey listener: %s. "
                "Check permissions and try again.",
                exc,
            )

    def stop(self) -> None:
        try:
            if self._listener is not None:
                self._listener.stop()
                logger.info("Hotkey listener stopped")
        except Exception as exc:
            logger.warning("Error stopping hotkey listener: %s", exc)
