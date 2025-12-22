"""
MAGIC Week 0 shim: pandas datetimes utilities.

The original file relied on internal pandas C-extensions such as
`pandas._libs.tslibs.parsing.format_is_iso`.

For MAGIC smoke tests, we only require that the module imports
successfully, so we expose a tiny stub API.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DummyTimestamp:
    value: Optional[datetime] = None


def parse_datetime(value: str) -> DummyTimestamp:
    """
    Extremely small placeholder just to show *something* is here.
    """
    return DummyTimestamp()
