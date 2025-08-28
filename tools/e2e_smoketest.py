from __future__ import annotations
import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple


def check_rows(
    rows: List[Dict[str, Any]], logs_root: Path
) -> Tuple[Dict[str, int], List[Dict[str, object]], bool]:
    totals: Counter[str] = Counter()
    checked: List[Dict[str, object]] = []
    ok = True
    for r in rows:
        status = str(r.get("status", "")).upper()
        if status:
            totals[status] += 1
        lp = r.get("log_path")
        if lp:
            p = logs_root / str(lp)
            ex = p.exists()
            ok = ok and ex
            checked.append({"log_path": str(p), "exists": ex})
        else:
            checked.append({"log_path": None, "exists": None})
    return dict(totals), checked, ok


def load_tsv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="E2E smoketest for MAGIC runner summaries")
    ap.add_argument("--summary", required=True)
    ap.add_argument("--logs-root", default="outputs/logs")
    args = ap.parse_args(argv)
    totals, checked, ok = check_rows(load_tsv(Path(args.summary)), Path(args.logs_root))
    print("Totals:", totals)
    miss = [x for x in checked if x["exists"] is False]
    if miss:
        print(f"Missing logs: {len(miss)}")
        for m in miss[:10]:
            print("  -", m["log_path"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
