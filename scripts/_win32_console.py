"""MAGIC shim for pip-style Win32 console helpers.

The real implementation wraps Windows console APIs and uses rich for
color handling. For MAGIC tests we keep this as an empty stub.
"""

from __future__ import annotations
