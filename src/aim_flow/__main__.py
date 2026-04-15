"""CLI entrypoint for AIM Flow.

Routes to platform-specific app implementation:
- macOS: Full-featured menubar app with meeting summarizer
- Windows: System tray app with dictation only
- Linux: Dictation mode (meeting summarizer optional)
"""

from __future__ import annotations

import logging
import os
import sys
import tempfile

_LOCK_FILE = os.path.join(tempfile.gettempdir(), "aim-flow.lock")
_lock_handle = None  # kept alive so the lock is held for the process lifetime


def _acquire_single_instance_lock() -> bool:
    """Return True if this is the only running instance, False otherwise.
    
    Only used on macOS (Windows will handle single instance differently).
    """
    global _lock_handle
    if sys.platform != "darwin":
        # Only support single instance lock on macOS
        return True
    
    try:
        import fcntl
        _lock_handle = open(_LOCK_FILE, "w")
        fcntl.flock(_lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        # Another instance already holds the lock.
        if _lock_handle:
            _lock_handle.close()
            _lock_handle = None
        return False


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Quiet down noisy third-party loggers.
    logging.getLogger("whisper").setLevel(logging.WARNING)
    logging.getLogger("numba").setLevel(logging.WARNING)
    logging.getLogger("filelock").setLevel(logging.WARNING)


def main() -> int:
    """Launch platform-specific application."""
    _configure_logging()
    
    if sys.platform == "darwin":
        # macOS: Full-featured app with menubar and meeting summarizer
        logger = logging.getLogger(__name__)
        logger.info("Launching AIM Flow on macOS")
        
        if not _acquire_single_instance_lock():
            # Silently exit — another instance is already running in the menu bar.
            return 0
        
        from .app import AIMFlowApp
        app = AIMFlowApp()
        app.run()
        
    elif sys.platform == "win32":
        # Windows: Dictation-only with system tray
        logger = logging.getLogger(__name__)
        logger.info("Launching AIM Flow on Windows (dictation only)")
        
        try:
            from .windows_app import WindowsApp
            app = WindowsApp()
            app.run()
        except ImportError as e:
            logger.error(f"Failed to import Windows app: {e}")
            logger.error("Make sure pystray and Pillow are installed:")
            logger.error("  pip install pystray pillow")
            return 1
        except Exception as e:
            logger.error(f"Failed to start Windows app: {e}")
            return 1
        
    else:
        # Linux: Dictation mode (meeting summarizer optional)
        logger = logging.getLogger(__name__)
        logger.info("Launching AIM Flow on Linux")
        
        from .app import AIMFlowApp
        app = AIMFlowApp()
        app.run()
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
