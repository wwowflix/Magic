from __future__ import annotations

"""
MAGIC stub for a date/time parser.

The original file was a large port of python-dateutil's parser, with complex
relative imports (..relativedelta, ..tz) that don't match the MAGIC scripts/
layout.

For MAGIC, the smoke tests only require that `import scripts._parser_2`
works. We provide a tiny `parse` function and a `ParserError` type so any
future code that imports these names won't crash.
"""

import datetime as _dt
from typing import Any as _Any


class ParserError(Exception):
    """MAGIC stub parser error."""
    pass


def parse(timestr: str, default: _dt.datetime | None = None, **kwargs: _Any) -> _dt.datetime:
    """Very small, safe datetime parser stub.

    Behaviour:
    - Try `datetime.fromisoformat`.
    - If that fails, return `default` or a fixed fallback value.

    This is NOT a full replacement for dateutil.parser.parse â€“ it's only
    here so MAGIC can import `scripts._parser_2` without pulling in the
    entire dateutil stack.
    """
    if default is None:
        default = _dt.datetime(1970, 1, 1)

    try:
        return _dt.datetime.fromisoformat(timestr)
    except Exception:
        return default
