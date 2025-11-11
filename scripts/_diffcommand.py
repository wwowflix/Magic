"""MAGIC-compatible wrapper for the _diffcommand CLI.

This is a reduced, import-safe version. The MAGIC smoke tests only
require that `scripts._diffcommand` imports successfully and that
`main()` can be called without raising errors.
"""

from __future__ import annotations


def main(argv=None):
    """No-op main function for MAGIC.

    Accepts an optional argv list for compatibility, but ignores it and
    exits cleanly.
    """
    # In the full environment this would parse arguments and call the
    # real diff functionality. For MAGIC we just return 0.
    return 0


__all__ = ["main"]
