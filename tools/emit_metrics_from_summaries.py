#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from collections import defaultdict, Counter

__all__ = ["emit_metrics", "main"]


def emit_metrics(summaries_dir: str, out_dir: str) -> str:
    """
    Read all *.tsv files in `summaries_dir` (tab-delimited with 'Status' and 'Phase' columns,
    but we will also work if only 'Status' is present), aggregate counts, and write JSON to
    `out_dir/agent_metrics.json`. Returns the output file path as a string.
    """
    sdir = Path(summaries_dir)
    odir = Path(out_dir)
    odir.mkdir(parents=True, exist_ok=True)

    totals = Counter()
    by_phase = defaultdict(lambda: Counter())

    for tsv in sdir.glob("*.tsv"):
        with tsv.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                status = str(row.get("Status", "")).strip()
                phase = str(row.get("Phase", "")).strip()
                if not status:
                    continue
                totals[status] += 1
                if phase:
                    by_phase[phase][status] += 1

    payload = {
        "totals": dict(totals),
        "by_phase": {k: dict(v) for k, v in by_phase.items()},
    }

    out_path = odir / "agent_metrics.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(out_path)


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Emit runner metrics from summary TSVs")
    # ✨ defaults changed to what the test expects
    ap.add_argument("--summaries", default="outputs/summaries")
    ap.add_argument("--out", default="outputs/metrics")
    ns = ap.parse_args(argv)
    p = emit_metrics(ns.summaries, ns.out)
    print(f"[emit_metrics] wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
