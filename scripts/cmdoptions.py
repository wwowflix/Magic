from __future__ import annotations

"""
Week 0 stub for scripts.cmdoptions.

The original module is part of pip's internal CLI option handling and
depends on pip._vendor.packaging. For MAGIC's Week 0 smoke-import
tests we only need this module to import cleanly; we do not require
real pip option behavior here.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OptionSpec:
    """Minimal stand-in for an option specification."""
    name: str
    help: str = ""
    default: Optional[Any] = None


def get_default_options() -> Dict[str, OptionSpec]:
    """
    Return a very small set of dummy options for illustrative purposes.

    This is only here so higher-level code that introspects options
    has something harmless to work with during Week 0.
    """
    return {
        "quiet": OptionSpec(name="quiet", help="Run in quiet mode.", default=False),
        "verbose": OptionSpec(name="verbose", help="Run in verbose mode.", default=False),
    }
