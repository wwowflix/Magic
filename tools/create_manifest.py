from __future__ import annotations
import argparse, json, sys
from pathlib import Path

# Legacy constant some tests import
SCRIPTS_ROOT = (Path(__file__).resolve().parents[1] / "scripts")

# ---------------- Core discovery ----------------

def _iter_ready_files(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*_READY.py"):
        yield p

def _entry_raw_from_path(p: Path) -> dict:
    """Modern entry: keep phase/module as strings, e.g. 'phase11', 'module_B'."""
    parts = p.parts
    try:
        idx = parts.index("scripts")
        phase_name  = parts[idx + 1] if len(parts) > idx + 1 else "unknown"
        module_name = parts[idx + 2] if len(parts) > idx + 2 else "unknown"
    except ValueError:
        phase_name, module_name = "unknown", "unknown"
    return {
        "phase": phase_name,
        "module": module_name,
        "path": str(p.as_posix()),
        "filename": p.name,
    }

def _normalize_phase_module(phase_name: str, module_name: str) -> tuple[int, str]:
    # phaseX -> int(X), else -1
    p = -1
    s = phase_name.lower()
    if s.startswith("phase"):
        try:
            p = int(s[5:])
        except ValueError:
            p = -1
    # module_Y -> "y" (lowercase), else "unknown"
    m = "unknown"
    t = module_name.lower()
    if t.startswith("module_"):
        suf = module_name.split("_", 1)[1].strip()
        m = (suf or "unknown").lower()
    return p, m

def _entry_norm_from_path(p: Path) -> dict:
    """Legacy entry: normalize to phase:int, module:token."""
    parts = p.parts
    try:
        idx = parts.index("scripts")
        phase_name  = parts[idx + 1] if len(parts) > idx + 1 else "unknown"
        module_name = parts[idx + 2] if len(parts) > idx + 2 else "unknown"
    except ValueError:
        phase_name, module_name = "unknown", "unknown"
    phase_int, module_tok = _normalize_phase_module(phase_name, module_name)
    return {
        "phase": phase_int,
        "module": module_tok,
        "path": str(p.as_posix()),
        "filename": p.name,
    }

def generate_manifest(scripts_root: Path) -> list[dict]:
    """Modern: return entries with phase/module as strings."""
    files = sorted(_iter_ready_files(scripts_root))
    entries = [_entry_raw_from_path(p) for p in files]
    return sorted(entries, key=lambda x: (x["phase"], x["module"], x["filename"]))

# ---------------- CLI ----------------

def main(argv: list[str] | None = None) -> int:
    """
    Flags:
      --scripts-root ./scripts  --out ./phase_manifest.json
    Positionals:
      <scripts_root> [out_path]

    Writes:
      - list [] when NOT using positionals (e.g., tests call cm.main() directly)
      - dict {"count": N, "entries": [...]} when BOTH positionals are provided
    """
    parser = argparse.ArgumentParser(prog="create_manifest")
    parser.add_argument("--scripts-root", default=str(Path.cwd() / "scripts"))
    parser.add_argument("--out",          default=str(Path.cwd() / "phase_manifest.json"))
    parser.add_argument("scripts_root_pos", nargs="?", help="Optional positional scripts_root")
    parser.add_argument("out_pos",         nargs="?", help="Optional positional output path")
    parser.add_argument("--compact", action="store_true", help="Write compact JSON (no pretty indent)")

    # tolerate unknown args (pytest adds its own)
    args, _unknown = parser.parse_known_args(argv)

    # Only honor positionals if BOTH are provided (avoids pytest sys.argv pollution)
    use_positional = bool(args.scripts_root_pos and args.out_pos)

    scripts_root = Path(args.scripts_root_pos if use_positional else args.scripts_root).resolve()
    out_path     = Path(args.out_pos         if use_positional else args.out).resolve()

    manifest = generate_manifest(scripts_root)

    payload = {"count": len(manifest), "entries": manifest} if use_positional else manifest
    indent = None if args.compact else 2

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=indent)

    print(f"[create_manifest] Wrote {len(manifest)} entries to {out_path}")
    return 0

# ---------------- Legacy compatibility shims ----------------

def discover(root: Path | str) -> list[Path]:
    """Return *_READY.py paths under <root>/scripts if it exists, otherwise under <root>."""
    base = Path(root)
    base = base / "scripts" if (base / "scripts").exists() else base
    return sorted(_iter_ready_files(base)) if base.exists() else []

def build(*args) -> list[dict]:
    """
    Accept either:
      build(files)
      build(root, files)
    Returns list of *normalized* entry dicts (phase:int, module:token).
    """
    if len(args) == 1:
        files = args[0]
    elif len(args) == 2:
        _root, files = args
    else:
        raise TypeError("build() expects (files) or (root, files)")
    entries = [_entry_norm_from_path(Path(f)) for f in files]
    return sorted(entries, key=lambda x: (x["phase"], x["module"], x["filename"]))

def build_manifest(*args) -> dict:
    """
    Accepts:
      build_manifest(files)
      build_manifest(root, files)
    Returns: {"count": N, "entries": [...]}
    """
    entries = build(*args)
    return {"count": len(entries), "entries": entries}

if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
