from __future__ import annotations

"""
Week 0 stub for scripts.main.

The original module is a CLI entrypoint that imports pip internals and
parses command-line arguments. For smoke-import tests we only need a
minimal surface so that scripts.cli and others can import it safely.
"""

from typing import Any, Dict, List, Optional, Tuple


def dotenv_values(*_a: Any, **_k: Any) -> Dict[str, str]:
    """
    Stub for dotenv_values used by CLI-related tools.
    Returns an empty mapping during Week 0 tests.
    """
    return {}


def set_key(_file: str, _key: str, _value: str, *_a: Any, **_k: Any) -> Tuple[None, str, str]:
    """
    Stub for set_key similar to python-dotenv's behavior.
    """
    return (None, _key, _value)


def unset_key(_file: str, _key: str, *_a: Any, **_k: Any) -> Tuple[None, str]:
    """
    Stub for unset_key similar to python-dotenv's behavior.
    """
    return (None, _key)


def main(argv: Optional[List[str]] = None) -> int:
    """
    Minimal CLI entry-point stub.

    Not invoked during pytest imports because it is guarded by
    if __name__ == "__main__".
    """
    # A real implementation can wire in argument parsing here later.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
