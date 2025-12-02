from __future__ import annotations

"""
Week 0 stub for `scripts.compilation`.

The original module integrates with `cmdstanpy` and external C++ toolchains
to compile Stan models. For MAGIC Week 0 smoke-import tests we only need
this module to import cleanly; no actual compilation is required.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Union

Logger = logging.Logger
PathLike = Union[str, Path]
JsonDict = Dict[str, Any]


def get_logger(name: str = "cmdstan_stub") -> Logger:
    """Return a basic logger instance in the Week 0 stub."""
    return logging.getLogger(name)


def compile_stan_file(
    stan_file: PathLike,
    *,
    output_dir: Optional[PathLike] = None,
    overwrite: bool = False,
    **_: Any,
) -> Path:
    """
    Pretend to compile a Stan file and return a dummy Path.

    In the Week 0 stub, we simply return a Path object pointing to where
    the compiled binary would live, without actually doing anything.
    """
    stan_path = Path(stan_file)
    if output_dir is not None:
        out_dir = Path(output_dir)
    else:
        out_dir = stan_path.parent
    # Fake compiled binary name (no actual file is created).
    return out_dir / (stan_path.stem + "_stub.exe")


def show_compiler_info() -> None:
    """No-op helper for Week 0 stub."""
    return None
