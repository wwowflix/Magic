from __future__ import annotations

"""
MAGIC shim for scripts.models

Two roles:

1) requests-style HTTP models:
   - Request, PreparedRequest, Response
   - DEFAULT_REDIRECT_LIMIT, REDIRECT_STATI

2) charset-normalizer-style models:
   - CharsetMatch, CharsetMatches
   - CoherenceMatches (for earlier API expectations)
"""

from dataclasses import dataclass, field
from typing import Any, Iterable, List, MutableMapping, Optional, Set


# ============================================================================
# HTTP models (requests-style)
# ============================================================================

DEFAULT_REDIRECT_LIMIT: int = 30
REDIRECT_STATI: Set[int] = {301, 302, 303, 307, 308}


@dataclass
class Request:
    method: str = "GET"
    url: str = ""
    headers: MutableMapping[str, str] = field(default_factory=dict)
    data: Any = None
    json: Any = None

    def prepare(self) -> "PreparedRequest":
        return PreparedRequest(
            method=self.method,
            url=self.url,
            headers=dict(self.headers),
            body=self.data if self.data is not None else self.json,
        )


@dataclass
class PreparedRequest:
    method: str = "GET"
    url: str = ""
    headers: MutableMapping[str, str] = field(default_factory=dict)
    body: Any = None


@dataclass
class Response:
    status_code: int = 200
    url: str = ""
    headers: MutableMapping[str, str] = field(default_factory=dict)
    _content: bytes = b""
    reason: str = ""
    request: Optional[PreparedRequest] = None

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 400

    @property
    def text(self) -> str:
        try:
            return self._content.decode("utf-8")
        except Exception:
            return self._content.decode("latin1", errors="ignore")

    def json(self, **kwargs: Any) -> Any:
        import json

        if not self._content:
            return None
        encoding = kwargs.get("encoding", "utf-8")
        return json.loads(self._content.decode(encoding))

    def raise_for_status(self) -> None:
        # For smoke tests we do not enforce HTTP semantics.
        return None


# ============================================================================
# Coherence / charset-normalizer models
# ============================================================================


@dataclass
class CoherenceMatches:
    """Tiny placeholder to satisfy API/coherence-related imports."""
    matches: List[Any] = field(default_factory=list)

    def __iter__(self):
        return iter(self.matches)

    def __len__(self) -> int:
        return len(self.matches)


@dataclass
class CharsetMatch:
    """
    Minimal stand-in for charset_normalizer.models.CharsetMatch.
    """
    encoding: str
    language: Optional[str] = None
    chaos: Optional[float] = None
    confidence: Optional[float] = None
    raw: Optional[bytes] = None

    def __str__(self) -> str:
        return self.encoding

    def __repr__(self) -> str:
        return f"CharsetMatch(encoding={self.encoding!r}, language={self.language!r})"


@dataclass
class CharsetMatches:
    """
    Container behaving like list[CharsetMatch].
    """
    _matches: List[CharsetMatch] = field(default_factory=list)

    def append(self, match: CharsetMatch) -> None:
        self._matches.append(match)

    def extend(self, matches: Iterable[CharsetMatch]) -> None:
        self._matches.extend(matches)

    def best(self) -> Optional[CharsetMatch]:
        return self._matches[0] if self._matches else None

    def __iter__(self):
        return iter(self._matches)

    def __len__(self) -> int:
        return len(self._matches)

    def __getitem__(self, index: int) -> CharsetMatch:
        return self._matches[index]

    def __repr__(self) -> str:
        return f"CharsetMatches({self._matches!r})"


__all__ = [
    # HTTP models
    "Request",
    "PreparedRequest",
    "Response",
    "DEFAULT_REDIRECT_LIMIT",
    "REDIRECT_STATI",
    # coherence / charset models
    "CoherenceMatches",
    "CharsetMatch",
    "CharsetMatches",
]
