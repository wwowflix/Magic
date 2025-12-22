from __future__ import annotations

"""
MAGIC stub for langrussianmodel.

Replaces dependency on pip._vendor.chardet.sbcharsetprober.SingleByteCharSetModel.
We only need the constants that sbcsgroupprober imports and basic attribute access.
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
    language: str = "Russian"
    encoding: str | None = None
    alphabet: str = "Russian"


# Very small placeholder "maps" – the real tables are not needed for
# Week 0, we just need a hashable / iterable placeholder.
_DUMMY_CHAR_TO_ORDER: tuple[int, ...] = ()


def _make_model(encoding: str | None = None) -> SingleByteCharSetModel:
    return SingleByteCharSetModel(
        char_to_order_map=_DUMMY_CHAR_TO_ORDER,
        language="Russian",
        encoding=encoding,
    )


# Commonly-used models – if sbcsgroupprober imports these explicitly,
# they will exist.
KOI8R_RUSSIAN_MODEL = _make_model("koi8-r")
WINDOWS_1251_RUSSIAN_MODEL = _make_model("windows-1251")
ISO_8859_5_RUSSIAN_MODEL = _make_model("iso-8859-5")
MACCYRILLIC_RUSSIAN_MODEL = _make_model("mac-cyrillic")
IBM855_RUSSIAN_MODEL = _make_model("ibm855")
IBM866_RUSSIAN_MODEL = _make_model("ibm866")


def __getattr__(name: str) -> SingleByteCharSetModel:
    """
    Fallback for any additional *_RUSSIAN_MODEL constants.

    If some other code looks up EXTRA_RUSSIAN_MODEL, we return a generic
    SingleByteCharSetModel so imports and basic detectors still work.
    """
    if name.endswith("_RUSSIAN_MODEL"):
        return _make_model()
    raise AttributeError(name)
