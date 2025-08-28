from __future__ import annotations

from pathlib import Path
from typing import TypedDict, Dict, Iterable, Tuple
import argparse
import csv
import json


class Counts(TypedDict):
    ok: int
    fail: int
    total: int


def _empty() -> Counts:
    return {"ok": 0, "fail": 0, "total": 0}


def _add(c: Counts, status: str) -> None:
    c["total"] += 1
    s = status.upper()
    if s == "PASS":
        c["ok"] += 1
    elif s == "FAIL":
        c["fail"] += 1


def _iter_rows(tsv_path: Path) -> Iterable[dict[str, str]]:
    with tsv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            yield row


def summarize(tsv_paths: Iterable[Path]) -> Tuple[Counts, Dict[str, Counts]]:
    totals: Counts = _empty()
    by_phase: Dict[str, Counts] = {}

    for tsv in tsv_paths:
        for row in _iter_rows(tsv):
            phase = str(row.get("Phase", "")).strip()
            status = str(row.get("Status", "")).strip()
            _add(totals, status)
            bucket = by_phase.setdefault(phase, _empty())
            _add(bucket, status)
    return totals, by_phase


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--summary", type=Path, help="Path to a single TSV summary")
    g.add_argument("--summary-dir", type=Path, help="Directory with *.tsv summaries")
    p.add_argument(
        "--out-json",
        type=Path,
        default=Path("outputs/metrics/summary_counts.json"),
        help="Where to write the JSON summary",
    )
    args = p.parse_args(argv)

    if args.summary:
        tsvs = [args.summary]
    else:
        sdir: Path = args.summary_dir
        tsvs = sorted(sdir.glob("*.tsv"))

    totals, by_phase = summarize(tsvs)

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(
        json.dumps({"totals": totals, "by_phase": by_phase}, indent=2),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
