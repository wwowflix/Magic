"""MAGIC shim for async tempfile helpers."""

from __future__ import annotations

import tempfile
from typing import IO


def temporary_file() -> IO[bytes]:
    """Return a basic NamedTemporaryFile for tests."""
    return tempfile.NamedTemporaryFile()
