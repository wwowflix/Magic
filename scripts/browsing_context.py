from __future__ import annotations

"""
MAGIC shim for scripts.browsing_context.

The original module wraps Selenium BiDi browsing context commands.
For MAGIC Week 0 we only need:

- the module to import cleanly
- a lightweight BrowsingContext-like object
- a couple of no-op helpers for managing contexts

No real Selenium or WebDriver calls are performed here.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BrowsingContext:
    """Minimal placeholder for a browser tab / window."""
    context_id: str
    url: Optional[str] = None
    title: Optional[str] = None
    active: bool = True


# In-memory registry for this shim only
_CONTEXTS: List[BrowsingContext] = []


def create_browsing_context(url: Optional[str] = None, title: Optional[str] = None) -> BrowsingContext:
    """
    Create and register a new BrowsingContext.

    In this MAGIC shim we just keep it in a local list with a simple id.
    """
    ctx_id = f"magic-context-{len(_CONTEXTS) + 1}"
    ctx = BrowsingContext(context_id=ctx_id, url=url, title=title, active=True)
    _CONTEXTS.append(ctx)
    return ctx


def list_browsing_contexts() -> List[BrowsingContext]:
    """Return all known browsing contexts in this shim."""
    return list(_CONTEXTS)


def close_browsing_context(context_id: str) -> None:
    """
    Mark a browsing context as inactive.

    If the id is not found, this is a no-op.
    """
    for ctx in _CONTEXTS:
        if ctx.context_id == context_id:
            ctx.active = False
            break


__all__ = [
    "BrowsingContext",
    "create_browsing_context",
    "list_browsing_contexts",
    "close_browsing_context",
]
