from __future__ import annotations

"""
MAGIC stub: Greek language model for chardet-style detectors.

The original file imported:
    from pip._vendor.chardet.sbcharsetprober import SingleByteCharSetModel

We do NOT want that pip._vendor dependency in MAGIC Week 0, so this stub
provides a tiny local stand-in and two model constants:

- ISO_8859_7_GREEK_MODEL
- WINDOWS_1253_GREEK_MODEL

The detectors only care that these objects exist and are "model-like".
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SingleByteCharSetModel:
    """
    Minimal stand-in for the real SingleByteCharSetModel.

    For Week 0, we just store some metadata fields that call sites might
    look at, but we do not implement any scoring logic.
    """

    char_to_order_map: Optional[Any] = None
    language: str = "Greek"
    encoding: Optional[str] = None
    alphabet: str = "Greek"


# Very small placeholder "maps" – the actual numeric tables are not needed
# for MAGIC Week 0, so we just use empty tuples.
_DUMMY_CHAR_TO_ORDER: tuple[int, ...] = ()


ISO_8859_7_GREEK_MODEL = SingleByteCharSetModel(
    char_to_order_map=_DUMMY_CHAR_TO_ORDER,
    language="Greek",
    encoding="iso-8859-7",
)

WINDOWS_1253_GREEK_MODEL = SingleByteCharSetModel(
    char_to_order_map=_DUMMY_CHAR_TO_ORDER,
    language="Greek",
    encoding="windows-1253",
)
