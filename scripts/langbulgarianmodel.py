from __future__ import annotations

"""
MAGIC stub: Bulgarian language model for chardet-style detectors.

The original file imported:
    from pip._vendor.chardet.sbcharsetprober import SingleByteCharSetModel

We do NOT want that pip._vendor dependency in MAGIC Week 0, so this stub
provides a tiny local stand-in and two model constants:

- ISO_8859_5_BULGARIAN_MODEL
- WINDOWS_1251_BULGARIAN_MODEL

The detectors only care that these objects exist and are "model-like".
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SingleByteCharSetModel:
    """
    Minimal stand-in for the real SingleByteCharSetModel.

    For Week 0, we just store some metadata fields that call sites might
    look at, but we do not implement any scoring logic.
    """

    char_to_order_map: Optional[Any] = None
    language: str = "Bulgarian"
    encoding: Optional[str] = None
    alphabet: str = "Bulgarian"
    # In the real implementation there are many more fields; we don't
    # need them for imports + basic use in detectors.


# Very small placeholder "maps" – the actual numeric tables are not needed
# for MAGIC Week 0, so we just use empty tuples.
_DUMMY_CHAR_TO_ORDER: tuple[int, ...] = ()


ISO_8859_5_BULGARIAN_MODEL = SingleByteCharSetModel(
    char_to_order_map=_DUMMY_CHAR_TO_ORDER,
    language="Bulgarian",
    encoding="iso-8859-5",
)

WINDOWS_1251_BULGARIAN_MODEL = SingleByteCharSetModel(
    char_to_order_map=_DUMMY_CHAR_TO_ORDER,
    language="Bulgarian",
    encoding="windows-1251",
)
