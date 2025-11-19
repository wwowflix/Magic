"""
MAGIC shim for scripts.enums

We only need to satisfy imports from scripts.annotations:

    from .enums import AnnotationFlag, AnnotationName, FileAttachmentAnnotationName
"""

from enum import Enum, IntFlag, auto


class AnnotationName(str, Enum):
    COMMENT = "comment"
    HIGHLIGHT = "highlight"
    NOTE = "note"
    FILE_ATTACHMENT = "file-attachment"
    OTHER = "other"


class FileAttachmentAnnotationName(str, Enum):
    GENERIC = "generic-file-attachment"
    IMAGE = "image-file-attachment"
    PDF = "pdf-file-attachment"
    OTHER = "other-file-attachment"


class AnnotationFlag(IntFlag):
    NONE = 0
    IMPORTANT = auto()
    RESOLVED = auto()
    HIDDEN = auto()
    PINNED = auto()


__all__ = [
    "AnnotationFlag",
    "AnnotationName",
    "FileAttachmentAnnotationName",
]
