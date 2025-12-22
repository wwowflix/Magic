from __future__ import annotations

"""
MAGIC shim for scripts.build_meta (PEP 517 interface).

The original module integrates setuptools and distutils to build wheels/sdists.
For MAGIC Week 0 we only need:

- the module to import cleanly
- basic PEP 517-style functions with no-op or minimal behaviour
"""

from pathlib import Path
from typing import Dict, Iterable, List, Optional


def get_requires_for_build_wheel(
    config_settings: Optional[Dict[str, object]] = None,
) -> List[str]:
    """Return an empty list of extra build requirements."""
    return []


def get_requires_for_build_sdist(
    config_settings: Optional[Dict[str, object]] = None,
) -> List[str]:
    """Return an empty list of extra build requirements for sdists."""
    return []


def prepare_metadata_for_build_wheel(
    metadata_directory: str,
    config_settings: Optional[Dict[str, object]] = None,
) -> str:
    """
    Create minimal metadata and return a metadata directory name.

    In this MAGIC shim we simply return a fixed stub name.
    """
    return "MAGIC-0.0.0.dist-info"


def build_wheel(
    wheel_directory: str,
    config_settings: Optional[Dict[str, object]] = None,
    metadata_directory: Optional[str] = None,
) -> str:
    """
    Build a wheel and return the filename.

    In this MAGIC shim we do not actually build anything; we just return a
    deterministic name that *would* be the wheel file.
    """
    wheel_name = "MAGIC-0.0.0-py3-none-any.whl"
    # Ensure the directory exists (best-effort).
    Path(wheel_directory).mkdir(parents=True, exist_ok=True)
    return wheel_name


def build_sdist(
    sdist_directory: str,
    config_settings: Optional[Dict[str, object]] = None,
) -> str:
    """
    Build an sdist and return the filename.

    In this MAGIC shim we do not build a real sdist; we just return a stub
    filename and make sure the directory exists.
    """
    sdist_name = "MAGIC-0.0.0.tar.gz"
    Path(sdist_directory).mkdir(parents=True, exist_ok=True)
    return sdist_name


__all__ = [
    "get_requires_for_build_wheel",
    "get_requires_for_build_sdist",
    "prepare_metadata_for_build_wheel",
    "build_wheel",
    "build_sdist",
]
