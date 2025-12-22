"""
MAGIC Week 0 shim for a DBFS + fsspec helper.

The original module used `from fsspec import AbstractFileSystem`, which is
not reliable in our environment (and we do not want real remote I/O during
smoke tests).

Here we provide a very small local AbstractFileSystem and a dummy DBFS
client that raises if used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class AbstractFileSystem:
    """
    Local placeholder; mirrors the shape of fsspec.AbstractFileSystem enough
    for imports and simple type checks.
    """

    root_marker: str = "/"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.storage_options = kwargs

    def open(self, path: str, mode: str = "rb", *args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("MAGIC dbfs shim: no real filesystem backend configured")


@dataclass
class DummyDbfsClient:
    host: str

    def upload(self, src: str, dest: str) -> None:
        raise RuntimeError("MAGIC dbfs shim: upload not implemented in smoke tests")
