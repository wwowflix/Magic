#!/usr/bin/env python
"""
MAGIC Week 0 – Import Diagnostic Scanner

Usage:
    python tools/magic_import_diagnose.py

What it does:
1. Detect *.py files that might SHADOW stdlib modules (socket, asyncio, abc, etc.).
2. Try importing each top-level module under `scripts/`:
   - prints [OK] or [FAIL] with the exception type + message.
3. Summary of counts at the end.

This is *read-only* and safe – it does not modify any files.
"""

from __future__ import annotations

import importlib
import os
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


# --------------------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------------------

# Names that are dangerous if you have files like `socket.py`, `queue.py`, etc.
STD_SHADOW_CANDIDATES = {
    "abc",
    "asyncio",
    "datetime",
    "email",
    "inspect",
    "importlib",
    "io",
    "json",
    "logging",
    "math",
    "os",
    "pathlib",
    "queue",
    "random",
    "re",
    "selectors",
    "socket",
    "ssl",
    "subprocess",
    "threading",
    "time",
    "typing",
    "unittest",
}

ROOT = Path(__file__).resolve().parent.parent  # E:\MAGIC
SCRIPTS_DIR = ROOT / "scripts"


@dataclass
class ImportResult:
    module: str
    ok: bool
    exc_type: Optional[str] = None
    exc_msg: Optional[str] = None


# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------


def print_header() -> None:
    print("=" * 80)
    print("MAGIC Week 0 – Import Diagnostic Scanner")
    print("=" * 80)
    print(f"Repo root: {ROOT}")
    print(f"Scripts dir: {SCRIPTS_DIR}")
    print()


def ensure_root_on_syspath() -> None:
    # Make sure ROOT (E:\MAGIC) is on sys.path[0]
    root_str = str(ROOT)
    if sys.path[0] != root_str:
        if root_str in sys.path:
            sys.path.remove(root_str)
        sys.path.insert(0, root_str)
    print(f"sys.path[0] = {sys.path[0]}")
    print()


def find_shadowing_files() -> List[Path]:
    """
    Look for any *.py in ROOT and scripts/ whose stem matches known stdlib names.
    """
    candidates: List[Path] = []

    for base in (ROOT, SCRIPTS_DIR):
        if not base.exists():
            continue
        for path in base.glob("*.py"):
            if path.name == "__init__.py":
                continue
            if path.stem in STD_SHADOW_CANDIDATES:
                candidates.append(path)

    return candidates


def scan_shadows() -> None:
    print("Step 1: Checking for files that shadow stdlib modules...")
    shadows = find_shadowing_files()
    if not shadows:
        print("  ✅ No obvious stdlib-shadowing files in ROOT/ or scripts/")
    else:
        print("  ⚠ Found potential stdlib shadows:")
        for p in sorted(shadows):
            print(f"    - {p.relative_to(ROOT)}")
        print("  If these are not intentional, consider renaming or moving them.")
    print()


def iter_scripts_modules() -> List[str]:
    """
    Discover top-level modules under scripts/.

    For each E:\MAGIC\scripts\foo.py, yields "scripts.foo".
    """
    modules: List[str] = []
    if not SCRIPTS_DIR.exists():
        print(f"WARNING: scripts dir does not exist: {SCRIPTS_DIR}")
        return modules

    for path in SCRIPTS_DIR.glob("*.py"):
        if path.name == "__init__.py":
            continue
        # Some files are support / backup, you can skip them if you want,
        # but for Week 0 it's useful to see everything.
        stem = path.stem
        modules.append(f"scripts.{stem}")

    return sorted(modules)


def try_import(module_name: str) -> ImportResult:
    try:
        importlib.invalidate_caches()
        importlib.import_module(module_name)
        return ImportResult(module=module_name, ok=True)
    except Exception as exc:  # noqa: BLE001
        exc_type = type(exc).__name__
        exc_msg = str(exc)
        return ImportResult(module=module_name, ok=False, exc_type=exc_type, exc_msg=exc_msg)


def scan_script_imports() -> List[ImportResult]:
    print("Step 2: Importing scripts.* modules...")
    results: List[ImportResult] = []

    modules = iter_scripts_modules()
    if not modules:
        print("  (No script modules found under scripts/)")
        return results

    for module_name in modules:
        result = try_import(module_name)
        if result.ok:
            print(f"  ✅ [OK]    {module_name}")
        else:
            print(f"  ❌ [FAIL]  {module_name} -> {result.exc_type}: {result.exc_msg}")
        results.append(result)

    print()
    return results


def summarize(results: List[ImportResult]) -> None:
    total = len(results)
    failed = sum(1 for r in results if not r.ok)
    ok = total - failed

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Total modules scanned: {total}")
    print(f"  ✅ OK:   {ok}")
    print(f"  ❌ FAIL: {failed}")
    print()

    if failed:
        print("Failing modules:")
        for r in results:
            if not r.ok:
                print(f"  - {r.module}: {r.exc_type}: {r.exc_msg}")
    else:
        print("All scripts.* modules imported successfully. 🎉")

    print("=" * 80)


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------


def main() -> None:
    print_header()
    ensure_root_on_syspath()
    scan_shadows()
    results = scan_script_imports()
    summarize(results)


if __name__ == "__main__":
    main()
