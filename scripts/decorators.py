"""
MAGIC Week 0 shim for legacy test decorators.

The original module expected test-only helpers like
`SkipTest`, `assert_warns`, `HAS_REFCOUNT` from a local `utils` package.

For MAGIC we only need this module to import, so we provide tiny stubs.
"""

from __future__ import annotations


class SkipTest(Exception):
    """MAGIC stub for nose.SkipTest / unittest.SkipTest."""


def assert_warns(*args, **kwargs):
    """MAGIC stub: no-op warning assertion."""
    return None


HAS_REFCOUNT = False


def slow(func):
    """
    Example decorator stub that just returns the function unchanged.
    """
    return func
