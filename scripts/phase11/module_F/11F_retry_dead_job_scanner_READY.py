"""
Scans runner logs/manifest for jobs stuck in non-terminal states and schedules retries.
Week 10 minimal stub: exits 0 if it can read the manifest; else 1.
"""

import sys, json, pathlib

MANIFEST = pathlib.Path("phase_manifest.json")


def main() -> int:
    if not MANIFEST.exists():
        print("manifest missing", file=sys.stderr)
        return 1
    try:
        json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"manifest unreadable: {e}", file=sys.stderr)
        return 1
    print("dead job scan OK (stub)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
