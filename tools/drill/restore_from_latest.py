from __future__ import annotations
import hashlib, json, os, shutil, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
BACKUPS = ROOT / "backups"
RESTORE_TARGET = ROOT
MANIFEST_NAME = "manifest.json"

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def latest_snapshot() -> Path:
    snaps = sorted([p for p in BACKUPS.iterdir() if p.is_dir()],
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not snaps:
        raise SystemExit("No backup snapshots found.")
    return snaps[0]

def restore_dir(src: Path, dst: Path) -> None:
    for root, dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for name in files:
            s = Path(root) / name
            d = dst / rel / name
            shutil.copy2(s, d)

def verify_hashes(manifest_path: Path, base: Path):
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches = []
    for rel, expected in data.get("files", {}).items():
        p = base / rel
        if not p.exists():
            mismatches.append((rel, expected, "MISSING"))
            continue
        actual = sha256(p)
        if actual != expected:
            mismatches.append((rel, expected, actual))
    return mismatches

def main() -> None:
    snap = latest_snapshot()
    print(f"[restore] using snapshot: {snap.name} ({datetime.fromtimestamp(snap.stat().st_mtime)})")
    restore_dir(snap / "payload", RESTORE_TARGET)
    manifest = snap / MANIFEST_NAME
    if manifest.exists():
        mismatches = verify_hashes(manifest, RESTORE_TARGET)
        if mismatches:
            print("[verify] hash mismatches:")
            for rel, exp, act in mismatches[:20]:
                print(f" - {rel}: expected {exp}, got {act}")
            sys.exit(2)
        else:
            print("[verify] all hashes match.")
    else:
        print("[warn] no manifest.json found; skipped hash verification.")

if __name__ == "__main__":
    main()
