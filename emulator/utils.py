"""Utility helpers for the emulator."""

from __future__ import annotations

from typing import Dict


def to_hex(value: int, width: int = 8) -> str:
    """Return value formatted as hexadecimal."""
    return f"0x{value:0{width}X}"


def parse_number(text: str) -> int:
    """Parse a string into an int supporting hex (0x) and decimal."""
    text = text.strip()
    if text.startswith("0x"):
        return int(text, 16)
    return int(text, 10)
