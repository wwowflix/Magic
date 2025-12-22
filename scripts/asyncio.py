from __future__ import annotations

"""
MAGIC – Week 0 asyncio shim.

Purpose
-------
- Allow `import scripts.asyncio` to succeed in smoke tests.
- Avoid importing the broken stdlib `asyncio` package
  (its __init__ currently raises NameError in this environment).
- Do NOT modify or replace the real stdlib `asyncio` module.

Any real async behaviour should use the standard-library module directly:
    import asyncio as std_asyncio

This file is a minimal placeholder until a proper adapter is implemented.
"""

IS_MAGIC_ASYNCIO_SHIM = True


def get_event_loop() -> None:  # type: ignore[override]
    """
    Week 0 placeholder.

    Intentionally NOT wired to a real event loop to avoid masking issues.
    """
    raise RuntimeError(
        "MAGIC asyncio shim: real event loop not available in Week 0. "
        "Use the stdlib `asyncio` module directly for real async behaviour."
    )


async def sleep(delay: float) -> None:  # type: ignore[override]
    """
    Week 0 placeholder async sleep.

    Exists only so attribute lookups don't fail; always raises at runtime.
    """
    raise RuntimeError(
        "MAGIC asyncio shim: `sleep()` is not implemented in Week 0. "
        "Use `asyncio.sleep` from the stdlib instead."
    )


__all__ = [
    "IS_MAGIC_ASYNCIO_SHIM",
    "get_event_loop",
    "sleep",
]
