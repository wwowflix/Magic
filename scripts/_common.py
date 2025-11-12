"""MAGIC-compatible common helpers.

This shim only provides tiny utilities needed for tests; it's safe to
import even if the original attrs/_common module is not present.
"""

from __future__ import annotations

import os
import sys
import pathlib
import tempfile
import importlib.util
from contextlib import contextmanager


def wrap_spec(spec):
    """Identity wrapper used in MAGIC environment.

    The original implementation tweaks importlib specs; for MAGIC we just
    return the spec unchanged so callers can still call this safely.
    """
    return spec


@contextmanager
def temporary_directory(prefix: str = "magic_"):
    """Yield a temporary directory as a pathlib.Path.

    Directory is removed automatically when the context exits.
    """
    with tempfile.TemporaryDirectory(prefix=prefix) as tmp:
        yield pathlib.Path(tmp)


def import_module_from_path(path: str | os.PathLike, module_name: str | None = None):
    """Minimal helper to import a module from a filesystem path."""
    path = os.fspath(path)
    if module_name is None:
        module_name = pathlib.Path(path).stem

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {module_name!r} from {path!r}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


__all__ = ["wrap_spec", "temporary_directory", "import_module_from_path"]
