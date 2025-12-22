from __future__ import annotations

"""
MAGIC Week 0 shim for scripts.dashboard.magic_dashboard.

Goal:
- Allow `import scripts.dashboard.magic_dashboard` under pytest.
- Avoid starting Streamlit or touching any real databases/files.
- Provide a tiny placeholder API that we can replace in a later phase.
"""

from typing import Any, Optional

try:
    import pandas as pd  # type: ignore[import]
except Exception:  # pragma: no cover - pandas not required in Week 0
    pd = None  # type: ignore[assignment]


def load_data(source: Optional[str] = None) -> "pd.DataFrame | None":
    """
    Week 0 stub: return an empty DataFrame (or None if pandas is missing).

    In a later MAGIC phase, this will read from SQLite / CSV / APIs.
    """
    if pd is None:
        return None
    return pd.DataFrame()


def build_dashboard(data: Optional["pd.DataFrame"] = None) -> None:
    """
    Week 0 stub: no-op.

    The real implementation will use Streamlit to render MAGIC trends,
    health, and analytics.
    """
    return None


def main() -> None:
    """
    Week 0 entrypoint: intentionally does nothing.

    This keeps imports safe while giving us a future hook for
    `python -m scripts.dashboard.magic_dashboard`.
    """
    _ = load_data(None)
    build_dashboard(None)


if __name__ == "__main__":
    main()
