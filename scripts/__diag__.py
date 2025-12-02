"""
MAGIC shim for optional diagnostics used by ElementTree / helpers.

The original packages use this to toggle optional debug/diagnostic
behaviour. We only need importability, not functionality.
"""

class DiagFlags:
    # Optional flags expected by etree, html parsing, helpers, etc.
    debug = False
    incremental = False
    collect_stats = False

# Public instance expected by callers
__diag__ = DiagFlags()

__all__ = ["__diag__", "DiagFlags"]
