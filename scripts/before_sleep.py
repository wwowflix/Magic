from __future__ import annotations

"""
MAGIC stub: replacement for tenacity "before_sleep" helpers.
"""

from typing import Any, Callable


def before_sleep_log(logger: Any, log_level: Any) -> Callable:
    """
    Decorator factory placeholder; in real code this logs before sleeping
    between retries. Here it is a no-op wrapper.
    """

    def decorator(fn: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any):
            return fn(*args, **kwargs)

        return wrapper

    return decorator
