from __future__ import annotations

"""
Week 0 stub for `scripts.cmdstan_args`.

The original module integrates with cmdstanpy and uses internal details
like `_TMPDIR`. For MAGIC Week 0, we only need this module to import
cleanly, so we provide a minimal configuration holder and a TMPDIR
helper without any external dependencies.
"""

from dataclasses import dataclass
from typing import Any, Mapping, Optional


TMPDIR: Optional[str] = None


def get_tmpdir() -> Optional[str]:
    """Return the configured temporary directory for CmdStan, if any."""
    return TMPDIR


def set_tmpdir(path: str) -> None:
    """Set the temporary directory used in this stub."""
    global TMPDIR
    TMPDIR = path


@dataclass
class CmdStanArgs:
    """
    Minimal stand-in for the argument container used by CmdStan.

    Only a subset of fields is provided for Week 0 smoke tests.
    """
    model_name: str
    data: Optional[Mapping[str, Any]] = None
    seed: Optional[int] = None
    chains: int = 4
    iter_sampling: int = 1000
    iter_warmup: int = 1000
    output_dir: Optional[str] = None
