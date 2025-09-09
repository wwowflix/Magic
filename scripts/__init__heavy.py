"""
Safe package initializer to avoid heavy side-effects at import time.

The original contents were moved to __init__heavy.py.
Call `scripts.bootstrap()` to execute them explicitly.
"""

__all__ = []

def bootstrap():
    import os, runpy
    here = os.path.dirname(__file__)
    heavy = os.path.join(here, "__init__heavy.py")
    if os.path.exists(heavy):
        # Run the old init in isolation; only when explicitly requested
        runpy.run_path(heavy, run_name="__main__")
    else:
        print("No __init__heavy.py found; nothing to bootstrap.")
