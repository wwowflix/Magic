from __future__ import annotations

"""
MAGIC Week 0 shim for scripts.dashboard.magic_ops_dashboard.

Goal:
- Let `import scripts.dashboard.magic_ops_dashboard` succeed under pytest.
- Do NOT import or start Streamlit.
- Avoid touching real databases, files, or the network.
- Provide a tiny placeholder API we can replace in a later phase.
"""

from typing import Any, Optional

try:
    import pandas as pd  # type: ignore[import]
except Exception:  # pragma: no cover
    pd = None  # type: ignore[assignment]


def load_ops_data(source: Optional[str] = None) -> "pd.DataFrame | None":
    """
    Week 0 stub: return an empty DataFrame (or None if pandas is missing).

    Later, this will read from MAGIC ops logs / SQLite / Notion exports etc.
    """
    if pd is None:
        return None
    return pd.DataFrame()


def build_ops_dashboard(data: Optional["pd.DataFrame"] = None) -> None:
    """
    Week 0 stub: no-op.

    Real implementation will render an ops view (queue health, failures,
    retries, etc.) via Streamlit or another UI layer.
    """
    return None


def main() -> None:
    """
    Week 0 entrypoint: intentionally does nothing visible.

    This gives us a future hook for `python -m scripts.dashboard.magic_ops_dashboard`
    without breaking imports during Week 0.
    """
    _ = load_ops_data(None)
    build_ops_dashboard(None)


if __name__ == "__main__":
    main()
