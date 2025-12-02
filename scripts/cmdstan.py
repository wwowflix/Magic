from __future__ import annotations

# Week 0 stub for `scripts.cmdstan`.
# The original code integrates with cmdstanpy and the external CmdStan
# installation. For MAGIC smoke-import tests we only need this module
# to import cleanly, not to actually manage CmdStan.

from typing import Optional

CMDSTAN_PATH: Optional[str] = None


def get_cmdstan_path() -> Optional[str]:
    """Return the configured CmdStan path, or None in the Week 0 stub."""
    return CMDSTAN_PATH


def set_cmdstan_path(path: str) -> None:
    """Set the CmdStan path in this stub module."""
    global CMDSTAN_PATH
    CMDSTAN_PATH = path


def install_cmdstan(*_args, **_kwargs) -> Optional[str]:
    """Pretend to install CmdStan and return the (stub) path."""
    return CMDSTAN_PATH
