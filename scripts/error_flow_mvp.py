from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


class MagicError(Exception):
    """Base class for MAGIC-specific runtime errors."""
    pass


class DataFlowError(MagicError):
    """Raised when data ingestion / normalisation fails."""
    pass


class AiFlowError(MagicError):
    """Raised when AI flow or model interaction fails."""
    pass


class FileFlowError(MagicError):
    """Raised when file routing / processing fails."""
    pass


@dataclass
class ErrorReport:
    """Minimal structured error report for Week-1."""
    kind: str
    message: str
    context: Dict[str, Any]


def ensure_non_empty(value: str, *, field: str) -> str:
    """Week-1 helper: require a non-empty string field."""
    if not isinstance(value, str):
        raise DataFlowError(f"{field} must be a string, got {type(value)!r}")
    if not value.strip():
        raise DataFlowError(f"{field} cannot be empty")
    return value


def log_error(
    exc: MagicError,
    *,
    kind: str,
    context: Dict[str, Any] | None = None,
) -> ErrorReport:
    """
    Turn an error into an ErrorReport.

    Week-1: minimal shape (kind, message, context).
    """
    ctx: Dict[str, Any] = dict(context or {})
    ctx.setdefault("exc_type", type(exc).__name__)
    return ErrorReport(
        kind=kind,
        message=str(exc),
        context=ctx,
    )
