"""MAGIC shim for Click termui implementation.

We replace the heavy terminal UI helpers with a tiny stub so that
`scripts._termui_impl` imports cleanly.
"""

from __future__ import annotations
