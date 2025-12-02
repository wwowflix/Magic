"""
MAGIC shim for scripts.annotations

Goal: let `import scripts.annotations` succeed in smoke tests
without pulling heavy syntax / pygments / pip._vendor dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from .enums import AnnotationFlag, AnnotationName, FileAttachmentAnnotationName


@dataclass
class Annotation:
    """
    Minimal annotation object used by MAGIC.

    Real implementations may have many fields and behaviours.
    For our smoke tests we just need a stable, importable type.
    """
    id: str
    name: AnnotationName
    created_at: datetime
    payload: Dict[str, Any]
    flag: AnnotationFlag = AnnotationFlag.NONE
    attachment_name: Optional[FileAttachmentAnnotationName] = None


__all__ = [
    "Annotation",
    "AnnotationFlag",
    "AnnotationName",
    "FileAttachmentAnnotationName",
]
