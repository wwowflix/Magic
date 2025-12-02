# -*- coding: utf-8 -*-
"""
MAGIC shim for scripts._network

The original upstream module expected to live inside a package where
`from .. import socket as tsocket` works. In the MAGIC layout, that
relative import fails ("attempted relative import beyond top-level package").

For MAGIC we only need this module to import cleanly and expose a
`tsocket` object that behaves like the standard-library socket module.
"""

from __future__ import annotations

import socket as tsocket  # stdlib socket

__all__ = ["tsocket"]
