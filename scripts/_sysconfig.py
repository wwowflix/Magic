"""MAGIC shim for pip._internal-style sysconfig helpers.

The real code deals with pip installation schemes. For MAGIC tests we
only need the module to import successfully.
"""

from __future__ import annotations
