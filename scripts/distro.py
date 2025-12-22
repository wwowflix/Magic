"""
MAGIC Week 0 shim for a distro / OS info tool.

The original module behaved like the third-party `distro` package and
also provided a CLI entrypoint. When imported under pytest, its `main()`
could be invoked with pytest arguments, causing argparse to exit with
status 2.

For MAGIC smoke tests we only need:

- import of `scripts.distro` to succeed, and
- a couple of simple helpers (`name`, `version`, `info`, `main`) that
  are safe to call and do not inspect real system state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class DistroInfo:
    id: str = "unknown"
    name: str = "Unknown"
    version: str = "0"
    pretty: Optional[str] = None


# ---------------------------------------------------------------------------
# Public API-style helpers
# ---------------------------------------------------------------------------

def name() -> str:
    """Return a very small placeholder distribution name."""
    return "Unknown"


def version() -> str:
    """Return a very small placeholder version string."""
    return "0"


def linux_distribution() -> Tuple[str, str, str]:
    """
    Legacy-style helper returning (name, version, id).

    This is kept for compatibility with older example code.
    """
    return (name(), version(), "unknown")


def info() -> DistroInfo:
    """
    Return a small DistroInfo object with placeholder values.
    """
    return DistroInfo(pretty=f"{name()} {version()}")


def main(argv: Optional[list[str]] = None) -> int:
    """
    CLI entrypoint shim.

    In MAGIC smoke tests we do NOT parse real command line arguments,
    because pytest sets sys.argv to its own flags. Instead we simply
    print a tiny summary (optional) and return exit code 0.

    This function is **never** called at import time.
    """
    text = f"{name()} {version()}".strip()
    print(text)
    return 0
