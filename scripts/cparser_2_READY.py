# -*- coding: utf-8 -*-
"""C parser stub for MAGIC; placeholder that compiles cleanly."""

from __future__ import annotations
from typing import Any, Tuple, Dict

# Stubbed exports that some modules might import during compile-only stages.
COMMON_TYPES: Dict[str, Any] = {}

class FFIError(Exception):
    """Stub FFI error."""

class CDefError(Exception):
    """Stub C definition error."""

def resolve_common_type(name: str) -> Tuple[str, Any]:
    """Return a dummy mapping for a 'common' C type."""
    return name, None

def parse_cdef(text: str) -> dict:
    """Pretend to parse a C definition and return a dummy AST."""
    return {"ast": [], "source_len": len(text)}
