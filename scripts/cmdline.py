from __future__ import annotations

"""
Week 0 stub for scripts.cmdline.

The original module is a Pygments command-line interface that imports
pip._vendor.pygments and parses real CLI arguments. For MAGIC's Week 0
smoke-import tests we only need this module to be importable without
side effects or external dependencies.
"""

from typing import List, Optional


__version__ = "0.0-week0-stub"


def main(argv: Optional[List[str]] = None) -> int:
    """
    Minimal CLI entry point stub.

    Does nothing and returns success. Not invoked during pytest imports
    because it is guarded by the standard if __name__ == "__main__" block.
    """
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
