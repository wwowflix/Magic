"""MAGIC shim for Altair transformed data helpers.

The original module imports Altair and Vegafusion. We replace it with
an empty shim to keep imports cheap and dependency-free.
"""

from __future__ import annotations
