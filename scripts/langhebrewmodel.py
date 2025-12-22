from __future__ import annotations

"""
MAGIC stub: Hebrew language model for chardet-style detectors.

The original file imported:
    from pip._vendor.chardet.sbcharsetprober import SingleByteCharSetModel

For MAGIC Week 0 we do NOT want that pip._vendor dependency, so this stub
provides a tiny local stand-in and the model constant:

- WINDOWS_1255_HEBREW_MODEL

The detectors only care that these objects exist and are "model-like".
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SingleByteCharSetModel:
    """
    Minimal stand-in for the real SingleByteCharSetModel.

    For Week 0, we just store some metadata fields that call sites might
    look at, but we do not implement scoring or statistics.
    """

    char_to_order_map: Optional[Any] = None
    language: str = "Hebrew"
    encoding: Optional[str] = None
    alphabet: str = "Hebrew"


# Placeholder map – real numeric tables are not needed for MAGIC imports.
_DUMMY_CHAR_TO_ORDER: tuple[int, ...] = ()


WINDOWS_1255_HEBREW_MODEL = SingleByteCharSetModel(
    char_to_order_map=_DUMMY_CHAR_TO_ORDER,
    language="Hebrew",
    encoding="windows-1255",
)
