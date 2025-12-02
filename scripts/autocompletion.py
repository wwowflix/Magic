"""
MAGIC stub: lightweight replacement for pip._internal-based autocompletion.

The original module is tightly coupled to `pip._internal.cli.main_parser` and
pip internals. For MAGIC we only need:

- safe import (no pip._internal requirement)
- a couple of tiny helpers that can be called by tests if needed
"""

from __future__ import annotations

from typing import Iterable, List, Optional


def get_completions(args: Optional[List[str]] = None) -> Iterable[str]:
    """
    Very small stand-in for a completion generator.

    In the real pip module, this would inspect available commands/options.
    Here we just return an empty iterable, which is enough for smoke tests.
    """
    if args is None:
        args = []
    # In a richer stub, you could return some fake commands here.
    return (item for item in [])  # empty generator


def autocomplete() -> int:
    """
    Entry point used by shell completion scripts.

    We do nothing and report success. This keeps the behavior simple and safe.
    """
    # In real pip, this would print completions to stdout based on env vars.
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """
    Tiny CLI shim that mimics an executable entry point.

    For MAGIC we don't parse anything; we just call `autocomplete()` to keep
    the shape of the API and return its result.
    """
    _ = argv or []
    return autocomplete()
