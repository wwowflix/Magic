"""
MAGIC Week 0 shim for a Databricks-style fsspec example.

The original script depended on `from fsspec import AbstractFileSystem`,
which is fragile in our environment.

For MAGIC smoke tests, we only need this module to import successfully, so
we provide a tiny local AbstractFileSystem placeholder and avoid importing
the real `fsspec` package entirely.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


class AbstractFileSystem:
    """
    Extremely small local placeholder for fsspec.AbstractFileSystem.

    This is only used to satisfy type/attribute references in this example.
    No real I/O is performed.
    """

    root_marker: str = "/"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.storage_options = kwargs

    def open(self, path: str, mode: str = "rb", *args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("MAGIC data_5 shim: no real filesystem backend configured")


@dataclass
class DummyDbfsConfig:
    workspace_url: str
    token: Optional[str] = None


# Example placeholder object that callers/tests might reference.
DEFAULT_CONFIG = DummyDbfsConfig(workspace_url="https://example.invalid")
