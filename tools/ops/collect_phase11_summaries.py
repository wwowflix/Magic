from __future__ import annotations
import csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUM = ROOT / "tools" / "outputs" / "summaries"
OUT = ROOT / "outputs" / "reports" / "phase11_full_latest.tsv"
OUT.parent.mkdir(parents=True, exist_ok=True)

rows = []
for p in sorted(SUM.glob("phase11_module_*_summary_*.tsv")):
    m = re.search(r"phase11_module_([A-Z])_summary_(\d{8}_\d{6})", p.name)
    mod = m.group(1) if m else "?"
    ts = m.group(2) if m else ""
    with p.open("r", encoding="utf-8") as f:
        r = csv.reader(f, delimiter="\t")
        header = next(r, None)
        for script, status in r:
            rows.append((ts, mod, script, status))

rows.sort(reverse=True)  # newest first
seen = set()
dedup = []
for ts, mod, script, status in rows:
    key = (mod, script)
    if key in seen:
        continue
    seen.add(key)
    dedup.append((mod, script, status, ts))

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["Module", "Script", "Status", "Timestamp"])
    w.writerows(dedup)

print(f"Wrote: {OUT}")