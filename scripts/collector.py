from __future__ import annotations

"""
Week 0 stub for `scripts.collector`.

The original module uses pip's vendored `requests` and defines a
LinkCollector for discovering package sources. For MAGIC Week 0 we only
need this module to import cleanly and optionally provide a minimal,
non-networking implementation.
"""

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class LinkCollector:
    """
    Minimal stub of a link collector.

    In Week 0 this does not perform any real HTTP requests; it only
    echoes the input URLs as "collected" links.
    """

    def collect_sources(self, urls: Iterable[str]) -> List[str]:
        return list(urls)


def collect_sources(urls: Iterable[str]) -> List[str]:
    """
    Convenience function mirroring the LinkCollector.collect_sources
    behavior in a simplified form.
    """
    return list(urls)
