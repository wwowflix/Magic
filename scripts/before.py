from __future__ import annotations

"""
MAGIC stub: replacement for tenacity "before" helpers.
"""

from typing import Any, Callable


def before_log(logger: Any, log_level: Any) -> Callable:
    """
    Very small decorator factory used in retry-style code.

    In the real implementation this logs before calling the function.
    For MAGIC we simply return the original function unchanged.
    """

    def decorator(fn: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any):
            return fn(*args, **kwargs)

        return wrapper

    return decorator
