from __future__ import annotations

"""
MAGIC – Week 0 typing shim.

Goal
----
- Provide minimal type aliases so vendored code that does
  "from scripts import typing" or "from .typing import X"
  can import successfully.
"""

from typing import Any, Iterable, Mapping, MutableMapping, Tuple, Union

# Wide, very relaxed aliases – we just need the NAMES.
_URL = Any
_TYPE_BODY = Any
_TYPE_FIELDS = Iterable[Tuple[str, Any]]
_TYPE_HEADER_VALUE = Union[str, bytes]
_TYPE_HEADERS = Mapping[str, _TYPE_HEADER_VALUE]

__all__ = [
    "_URL",
    "_TYPE_BODY",
    "_TYPE_FIELDS",
    "_TYPE_HEADER_VALUE",
    "_TYPE_HEADERS",
]
