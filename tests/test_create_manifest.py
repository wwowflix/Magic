#!/usr/bin/env python3
"""
create_manifest.py

Discovers *_READY.py scripts in the repository and writes a JSON manifest.

Fields per entry:
- path   : POSIX-style relative path from repo root (e.g., "scripts/phase11/module_a/11A_task_READY.py")
- phase  : int if detected from "phase<NUM>" in the path, else null
- module : e.g., "module_a" if present, else best-effort token
- name   : script filename (stem)

Usage:
  python tools/create_manifest.py <root_dir> <out_path>
  python tools/create_manifest.py --root . --out phase_manifest.json
  python -m tools.create_manifest --root . --out phase_manifest.json

This module also exposes a library function:
  generate_manifest(root_dir: str, out_path: str, **kwargs) -> dict
"""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import Iterable, List, Dict, Any, Optional

READY_GLOB_DEFAULTS = ["*_READY.py"]
EXCLUDE_DIRS_DEFAULT = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "htmlcov",
    ".pytest_cache",
}

PHASE_RE = re.compile(r"(?:^|[/\\])phase(\d+)(?:[/\\]|$)", re.IGNORECASE)
MODULE_RE = re.compile(r"(?:^|[/\\])(module_[a-z0-9]+)(?:[/\\]|$)", re.IGNORECASE)


def _is_excluded(path: Path, exclude_dirs: Iterable[str]) -> bool:
    parts = {p.name.lower() for p in path.parents}
    parts.add(path.name.lower())
    exclude_lower = {d.lower() for d in exclude_dirs}
    return any(d in parts for d in exclude_lower)


def _posix_relpath(path: Path, root: Path) -> str:
    """Return the relative path using forward slashes for portability."""
    return path.relative_to(root).as_posix()


def _detect_phase(rel_posix: str) -> Optional[int]:
    m = PHASE_RE.search(rel_posix)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None


def _detect_module(rel_posix: str) -> Optional[str]:
    m = MODULE_RE.search(rel_posix)
    return m.group(1) if m else None


def discover_ready_scripts(
    root_dir: Path,
    ready_globs: Iterable[str] = READY_GLOB_DEFAULTS,
    search_base: Optional[Path] = None,
    exclude_dirs: Iterable[str] = EXCLUDE_DIRS_DEFAULT,
) -> List[Path]:
    """Find *_READY.py scripts under search_base (or scripts/ under root by default)."""
    root_dir = root_dir.resolve()
    if search_base is None:
        search_base = root_dir / "scripts"
    search_base = search_base.resolve()

    if not search_base.exists():
        return []

    results: List[Path] = []
    for pat in ready_globs:
        for p in search_base.rglob(pat):
            if p.is_file():
                # skip excluded directories anywhere in the path
                if any(part.lower() in {d.lower() for d in exclude_dirs} for part in p.parts):
                    continue
                results.append(p.resolve())

    # stable ordering: phase then module then filename
    def sort_key(path: Path):
        rel = _posix_relpath(path, root_dir)
        return (
            _detect_phase(rel) or 9999,
            _detect_module(rel) or "",
            rel,
        )

    results.sort(key=sort_key)
    return results


def build_manifest_dict(root_dir: Path, files: Iterable[Path]) -> Dict[str, Any]:
    """Create the manifest dictionary from discovered files."""
    root_dir = root_dir.resolve()
    entries: List[Dict[str, Any]] = []

    for f in files:
        rel = _posix_relpath(f, root_dir)
        entries.append(
            {
                "path": rel,
                "phase": _detect_phase(rel),
                "module": _detect_module(rel),
                "name": f.stem,
            }
        )

    return {
        "root": str(root_dir.as_posix()),
        "count": len(entries),
        "entries": entries,
        "version": 1,
    }


def generate_manifest(
    root_dir: str,
    out_path: str,
    *,
    include: Iterable[str] = READY_GLOB_DEFAULTS,
    exclude_dirs: Iterable[str] = EXCLUDE_DIRS_DEFAULT,
    search_base: Optional[str] = None,
    pretty: bool = True,
) -> Dict[str, Any]:
    """
    High-level API: discover *_READY.py and write manifest JSON.

    Returns the manifest dict that was written.
    """
    root = Path(root_dir).resolve()
    if search_base:
        search_root = Path(search_base).resolve()
    else:
        search_root = root / "scripts"

    files = discover_ready_scripts(
        root, ready_globs=include, search_base=search_root, exclude_dirs=exclude_dirs
    )
    manifest = build_manifest_dict(root, files)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        if pretty:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
        else:
            json.dump(manifest, fh, separators=(",", ":"), ensure_ascii=False)
            fh.write("\n")
    return manifest


# Backwards-compatible entry points for tests/tools that might call different names
create_manifest = generate_manifest  # alias
write_manifest = generate_manifest  # alias
build_manifest = generate_manifest  # alias


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a manifest of *_READY.py scripts.")
    p.add_argument("root", nargs="?", default=".", help="Repo root (default: .)")
    p.add_argument(
        "out",
        nargs="?",
        default="phase_manifest.json",
        help="Output JSON path (default: phase_manifest.json)",
    )
    p.add_argument("--root", dest="root_kw", help="Explicit repo root (overrides positional)")
    p.add_argument("--out", dest="out_kw", help="Explicit output path (overrides positional)")
    p.add_argument(
        "--include",
        nargs="*",
        default=READY_GLOB_DEFAULTS,
        help="Glob(s) to include (default: *_READY.py)",
    )
    p.add_argument(
        "--exclude-dirs",
        nargs="*",
        default=list(EXCLUDE_DIRS_DEFAULT),
        help="Directories to exclude by name",
    )
    p.add_argument(
        "--search-base",
        default=None,
        help="Override search base (default: <root>/scripts)",
    )
    p.add_argument("--compact", action="store_true", help="Write compact JSON (no pretty indent)")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    ns = _parse_args(argv)
    root = ns.root_kw or ns.root
    out = ns.out_kw or ns.out
    try:
        generate_manifest(
            root,
            out,
            include=ns.include,
            exclude_dirs=ns.exclude_dirs,
            search_base=ns.search_base,
            pretty=not ns.compact,
        )
    except Exception as e:
        print(f"[create_manifest] ERROR: {e}")
        return 1
    print(f"[create_manifest] Wrote manifest -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
