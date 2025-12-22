"""MAGIC shim for trio.lowlevel-style helpers.

We only expose a tiny checkpoint() function so that imports from
`scripts.lowlevel` succeed during tests.
"""

from __future__ import annotations

import asyncio


async def checkpoint() -> None:
    """Tiny async checkpoint used as a placeholder."""
    await asyncio.sleep(0)
