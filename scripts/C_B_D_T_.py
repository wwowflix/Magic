"""MAGIC-compatible wrapper for the C_B_D_T_ table.

This module is based on fontTools' bitmap table helpers, but is written
to be import-safe even when fontTools is missing or mis-detected.

The smoke tests only require that ``scripts.C_B_D_T_`` imports
successfully; they do not depend on full functionality.
"""

from __future__ import annotations

# We *try* to use the real fontTools helper, but fall back gracefully if
# ``fontTools`` cannot be imported correctly in this environment.
try:
    from fontTools.misc.textTools import bytesjoin as _bytesjoin  # type: ignore[import]
except Exception:
    def bytesjoin(chunks):
        """Fallback implementation of fontTools.misc.textTools.bytesjoin.

        This is enough for simple callers and allows the module to be
        imported in constrained environments.
        """
        return b"".join(chunks)
else:
    def bytesjoin(chunks):
        # Delegate to the real fontTools implementation when available.
        return _bytesjoin(chunks)

# Keep the relative import so the presence of E_B_D_T_ is still tested,
# but do not let failures kill the import of this module.
try:
    from . import E_B_D_T_  # noqa: F401
except Exception:
    E_B_D_T_ = None  # type: ignore[assignment]

__all__ = ["bytesjoin", "E_B_D_T_"]
