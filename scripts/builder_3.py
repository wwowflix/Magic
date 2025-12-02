from __future__ import annotations

"""
MAGIC shim for scripts.builder_3.

The original module is a fontTools name-table builder that imports
fontTools.ttLib.tables._n_a_m_e and complex OpenType structures.

For MAGIC Week 0 we only need:

- the module to import cleanly
- optionally a small helper that looks like a "builder" API
"""

from typing import Any


def build_name_table(*args: Any, **kwargs: Any) -> None:
    """
    No-op placeholder used by MAGIC.

    Callers that expect some side-effect can safely call this without
    raising errors, but it performs no real work.
    """
    return None


def main(argv: list[str] | None = None) -> int:
    """
    Optional CLI-style entry point.

    Returns 0 to indicate success without doing anything.
    """
    return 0


__all__ = ["build_name_table", "main"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
