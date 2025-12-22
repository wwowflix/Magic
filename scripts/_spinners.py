"""MAGIC shim for terminal spinners.

Original file had many Unicode frames and got corrupted.
We only need imports to succeed.
"""

from __future__ import annotations

SPINNERS = {
    "line": {"interval": 100, "frames": ["-", "\\", "|", "/"]},
}
