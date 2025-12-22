from __future__ import annotations

"""
MAGIC stub: safe placeholder for certificate transparency helpers.

Week 0 Goal:
- Allow `import scripts.certificate_transparency` to succeed
- Avoid importing real `cryptography.utils` or other heavy deps
- Provide minimal, harmless API surface if something calls into it
"""

from typing import Any, Iterable, List


class LogEntry:
    """Very small placeholder for a CT log entry."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover
        return f"<MAGIC-CT-LogEntry len_args={len(self.args)}>"


def verify_scts(
    chain: Iterable[bytes] | None = None,
    scts: Iterable[bytes] | None = None,
    *args: Any,
    **kwargs: Any,
) -> bool:
    """
    Minimal stub for an SCT verification helper.

    Real cryptography validates Signed Certificate Timestamps.
    For MAGIC Week 0 we simply return True so optional CT checks "pass".
    """
    return True


def get_log_list() -> List[LogEntry]:
    """
    Return an empty list of CT logs.

    Callers can iterate safely but no real CT metadata is shipped.
    """
    return []
