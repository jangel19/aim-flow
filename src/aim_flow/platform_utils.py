"""Platform detection and OS-specific utilities."""

import sys
import platform


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def get_platform_name() -> str:
    """Get human-readable platform name."""
    if is_macos():
        return "macOS"
    elif is_linux():
        return "Linux"
    elif is_windows():
        return "Windows"
    else:
        return "Unknown"
