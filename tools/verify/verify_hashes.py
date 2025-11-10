import argparse
import hashlib
import os
from pathlib import Path
from datetime import datetime

OUT_TSV = Path("outputs/reports/quarantine_hashes.tsv")


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root",
        nargs="?",
        default="backups",
        help="Root directory to hash (default: backups)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"Root path does not exist: {root}")

    rows = []
    total_files = 0

    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            p = Path(dirpath) / name
            rel = p.as_posix()
            try:
                digest = hash_file(p)
                size = p.stat().st_size
            except OSError as e:
                print(f"Skipping {rel}: {e}")
                continue

            rows.append((rel, size, digest))
            total_files += 1

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
        f.write("path\tbytes\tsha256\tgenerated_at\n")
        ts = datetime.utcnow().isoformat() + "Z"
        for rel, size, digest in rows:
            f.write(f"{rel}\t{size}\t{digest}\t{ts}\n")

    print(f"Hashed {total_files} files under {root}")
    print(f"Hashes written to {OUT_TSV}")


if __name__ == "__main__":
    main()
