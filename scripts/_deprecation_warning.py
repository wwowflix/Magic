# -*- coding: utf-8 -*-
"""Compatibility shim for setuptools-style deprecation warning used by tests."""

__all__ = ["SetuptoolsDeprecationWarning"]

class SetuptoolsDeprecationWarning(Warning):
    """Base class for warning deprecations (visible by default)."""
    pass
