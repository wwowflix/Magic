from __future__ import annotations

from typing import Any, Dict
from scripts.error_flow_mvp import MagicError, ErrorReport, log_error


class Err003FileRoutingFailure(MagicError):
    """Auto-generated error for ERR003."""
    pass


def build_error_report(context: Dict[str, Any] | None = None) -> ErrorReport:
    """Build a standardised ErrorReport for ERR003."""
    exc = Err003FileRoutingFailure("ERR003: File routing failure")
    ctx: Dict[str, Any] = dict(context or {})
    ctx.setdefault("error_code", "ERR003")
    ctx.setdefault("severity", "warning")
    return log_error(exc, kind="file_flow", context=ctx)
