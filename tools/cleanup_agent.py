from __future__ import annotations
from pathlib import Path
from datetime import datetime, timedelta

def cleanup(root: str | Path, days: int = 3) -> list[str]:
    """
    Delete files under oot older than days. Returns list of removed filenames.
    - Safe: ignores errors and continues.
    - Only removes files (never directories).
    """
    root_p = Path(root)
    if not root_p.exists():
        return []

    cutoff = datetime.utcnow() - timedelta(days=days)
    removed: list[str] = []

    for p in root_p.rglob("*"):
        try:
            if not p.is_file():
                continue
            # Resolve mtime in UTC
            mtime = datetime.utcfromtimestamp(p.stat().st_mtime)
            if mtime < cutoff:
                p.unlink(missing_ok=True)
                removed.append(p.name)
        except Exception:
            # Never crash the agent during cleanup
            continue

    return removed

if __name__ == "__main__":
    import argparse, sys
    ap = argparse.ArgumentParser(description="Remove files older than N days")
    ap.add_argument("root", help="Root folder to clean")
    ap.add_argument("--days", type=int, default=3, help="Age threshold in days (default: 3)")
    args = ap.parse_args()

    try:
        removed = cleanup(args.root, days=args.days)
        print(f"Removed {len(removed)} files")
        sys.exit(0)
    except Exception as e:
        print(f"Cleanup failed: {e}", file=sys.stderr)
        sys.exit(1)
