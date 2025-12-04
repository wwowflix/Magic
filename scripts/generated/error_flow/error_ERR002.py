from __future__ import annotations

from typing import Any, Dict
from scripts.error_flow_mvp import MagicError, ErrorReport, log_error


class Err002ModelFailure(MagicError):
    """Auto-generated error for ERR002."""
    pass


def build_error_report(context: Dict[str, Any] | None = None) -> ErrorReport:
    """Build a standardised ErrorReport for ERR002."""
    exc = Err002ModelFailure("ERR002: AI model failure")
    ctx: Dict[str, Any] = dict(context or {})
    ctx.setdefault("error_code", "ERR002")
    ctx.setdefault("severity", "error")
    return log_error(exc, kind="ai_flow", context=ctx)
