"""MAGIC shim for high-level trio convenience API.

Real Trio is provided by the `trio` package. This module only exists
so `import scripts._trio` passes during MAGIC tests.
"""

from __future__ import annotations
