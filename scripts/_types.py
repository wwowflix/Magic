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
