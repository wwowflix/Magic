from __future__ import annotations

"""
MAGIC shim for scripts.appengine

Original module typically detects Google App Engine environment and
adjusts HTTP behaviour.

For MAGIC smoke tests we only need imports to succeed, and a simple
boolean / helper.
"""

import os


ON_APPENGINE: bool = bool(os.environ.get("GAE_ENV"))


def is_appengine() -> bool:
    """Return True if environment resembles Google App Engine."""
    return ON_APPENGINE


__all__ = ["ON_APPENGINE", "is_appengine"]
