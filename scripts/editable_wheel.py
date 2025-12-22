from __future__ import annotations

"""
MAGIC Week 0 shim for editable_wheel.

Goals:
- Avoid SyntaxError from truncated original file.
- Avoid running heavy setuptools / wheel-building logic at import time.
- Provide a tiny, no-op API surface so imports and type hints are happy.
"""

from dataclasses import dataclass
from typing import Iterable, Any, Optional


@dataclass
class EditableWheelResult:
    """
    Minimal placeholder result object for editable wheel operations.
    """
    wheel_path: str = ""
    created: bool = False
    message: str = "MAGIC Week 0 shim: no real wheel created."


def build_editable_wheel(
    source_dir: str,
    target_dir: Optional[str] = None,
    args: Optional[Iterable[str]] = None,
) -> EditableWheelResult:
    """
    Week 0 placeholder implementation.

    Real behaviour (Week 1+):
    - Inspect project metadata.
    - Build an editable wheel into target_dir.
    - Return the filesystem path.

    Week 0 behaviour:
    - Do nothing and return a stub EditableWheelResult.
    """
    _ = (source_dir, target_dir, args)  # unused for now
    return EditableWheelResult()


__all__ = [
    "EditableWheelResult",
    "build_editable_wheel",
]
