"""MAGIC-compatible compatibility helpers.

Minimal shim; only defines pieces needed by MAGIC smoke tests.
"""

from __future__ import annotations

import io


class _NonClosingTextIOWrapper(io.TextIOWrapper):
    """TextIOWrapper that does not close the underlying buffer.

    The original implementation (in click / attrs-style code) uses this to wrap
    stdio streams on Windows. For MAGIC tests we just need something that:
    - behaves like TextIOWrapper, and
    - does NOT actually close the underlying buffer when .close() is called.
    """

    def close(self):
        try:
            self.flush()
        except Exception:
            # Ignore flush errors, this is just a safety wrapper.
            pass
        # IMPORTANT: do NOT call super().close()
        # so the underlying buffer (e.g. sys.stdout.buffer) stays open.
        # This matches the intent of a "non-closing" wrapper.


__all__ = ["_NonClosingTextIOWrapper"]

# ---- MAGIC shim: Protocol ----
try:
    from typing import Protocol  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    class Protocol(object):  # minimal fallback for runtime checks
        pass
# ---- end MAGIC shim: Protocol ----
