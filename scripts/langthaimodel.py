from __future__ import annotations

"""
MAGIC stub for langthaimodel.

Replaces dependency on pip._vendor.chardet.sbcharsetprober.SingleByteCharSetModel.
We only provide TIS_620_THAI_MODEL used by the charset detectors.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class SingleByteCharSetModel:
    """
    Minimal stand-in for chardet SingleByteCharSetModel.

    We just keep a few descriptive fields; the numeric maps are omitted
    for MAGIC Week 0.
    """

    char_to_order_map: Any | None = None
    language: str = "Thai"
    encoding: str | None = None
    alphabet: str = "Thai"


# Placeholder map – real numeric tables are not needed for Week 0.
_DUMMY_CHAR_TO_ORDER: tuple[int, ...] = ()


# The single model sbcsgroupprober expects from this module.
TIS_620_THAI_MODEL = SingleByteCharSetModel(
    char_to_order_map=_DUMMY_CHAR_TO_ORDER,
    language="Thai",
    encoding="tis-620",
)
