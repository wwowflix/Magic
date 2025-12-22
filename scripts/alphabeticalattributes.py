"""MAGIC stub for snscrape alphabeticalattributes filter.

The real module integrates with snscrape.utils.Filter; here we just expose
a minimal Filter class so imports succeed.
"""

from __future__ import annotations

import logging


class Filter(logging.Filter):
    """Minimal logging.Filter stand-in used by MAGIC.

    Always returns True so it never drops log records.
    """

    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover
        return True


__all__ = ["Filter"]
