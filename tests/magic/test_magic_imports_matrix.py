from __future__ import annotations

import importlib
import pathlib
from typing import List
import pytest

# MAGIC matrix test for *_READY.py scripts

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"

CANDIDATE_MODULES: List[str] = []

for path in SCRIPTS_DIR.rglob("*_READY.py"):
    # Skip dunder files like __init__ etc.
    if path.name.startswith("__"):
        continue

    rel = path.relative_to(ROOT)

    # 🔹 SKIP hidden / dot-directories like .github, .something
    if any(part.startswith(".") for part in rel.parts):
        continue

    # Build module path: scripts.foo.bar.my_script_READY
    mod_path = rel.with_suffix("")
    mod_name = ".".join(mod_path.parts)

    # Ensure it starts with "scripts."
    if not mod_name.startswith("scripts."):
        continue

    CANDIDATE_MODULES.append(mod_name)

# Deduplicate & sort for stable order
CANDIDATE_MODULES = sorted(set(CANDIDATE_MODULES))


@pytest.mark.parametrize("module_name", CANDIDATE_MODULES)
def test_magic_ready_scripts_import_cleanly(module_name: str) -> None:
    """
    Global safety net:
    - Every *_READY.py under scripts/ (excluding dot-dirs) must import cleanly.
    """
    mod = importlib.import_module(module_name)
    assert mod is not None, f"Import failed for {module_name!r}"


def test_magic_import_list_not_empty() -> None:
    """Sanity check so this test doesn't silently do nothing."""
    assert CANDIDATE_MODULES, "No *_READY.py scripts were discovered."
