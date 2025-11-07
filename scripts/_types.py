from __future__ import annotations

# SPDX-License-Identifier: MIT
# --- end MAGIC types shim ---
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.

from typing import Any, Callable, Tuple

# Type annotations
ParseFloat = Callable[[str], Any]
Key = Tuple[str, ...]
Pos = int

# --- MAGIC types shim ---
from typing import Mapping, Iterable, Tuple, Union, Optional

# Minimal shapes commonly used by HTTP-client style configs:
HeaderTypes = Union[Mapping[str, str], Iterable[Tuple[str, str]]]
TimeoutTypes = Union[float, Tuple[float, float], None]
CertTypes = Union[str, Tuple[str, str], None]

try:
    __all__
except NameError:
    __all__ = []
for _n in ("HeaderTypes", "TimeoutTypes", "CertTypes"):
    if _n not in __all__:
        __all__.append(_n)
# --- end MAGIC types shim ---
# --- shim block begin (MAGIC) ---
from typing import Any, Iterable, AsyncIterable, Mapping, Tuple, List, Dict, Union, Optional

# Anchor (for idempotency scans)
class _TypesShimAnchor: pass  # noqa: F401

# Stream-like typing aliases expected by _content
SyncByteStream  = Iterable[bytes]
AsyncByteStream = AsyncIterable[bytes]

# Request/response content typing that keeps http stack happy.
RequestContent  = Union[bytes, bytearray, str, SyncByteStream, AsyncByteStream]
RequestData     = Union[Mapping[str, Any], List[Tuple[str, Any]]]
# Common file tuple forms: (filename, content) or (filename, content, mimetype)
RequestFiles    = Mapping[str, Union[Tuple[str, bytes], Tuple[str, bytes, str]]]
ResponseContent = Union[bytes, SyncByteStream, AsyncByteStream]

# __all__ enrichment (non-destructive)
try:
    __all__  # type: ignore[name-defined]
except NameError:
    __all__ = []  # type: ignore[var-annotated]

for _n in [
    "SyncByteStream", "AsyncByteStream",
    "RequestContent", "RequestData", "RequestFiles",
    "ResponseContent"
]:
    if _n not in __all__:
        __all__.append(_n)
# --- shim block end (MAGIC) ---
