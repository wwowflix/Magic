from __future__ import annotations

"""
MAGIC stub for numpy.random.mtrand.

The real module provides a full RandomState implementation. For MAGIC, we
only need the class to exist so that `scripts._pickle` can import it.
"""

class RandomState:
    """Very small stand-in for numpy.random.mtrand.RandomState."""

    def __init__(self, *args, **kwargs):
        # Accept any arguments but do nothing.
        self._args = args
        self._kwargs = kwargs

    def get_state(self):
        """Return a dummy state object."""
        return {"state": "MAGIC-stub"}

    def set_state(self, state):
        """Accept a state object but ignore it."""
        self._state = state

    def __repr__(self) -> str:
        return f"<MAGIC RandomState stub args={self._args!r} kwargs={self._kwargs!r}>"
