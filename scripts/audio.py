from __future__ import annotations

"""
MAGIC stub: lightweight replacement for the audio helper.

The original module expected a beep.wav asset under scripts/data/beep.wav
and tried to load it at import time. In MAGIC we want imports to be safe
even if that asset is missing, and we only need a tiny stub so tests can
import the module and call a simple function.
"""

from typing import Optional
import os


# Directory where audio assets would live in a real setup
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _read_wave_file(filepath: str) -> bytes:
    """
    Very small helper that tries to read a wave file as raw bytes.

    If the file is missing (common in MAGIC dev environment), we return
    an empty bytes object instead of raising FileNotFoundError.
    """
    try:
        with open(filepath, "rb") as f:
            return f.read()
    except FileNotFoundError:
        # MAGIC: Missing asset is acceptable in tests.
        return b""


# Try to load a built-in beep asset if present; otherwise this will be b"".
BEEP: bytes = _read_wave_file(os.path.join(DATA_DIR, "beep.wav"))


def play_beep() -> None:
    """
    Stub function used by tests.

    In real code this would send BEEP to an audio playback device.
    For MAGIC smoke tests, it is enough that this function exists and
    does nothing (or at most performs a cheap check).
    """
    # Do nothing; if you like, you could log or print, but silence is fine.
    return


def has_beep_asset() -> bool:
    """
    Convenience helper for tests or diagnostics: returns True if a non-empty
    beep payload was loaded, False otherwise.
    """
    return bool(BEEP)
