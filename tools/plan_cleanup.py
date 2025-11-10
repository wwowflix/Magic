import os
import json
from pathlib import Path
from datetime import datetime

ROOTS = [
    Path("outputs"),
    Path("logs"),
    Path("tmp"),
]

EXCLUSIONS_FILE = Path("tools/config/cleanup_exclusions.json")
OUT_TSV = Path("outputs/reports/cleanup_plan.tsv")


def load_exclusions() -> list[str]:
    if not EXCLUSIONS_FILE.exists():
        return []

    data = json.loads(EXCLUSIONS_FILE.read_text(encoding="utf-8"))
    paths = data.get("exclude_paths", [])
    # normalise to forward-slash for comparison
    return [p.replace("\\", "/") for p in paths]


def is_excluded_path(path_str: str, exclusions: list[str]) -> bool:
    # path_str is already in forward-slash form
    for ex in exclusions:
        if path_str.startswith(ex):
            return True
    return False


def main() -> None:
    exclusions = load_exclusions()

    rows: list[tuple[str, int, float, str, str]] = []
    total_bytes = 0

    for root in ROOTS:
        if not root.exists():
            continue

        root_str = root.as_posix()

        def onerror(err: OSError) -> None:
            # Just skip directories that cause errors
            print(f"Skipping problematic path under {root_str}: {err}")

        for dirpath, dirnames, filenames in os.walk(root, onerror=onerror):
            dir_rel = Path(dirpath).as_posix()

            # If this whole directory is excluded, prune it and continue
            if is_excluded_path(dir_rel + "/", exclusions):
                dirnames[:] = []  # don't descend further
                continue

            for name in filenames:
                p = Path(dirpath) / name
                rel = p.as_posix()

                if is_excluded_path(rel, exclusions):
                    continue

                try:
                    stat = p.stat()
                except OSError:
                    # file disappeared or is unreadable
                    continue

                size = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
                total_bytes += size
                size_mb = round(size / (1024 * 1024), 3)
                rows.append((rel, size, size_mb, mtime, root_str))

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
        f.write("path\tbytes\tmb\tmodified_iso\troot\n")
        for path, b, mb, mtime, root_str in rows:
            f.write(f"{path}\t{b}\t{mb}\t{mtime}\t{root_str}\n")

    total_gb = total_bytes / (1024 * 1024 * 1024)
    print(f"Planned cleanup candidates: {len(rows)} files")
    print(f"Total candidate size ~ {total_gb:.3f} GB")
    print(f"Plan written to {OUT_TSV}")


if __name__ == "__main__":
    main()
