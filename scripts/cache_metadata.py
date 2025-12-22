from __future__ import annotations

"""
MAGIC stub: replacement for cache_metadata using a local atomic_write.

The original module imported `atomic_write` from `fsspec.utils`. In MAGIC,
we keep things simple:

- provide our own atomic_write context manager
- add tiny helpers to load/save a pickled metadata dict

This is enough for smoke tests and basic usage.
"""

import contextlib
import os
import pickle
from typing import Any, Dict, Optional


@contextlib.contextmanager
def atomic_write(path: str, mode: str = "wb"):
    """
    Minimal atomic write helper:

    - writes to <path>.tmp
    - fsyncs
    - replaces the final file on success
    """
    tmp_path = f"{path}.tmp"
    f = open(tmp_path, mode)
    try:
        yield f
        f.flush()
        try:
            os.fsync(f.fileno())
        except OSError:
            # Some platforms/filesystems may not support fsync; ignore.
            pass
        f.close()
        os.replace(tmp_path, path)
    finally:
        # Very defensive cleanup
        try:
            if not f.closed:
                f.close()
        except Exception:
            pass
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def load_metadata(path: str) -> Optional[Dict[str, Any]]:
    """
    Load a metadata dict from the given path, or return None if missing/invalid.
    """
    try:
        with open(path, "rb") as f:
            data = pickle.load(f)
        if isinstance(data, dict):
            return data
    except FileNotFoundError:
        return None
    except Exception:
        # For Week 0 we treat any error as "no metadata".
        return None
    return None


def save_metadata(path: str, data: Dict[str, Any]) -> None:
    """
    Save a metadata dict to the given path using atomic_write.
    """
    with atomic_write(path, "wb") as f:
        pickle.dump(data, f)
