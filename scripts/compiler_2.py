from __future__ import annotations

"""
Week 0 stub for `scripts.compiler_2`.

The original module uses `altair.utils._importers.import_vl_convert` to
load the vega-lite conversion backend. For MAGIC Week 0 smoke-import
tests we only need this module to import cleanly.

We provide a tiny stub `import_vl_convert` that returns a dummy callable.
"""

from typing import Any, Callable


def import_vl_convert(*_args: Any, **_kwargs: Any) -> Callable[..., Any]:
    """
    Stand-in for `altair.utils._importers.import_vl_convert`.

    Returns a callable that pretends to perform a conversion and just
    returns an empty dict.
    """

    def _dummy_convert(*args: Any, **kwargs: Any) -> dict:
        return {}

    return _dummy_convert
