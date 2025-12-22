from __future__ import annotations

"""
Week 0 stub for scripts.cmap.

The original module integrates with fontTools' merge/unicode machinery and
hits assertions in fontTools.merge.base during import.

For MAGIC Week 0, we only need this module to import cleanly. This stub
provides a minimal representation of a cmap table and a couple of helper
functions that higher-level code can call without pulling in fontTools.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass
class CmapEntry:
    codepoint: int
    glyph_name: str


@dataclass
class CmapTable:
    entries: List[CmapEntry]

    def get_glyph(self, codepoint: int) -> Optional[str]:
        for entry in self.entries:
            if entry.codepoint == codepoint:
                return entry.glyph_name
        return None

    def to_dict(self) -> Dict[int, str]:
        return {e.codepoint: e.glyph_name for e in self.entries}


def build_cmap(mapping: Dict[int, str]) -> CmapTable:
    """
    Build a simple cmap table from a codepoint → glyph name mapping.
    """
    entries = [CmapEntry(cp, name) for cp, name in mapping.items()]
    return CmapTable(entries=entries)


def merge_cmaps(cmps: Iterable[CmapTable]) -> CmapTable:
    """
    Merge multiple CmapTable objects.

    Later tables override earlier ones if they define the same codepoint.
    """
    merged: Dict[int, str] = {}
    for cmap in cmps:
        merged.update(cmap.to_dict())
    return build_cmap(merged)
