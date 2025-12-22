"""MAGIC stub for tenacity.after-style helpers.

The real implementation integrates with pip._vendor.tenacity._utils.
Here we only provide a compatible after_log decorator that is import-safe.
"""

from __future__ import annotations

from typing import Any, Callable


def after_log(logger: Any | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Return a no-op decorator that simply calls the wrapped function."""

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = fn(*args, **kwargs)
            # A real implementation would log here; MAGIC stub does nothing.
            return result

        return wrapper

    return decorator


__all__ = ["after_log"]
