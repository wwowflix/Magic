"""
MAGIC shim module for ``scripts._magics``.

Original code depended on IPython and vega-lite Jupyter integrations.
For the MAGIC project we only need this module to be *importable* so that
smoke tests and any indirect imports don’t fail.

This shim defines a minimal VegaLiteMagics class that raises a clear
RuntimeError if someone actually tries to use it.
"""

from __future__ import annotations

from typing import Any

try:
    # Real IPython magics (if IPython is installed in future)
    from IPython.core.magic import Magics, magics_class, line_cell_magic
except Exception:  # ImportError or any other failure
    # Fallback no-op shims so imports keep working
    class Magics:  # type: ignore[override]
        """Minimal base class stub used when IPython is not available."""
        pass

    def magics_class(cls: type) -> type:  # type: ignore[override]
        """Decorator stub: returns the class unchanged."""
        return cls

    def line_cell_magic(func):  # type: ignore[override]
        """Decorator stub: returns the function unchanged."""
        return func


@magics_class
class VegaLiteMagics(Magics):
    """Stub IPython magic for vega-lite.

    In this environment we don't provide real Jupyter integration.
    Attempting to call this will raise a clear RuntimeError.
    """

    @line_cell_magic
    def vegalite(self, line: str, cell: str | None = None) -> None:
        raise RuntimeError(
            "VegaLiteMagics is not usable in this environment; "
            "IPython / vega-lite Jupyter integration is not installed."
        )


__all__ = ["VegaLiteMagics"]
