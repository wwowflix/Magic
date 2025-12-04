from __future__ import annotations

from typing import Any, Dict
from scripts.error_flow_mvp import MagicError, ErrorReport, log_error


class Err001DataTimeout(MagicError):
    """Auto-generated error for ERR001."""
    pass


def build_error_report(context: Dict[str, Any] | None = None) -> ErrorReport:
    """Build a standardised ErrorReport for ERR001."""
    exc = Err001DataTimeout("ERR001: Data timeout")
    ctx: Dict[str, Any] = dict(context or {})
    ctx.setdefault("error_code", "ERR001")
    ctx.setdefault("severity", "warning")
    return log_error(exc, kind="data_flow", context=ctx)
