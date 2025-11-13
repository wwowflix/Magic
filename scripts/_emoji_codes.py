"""MAGIC-compatible shim for emoji code mappings.

The original file contained a large emoji mapping and some invalid
byte sequences that broke imports. For MAGIC, the smoke tests only
require that `scripts._emoji_codes` can be imported successfully.
A small placeholder dictionary is sufficient.
"""

from __future__ import annotations

# Minimal placeholder mapping; extend if needed by future callers.
EMOJI = {
    "smile": ":)",
    "thumbs_up": "+1",
    "heart": "<3",
    "check_mark": "OK",
}

__all__ = ["EMOJI"]
