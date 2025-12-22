from __future__ import annotations

"""
MAGIC Week 0 shim for setuptools-style `egg_info` command.

Goals:
- Let `import scripts.egg_info` succeed without SyntaxError.
- Avoid importing setuptools/distutils or touching the filesystem at import time.
- Provide a tiny, harmless placeholder API for Week 0 only.
"""

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class DistributionMetadata:
    """
    Extremely small stand-in for distribution metadata.

    Real setuptools has a huge metadata model. In Week 0, we just need
    something lightweight so other code can hold a reference if needed.
    """
    name: str = "magic-placeholder"
    version: str = "0.0.0"
    summary: str = ""
    home_page: str = ""
    author: str = ""
    author_email: str = ""
    license: str = ""


class EggInfoCommand:
    """
    Tiny no-op replacement for `setuptools.command.egg_info.egg_info`.

    Week 0 rules:
    - Do not write any files.
    - Do not depend on setuptools internals.
    - Be safe to import in any environment.
    """

    def __init__(self, dist: Optional[DistributionMetadata] = None) -> None:
        self.distribution: DistributionMetadata = dist or DistributionMetadata()
        self.egg_base: Optional[str] = None
        self.egg_info: Optional[str] = None
        self.outputs: List[str] = []

    def initialize_options(self) -> None:
        """Week 0: do nothing."""
        ...

    def finalize_options(self) -> None:
        """Week 0: do nothing."""
        ...

    def run(self) -> None:
        """
        Week 0: pretend to generate egg-info metadata.

        In the real implementation this would create a directory,
        write PKG-INFO and assorted metadata files. For Week 0 we
        deliberately avoid filesystem writes and just leave `outputs`
        empty.
        """
        self.outputs = []

    def get_outputs(self) -> List[str]:
        """
        Return the list of generated files.

        Week 0: always an empty list.
        """
        return list(self.outputs)


__all__ = [
    "DistributionMetadata",
    "EggInfoCommand",
]
