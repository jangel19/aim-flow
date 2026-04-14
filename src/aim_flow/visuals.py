"""Status bar image rendering."""

from __future__ import annotations

import logging
import math
from pathlib import Path
from typing import Sequence

from AppKit import (
    NSBezierPath,
    NSColor,
    NSCompositingOperationSourceOver,
    NSImage,
    NSMakeRect,
    NSMakeSize,
    NSStatusBar,
)

from . import config

logger = logging.getLogger(__name__)


class StatusIconRenderer:
    """Builds crisp menu bar images for idle, recording, and processing states."""

    def __init__(self) -> None:
        self.base_logo = self._load_logo()

    def idle_image(self) -> NSImage:
        return self._composite_image(None, None)

    def recording_image(self, levels: Sequence[float]) -> NSImage:
        return self._composite_image(levels, None)

    def processing_image(self, phase: float) -> NSImage:
        return self._composite_image(None, phase)

    def apply_to_status_item(self, status_item, image: NSImage) -> None:
        """Set the image directly on the NSStatusItem (uses the same API rumps uses)."""
        try:
            status_item.setImage_(image)
            # Explicit width so the status item resizes for the waveform panel.
            status_item.setLength_(image.size().width + 10.0)
        except Exception as exc:
            logger.warning("Failed to set status item image: %s", exc)

    def _load_logo(self) -> NSImage:
        path = config.resource_path(config.STATUS_LOGO_NAME)
        image = NSImage.alloc().initWithContentsOfFile_(str(path))
        if image is None:
            raise FileNotFoundError(f"Unable to load status logo from {path}")
        image.setSize_(NSMakeSize(config.STATUS_ICON_WIDTH, config.STATUS_ICON_HEIGHT))
        return image

    def _composite_image(
        self,
        levels: Sequence[float] | None,
        processing_phase: float | None,
    ) -> NSImage:
        width = config.STATUS_ICON_WIDTH
        if levels is not None or processing_phase is not None:
            width += config.STATUS_ITEM_SPACING + config.STATUS_WAVE_WIDTH

        image = NSImage.alloc().initWithSize_(NSMakeSize(width, config.STATUS_ICON_HEIGHT))
        image.lockFocus()

        logo_rect = NSMakeRect(0.0, 0.0, config.STATUS_ICON_WIDTH, config.STATUS_ICON_HEIGHT)
        self.base_logo.drawInRect_fromRect_operation_fraction_(
            logo_rect,
            NSMakeRect(
                0.0,
                0.0,
                self.base_logo.size().width,
                self.base_logo.size().height,
            ),
            NSCompositingOperationSourceOver,
            1.0,
        )

        if levels is not None:
            self._draw_waveform(levels)
        elif processing_phase is not None:
            self._draw_processing_indicator(processing_phase)

        image.unlockFocus()
        image.setTemplate_(False)
        image.setSize_(NSMakeSize(width, config.STATUS_ICON_HEIGHT))
        return image

    def _draw_waveform(self, levels: Sequence[float]) -> None:
        start_x = config.STATUS_ICON_WIDTH + config.STATUS_ITEM_SPACING
        total_width = (
            config.WAVE_BAR_COUNT * config.WAVE_BAR_WIDTH
            + (config.WAVE_BAR_COUNT - 1) * config.WAVE_BAR_GAP
        )
        origin_x = start_x + max((config.STATUS_WAVE_WIDTH - total_width) / 2.0, 0.0)

        bar_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.08, 0.08, 0.1, 1.0)

        for index, level in enumerate(levels):
            height = config.WAVE_MIN_HEIGHT + level * (config.WAVE_MAX_HEIGHT - config.WAVE_MIN_HEIGHT)
            x = origin_x + index * (config.WAVE_BAR_WIDTH + config.WAVE_BAR_GAP)
            y = (config.STATUS_ICON_HEIGHT - height) / 2.0
            rect = NSMakeRect(x, y, config.WAVE_BAR_WIDTH, height)
            radius = config.WAVE_BAR_WIDTH / 2.0
            path = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(rect, radius, radius)
            bar_color.setFill()
            path.fill()

    def _draw_processing_indicator(self, phase: float) -> None:
        start_x = config.STATUS_ICON_WIDTH + config.STATUS_ITEM_SPACING
        alpha = 0.35 + 0.45 * (0.5 + 0.5 * math.sin(phase))
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.08, 0.08, 0.1, alpha)
        for offset in (0.0, 8.0, 16.0):
            rect = NSMakeRect(start_x + offset, 7.0, 4.0, 4.0)
            path = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(rect, 2.0, 2.0)
            color.setFill()
            path.fill()


def status_bar_height() -> float:
    return float(NSStatusBar.systemStatusBar().thickness())
