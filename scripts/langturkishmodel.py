from __future__ import annotations

"""
MAGIC stub for langturkishmodel.

Removes dependency on pip._vendor.chardet.sbcharsetprober.SingleByteCharSetModel.
Provides ISO_8859_9_TURKISH_MODEL used by the SBCSGroupProber.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SingleByteCharSetModel:
    """
    Minimal stand-in for chardet SingleByteCharSetModel.

    We only keep a few descriptive fields; numeric maps are not needed
    for MAGIC Week 0.
    """

    char_to_order_map: Any | None = None
    language: str = "Turkish"
    encoding: Optional[str] = None
    alphabet: str = "Turkish"


# Placeholder table – real numeric data is not required for imports.
_DUMMY_CHAR_TO_ORDER: tuple[int, ...] = ()


# The single model sbcsgroupprober expects from this module.
ISO_8859_9_TURKISH_MODEL = SingleByteCharSetModel(
    char_to_order_map=_DUMMY_CHAR_TO_ORDER,
    language="Turkish",
    encoding="iso-8859-9",
)
