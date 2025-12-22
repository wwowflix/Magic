"""
MAGIC Week 0 shim for easy_install.

The original setuptools.easy_install module is deprecated, and
contains huge legacy code that is not needed for MAGIC.
This shim only exists so smoke tests can import the module safely.
"""

__all__ = ["EasyInstall"]

class EasyInstall:
    def __init__(self, *a, **kw):
        pass

    def install(self, *a, **kw):
        return None
