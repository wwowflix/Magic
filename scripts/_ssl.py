"""MAGIC shim for TLS-related helpers.

The real implementation integrates with trio and system SSL. For MAGIC
we just need a module that imports cleanly.
"""
from __future__ import annotations
