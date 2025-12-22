from __future__ import annotations

"""
MAGIC Week 0 shim for build_data_db.

Goals:
- Allow `import scripts.build_data_db` to succeed.
- Avoid touching sqlite or the filesystem at import time.
- Provide a tiny placeholder API that you can replace later in Week 1+.
"""

from dataclasses import dataclass
from typing import Sequence


@dataclass
class Record:
    """
    Extremely small stand-in for whatever real records this module
    would manage in a SQLite database.
    """
    keyword: str = ""
    data: str = ""


def build_index(db_path: str) -> None:
    """
    Week 0: no-op placeholder.

    Real implementation would open a sqlite database at `db_path`
    and populate tables. For the import layer we deliberately do
    nothing to avoid I/O and schema issues.
    """
    return None


def main(argv: Sequence[str] | None = None) -> int:
    """
    Week 0 CLI entrypoint placeholder.

    Real code would parse args and call `build_index`.
    Here we just return success so tools can import and maybe call it
    without blowing up.
    """
    return 0


__all__ = ["Record", "build_index", "main"]
