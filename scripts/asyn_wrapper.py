from __future__ import annotations

"""
MAGIC stub: lightweight replacement for fsspec.asyn wrapper.

The real module integrates with fsspec.asyn.AsyncFileSystem and exposes
helpers like running_async / sync wrappers.

For MAGIC, we only need:
- imports to succeed
- a minimal AsyncFileSystem placeholder
- a running_async() helper
- a simple sync() wrapper to run async callables if needed
"""

from typing import Any, Awaitable, Callable, TypeVar
import asyncio

T = TypeVar("T")


class AsyncFileSystem:
    """
    Minimal placeholder for fsspec.asyn.AsyncFileSystem.

    This class is intentionally tiny. In MAGIC we only care that:
    - The name exists for type checkers and imports.
    - It does not try to touch real fsspec internals at import time.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    async def _open(self, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover - stub
        raise RuntimeError("AsyncFileSystem._open is not implemented in MAGIC stub.")


def running_async() -> bool:
    """
    Return True if there is a running event loop, False otherwise.
    This mimics the common pattern used by async wrappers.
    """
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


def _ensure_awaitable(obj: Any) -> Awaitable[Any]:
    """
    Internal helper: wrap non-awaitables in a trivial coroutine so we can
    treat everything uniformly.
    """

    async def _wrapper() -> Any:
        return obj

    if asyncio.iscoroutine(obj) or isinstance(obj, Awaitable):
        return obj  # type: ignore[return-value]
    return _wrapper()


def sync(func: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    """
    Very small helper that runs an async function in a fresh event loop
    when we are not already inside one.

    This is good enough for tests that want to call sync(some_async_fn)(...).
    """

    def wrapper(*args: Any, **kwargs: Any) -> T:
        if running_async():
            # In a real wrapper you might use current loop; for MAGIC we assume
            # caller knows what they are doing in that case.
            coro = func(*args, **kwargs)
            raise RuntimeError(
                "sync() called while already running an event loop in MAGIC stub."
            )
        return asyncio.run(func(*args, **kwargs))

    return wrapper
