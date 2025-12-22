"""
MAGIC – Week 0 stub for core_9.

Original module expected an `Abort` symbol from `scripts.exceptions`.
For Week 0 we do not need that behaviour; we just need a safe import.
"""


class AbortPlaceholder(Exception):
    """Minimal placeholder, in case anything checks for Abort-type errors."""
    pass


__all__ = ["AbortPlaceholder"]
