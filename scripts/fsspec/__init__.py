from __future__ import annotations

"""
MAGIC Week 0 stub for the `fsspec` package.

Goal:
- Make `from fsspec.asyn import AbstractAsyncStreamedFile, AsyncFileSystem, sync, sync_wrapper`
  work without pulling real fsspec.
- Mark this as a REAL package (via __path__) so `fsspec.asyn` can be imported.
"""

from pathlib import Path

# Mark this module as a package so Python can find submodules under fsspec.*
__path__ = [str(Path(__file__).parent)]

# Import our local asyn stub so it is available as fsspec.asyn
try:
    from . import asyn  # noqa: F401
except Exception:
    asyn = None  # type: ignore[assignment]

__all__ = ["asyn"]
