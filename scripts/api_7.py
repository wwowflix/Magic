"""
MAGIC shim: api_7 – placeholder for missing scripts.v5 package.

The original module re-exported from `.v5.api`. In this environment we only
need a lightweight, import-safe stub so that tests/smoke can import this
module without pulling in the full dependency tree.
"""

from __future__ import annotations


class MagicAPIV5Compat:
    """
    Tiny stand-in object that pretends to be the v5 API surface.

    This is intentionally minimal and NOT a full implementation. It only
    exists so that `import scripts.api_7` succeeds during MAGIC smoke tests.
    """

    version = "v5-magic-shim"

    def describe(self) -> str:
        return "MAGIC compatibility shim for scripts.api_7 / v5.api"


def get_version() -> str:
    """Return a fake version string for the shim."""
    return MagicAPIV5Compat.version


__all__ = ["MagicAPIV5Compat", "get_version"]
