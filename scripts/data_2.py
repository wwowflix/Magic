"""
MAGIC Week 0: safe stub for data_2 (Altair-style helpers).

Goal:
- Let "import scripts.data_2" succeed.
- Provide sanitize_pandas_dataframe(...) with a compatible signature.
- Avoid importing altair, narwhals, pyarrow, or doing heavy work.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

try:
    import pandas as _pd  # noqa: F401
except Exception:
    _pd = None  # type: ignore[assignment]

if TYPE_CHECKING:  # only for type-checkers; not needed at runtime
    from pandas import DataFrame


@overload
def sanitize_pandas_dataframe(data: "DataFrame") -> "DataFrame":
    ...


@overload
def sanitize_pandas_dataframe(data: Any) -> Any:
    ...


def sanitize_pandas_dataframe(data: Any) -> Any:
    """
    Week 0 stub for altair.utils.core.sanitize_pandas_dataframe.
    For Week 0 we just return the input unchanged.
    """
    return data


__all__ = ["sanitize_pandas_dataframe"]
