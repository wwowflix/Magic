from __future__ import annotations

"""
MAGIC – Week 0 pandas config shim.

Goal
----
- Make `import scripts.config_init` safe during global smoke tests.
- Avoid re-registering pandas options like 'compute.use_bottleneck'.
- Do NOT call pandas._config.config.register_option at all.

The original vendored module has been moved to:
    config_init.py.magic_bak_week0

A later week can reintroduce a proper adapter if needed.
"""

from typing import Any

try:
    import pandas as _pd  # type: ignore[import]
except Exception:  # pragma: no cover - pandas may not be installed
    _pd = None  # type: ignore[assignment]


def init_pandas_options() -> None:
    """
    Week 0 no-op / minimal initializer.

    In the original module this may register custom options.
    Here we intentionally do nothing to avoid OptionError about
    already-registered keys such as 'compute.use_bottleneck'.
    """
    # If you ever want to tweak harmless options later, you can do:
    # if _pd is not None:
    #     _pd.set_option("display.width", 120)
    return None


# Run a very lightweight init if pandas is present
if _pd is not None:
    init_pandas_options()


__all__ = ["init_pandas_options"]
