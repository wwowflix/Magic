"""
MAGIC Week 0 shim for `scripts.annotations`.

Goal:
- Let `import scripts.annotations` succeed in smoke tests.
- Provide small, self-contained enums and a simple Annotation dataclass.
- Avoid any dependency on `scripts.enums` or heavy rich/syntax logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntFlag, auto
from typing import Any, Dict, Optional


class AnnotationFlag(IntFlag):
    """
    Tiny flag enum for marking annotations.

    This is intentionally minimal. It just needs to exist and be usable.
    """

    NONE = 0
    IMPORTANT = auto()
    TODO = auto()
    RESOLVED = auto()


class AnnotationName(Enum):
    """
    Basic annotation kinds.

    Real implementations may have more; Week 0 only needs stable names.
    """

    COMMENT = "comment"
    TODO = "todo"
    WARNING = "warning"
    INFO = "info"


class FileAttachmentAnnotationName(Enum):
    """
    Placeholder names for file-related annotations.
    """

    FILE = "file"
    IMAGE = "image"
    LINK = "link"


@dataclass
class Annotation:
    """
    Simple data holder for an annotation.

    This is enough for imports and for tests that just construct / inspect it.
    """

    name: AnnotationName
    message: str
    created_at: datetime = datetime.utcnow()
    flag: AnnotationFlag = AnnotationFlag.NONE
    extra: Optional[Dict[str, Any]] = None


def make_simple_annotation(
    message: str,
    name: AnnotationName = AnnotationName.COMMENT,
    flag: AnnotationFlag = AnnotationFlag.NONE,
    extra: Optional[Dict[str, Any]] = None,
) -> Annotation:
    """
    Convenience helper used by tests or tools.

    Returns a basic Annotation instance.
    """
    return Annotation(name=name, message=message, flag=flag, extra=extra)
