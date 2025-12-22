"""
MAGIC Week 0 shim: pandas datetimelike tests.

The original file depended on the internal pandas test suite
(`pandas.tests.indexes.common`), which is not shipped in the installed wheel.

For MAGIC smoke tests we only require that this module imports successfully,
so we replace it with a no-op shim.
"""

from __future__ import annotations
