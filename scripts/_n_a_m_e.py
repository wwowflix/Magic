# -*- coding: utf-8 -*-
"""
MAGIC shim for fontTools.ttLib.tables._n_a_m_e

Goal:
- Import cleanly inside MAGIC
- Avoid all dependency / sys.path weirdness around fontTools
- Provide a minimal but compatible surface (table__n_a_m_e, NameRecord)
  so other code and smoke tests don't crash.

This is NOT a full OpenType 'name' table implementation.
It is a light-weight compatibility layer.
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple


class NameRecord:
    """Very small stand-in for fontTools.ttLib.tables._n_a_m_e.NameRecord."""

    def __init__(
        self,
        string: str | bytes = "",
        nameID: int = 0,
        platformID: int = 3,
        platEncID: int = 1,
        langID: int = 0x409,
    ) -> None:
        self.string = string
        self.nameID = nameID
        self.platformID = platformID
        self.platEncID = platEncID
        self.langID = langID

    # --- basic encoding helpers -------------------------------------------------

    def toUnicode(self, errors: str = "strict") -> str:
        if isinstance(self.string, bytes):
            try:
                return self.string.decode("utf-8", errors=errors)
            except Exception:
                return self.string.decode("latin-1", errors=errors)
        return str(self.string)

    def toBytes(self, errors: str = "strict") -> bytes:
        if isinstance(self.string, bytes):
            return self.string
        return str(self.string).encode("utf-8", errors=errors)

    # fontTools compatibility alias
    toStr = toUnicode  # type: ignore[assignment]

    def __repr__(self) -> str:
        return (
            f"<NameRecord NameID={self.nameID}; "
            f"PlatformID={self.platformID}; LanguageID={self.langID}>"
        )


class table__n_a_m_e:
    """
    Tiny shim for the 'name' table.

    It only supports a subset of the real behaviour that MAGIC is likely to use:
    - storing NameRecord objects in .names
    - basic getName / setName / addName helpers
    - simple getBestFullName for debugging
    """

    # kept for compatibility with the real table
    dependencies: Sequence[str] = ("ltag",)

    def __init__(self, tag: Optional[str] = None) -> None:
        self.tag = tag
        self.names: List[NameRecord] = []

    # --- core helpers -----------------------------------------------------------

    def getName(
        self,
        nameID: int,
        platformID: int,
        platEncID: int,
        langID: Optional[int] = None,
    ) -> Optional[NameRecord]:
        for n in self.names:
            if (
                n.nameID == nameID
                and n.platformID == platformID
                and n.platEncID == platEncID
                and (langID is None or n.langID == langID)
            ):
                return n
        return None

    def setName(
        self,
        string: str | bytes,
        nameID: int,
        platformID: int,
        platEncID: int,
        langID: int,
    ) -> None:
        rec = self.getName(nameID, platformID, platEncID, langID)
        if rec is None:
            rec = NameRecord(
                string=string,
                nameID=nameID,
                platformID=platformID,
                platEncID=platEncID,
                langID=langID,
            )
            self.names.append(rec)
        else:
            rec.string = string

    def addName(
        self,
        string: str | bytes,
        platforms: Iterable[Tuple[int, int, int]] = ((3, 1, 0x409),),
        minNameID: int = 255,
    ) -> int:
        """Add a new name for each platform triplet and return the new nameID."""
        # choose next available ID > minNameID
        existing = [n.nameID for n in self.names if n.nameID > minNameID]
        nameID = (max(existing) + 1) if existing else (minNameID + 1)
        for platformID, platEncID, langID in platforms:
            self.setName(string, nameID, platformID, platEncID, langID)
        return nameID

    # --- debug-ish helpers ------------------------------------------------------

    def getBestFullName(self) -> Optional[str]:
        """
        Minimal version of the real API:
        Try Windows English full name (nameID 4) first, otherwise first available.
        """
        rec = self.getName(4, 3, 1, 0x409)
        if rec is not None:
            return rec.toUnicode()

        if not self.names:
            return None
        # fallback: just give something stable-ish
        return self.names[0].toUnicode()

    # Stubs for APIs that real fontTools tables expose but MAGIC probably never
    # exercises deeply. They are here only so that attribute access doesn't crash.

    def decompile(self, data, ttFont) -> None:  # pragma: no cover - stub
        # We don't need real binary parsing for MAGIC's runners.
        self.names = []

    def compile(self, ttFont):  # pragma: no cover - stub
        # Return empty binary – MAGIC never serializes fonts.
        return b""

    def toXML(self, writer, ttFont) -> None:  # pragma: no cover - stub
        for rec in self.names:
            writer.simpletag(
                "namerecord",
                nameID=rec.nameID,
                platformID=rec.platformID,
                platEncID=rec.platEncID,
                langID=hex(rec.langID),
            )
            writer.newline()

    def fromXML(self, name, attrs, content, ttFont) -> None:  # pragma: no cover - stub
        if name != "namerecord":
            return
        s = "".join(content).strip()
        rec = NameRecord(
            string=s,
            nameID=int(attrs.get("nameID", "0")),
            platformID=int(attrs.get("platformID", "3")),
            platEncID=int(attrs.get("platEncID", "1")),
            langID=int(attrs.get("langID", "0x409"), 16),
        )
        self.names.append(rec)


# Lightweight visitor stub so imports like "from scripts._n_a_m_e import NameRecordVisitor"
# won't crash. It doesn't walk real fonts – MAGIC doesn't need that depth here.
class NameRecordVisitor:
    TABLES: Tuple[str, ...] = ("GSUB", "GPOS", "fvar", "CPAL", "STAT")

    def __init__(self) -> None:
        self.seen = set()

    def visit(self, font, *args, **kwargs) -> None:  # pragma: no cover - stub
        # Real fontTools walks tables here; we just do nothing.
        return
