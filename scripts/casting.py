from __future__ import annotations

"""
MAGIC stub for pandas casting helpers.

The original module depended on `pandas.compat.np_version_under1p21`.
That symbol no longer exists in modern pandas, so we re-create the
behaviour we actually need:

- Provide `np_version_under1p21` as a boolean flag
- Offer one tiny helper to check safe casting, so call sites can work.
"""

from typing import Any
import numpy as np


def _np_version_tuple() -> tuple[int, int, int]:
    try:
        parts = np.__version__.split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        micro = int(parts[2].split("+")[0]) if len(parts) > 2 else 0
        return (major, minor, micro)
    except Exception:
        # Extremely defensive: if anything goes wrong, pretend version 0.0.0
        return (0, 0, 0)


NP_VERSION = _np_version_tuple()

# Public flag to mirror the old pandas.compat behaviour
np_version_under1p21: bool = NP_VERSION < (1, 21, 0)


def can_cast_safely(value: Any, dtype: "np.dtype[Any]") -> bool:
    """
    Very small utility: try casting value to dtype and report if it works.

    This is deliberately simple and safe; for Week 0 we just need a helper
    that exists and behaves sensibly.
    """
    try:
        np.asarray(value, dtype=dtype)
        return True
    except Exception:
        return False
