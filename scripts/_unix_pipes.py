"""MAGIC shim for Unix pipes helpers.

The real module is POSIX-only and raises ImportError on Windows.
Here we provide a dummy module so smoke tests do not fail.
"""

from __future__ import annotations
