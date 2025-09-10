import csv
import glob
import json
import os
import pathlib
import re
from datetime import datetime

ROOT = r"D:\MAGIC"
SCRIPTS = os.path.join(ROOT, "scripts")
OUTDIR = os.path.join(ROOT, "outputs", "reports")
os.makedirs(OUTDIR, exist_ok=True)


def exists_any(patterns):
    for p in patterns:
        if any(glob.iglob(p, recursive=True)):
            return True
    return False


def count_files(patterns):
    c = 0
    for p in patterns:
        c += sum(1 for _ in glob.iglob(p, recursive=True))
    return c


def newest_file(patterns):
    newest = None
    for p in patterns:
        for f in glob.iglob(p, recursive=True):
            try:
                ts = os.path.getmtime(f)
                if newest is None or ts > newest[0]:
                    newest = (ts, f)
            except OSError:
                pass
    if newest:
        return datetime.fromtimestamp(newest[0]).strftime("%Y-%m-%d %H:%M"), newest[1]
    return "", ""


def load_manifest_paths():
    p = os.path.join(ROOT, "phase_manifest.json")
    if not os.path.exists(p):
        return None, 0
    try:
        data = json.load(open(p, "r", encoding="utf-8"))
        # accept heterogeneous schemas
        items = []
        for it in data:
            fn = it.get("FinalFilename") or it.get("filename") or it.get("path") or ""
            if fn:
                items.append(fn)
        return items, len(items)
    except Exception:
        return None, 0


def ready_counts():
    rows = []
    total = 0
    for p in pathlib.Path(SCRIPTS).rglob("*_READY.py"):
        total += 1
        rel = p.relative_to(SCRIPTS).as_posix()
        m = re.match(r"phase(\d+)/(module_[A-Za-z])/", rel)
        phase = f"phase{m.group(1)}" if m else "unknown"
        module = m.group(2) if m else "unknown"
        rows.append((phase, module, rel))
    # aggregate
    agg = {}
    for phase, module, _ in rows:
        agg.setdefault((phase, module), 0)
        agg[(phase, module)] += 1
    # write per phase/module table
    path = os.path.join(OUTDIR, "phase_file_counts.tsv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["Phase", "Module", "READY_Count"])
        for (phase, module), n in sorted(agg.items()):
            w.writerow([phase, module, n])
    return total, path


def status(ok, partial=False):
    if ok and not partial:
        return "✅"
    if partial:
        return "⚠"
    return "❌"


manifest_items, manifest_total = load_manifest_paths()
ready_total, phase_counts_path = ready_counts()

# Indicators for each week (heuristics aligned to your roadmap)
indicators = {
    # Week 1 – Scaffold & Inventory
    ("1", "Inventory all scripts"): exists_any(
        [os.path.join(SCRIPTS, "**", "*_READY.py")]
    ),
    ("1", "Manifest present"): os.path.exists(
        os.path.join(ROOT, "phase_manifest.json")
    ),
    ("1", "Runner foundation present"): exists_any(
        [os.path.join(ROOT, "self_healing_runner*.py")]
    ),
    ("1", "Placeholders auto-created"): exists_any(
        [os.path.join(SCRIPTS, "**", "*.py")]
    ),  # heuristic
    # Week 2 – Logging & Retry
    ("2", "Logs folder exists"): os.path.isdir(os.path.join(ROOT, "outputs", "logs")),
    ("2", "Summary TSVs exist"): exists_any(
        [os.path.join(ROOT, "outputs", "**", "*.tsv")]
    ),
    # Week 3 – Self-healing remediations
    ("3", "Wire-Joiner/auto-remediation tool"): exists_any(
        [os.path.join(ROOT, "tools", "wire_joiner.py")]
    ),
    # Week 4 – CI/CD & Notifications
    ("4", "CI workflow present"): exists_any(
        [os.path.join(ROOT, ".github", "workflows", "*.yml")]
    ),
    ("4", "Tests present"): exists_any([os.path.join(ROOT, "tests", "**", "*.py")]),
    # Week 5 – Module integration
    ("5", "Phase 11 module runs/logs"): exists_any(
        [
            os.path.join(ROOT, "outputs", "logs", "phase11*", "**", "*.log"),
            os.path.join(ROOT, "outputs", "**", "phase11*summary*.tsv"),
        ]
    ),
    # Week 6 – Bulk cleanup & remediation
    ("6", "Scan reports exist"): exists_any(
        [
            os.path.join(ROOT, "outputs", "scan_report*.txt"),
            os.path.join(ROOT, "outputs", "scan_report*.csv"),
            os.path.join(ROOT, "outputs", "wire_joiner", "*.tsv"),
        ]
    ),
    # Week 7 – CI hardening / pre-commit
    ("7", "Pre-commit configured"): os.path.exists(
        os.path.join(ROOT, ".pre-commit-config.yaml")
    ),
    # Week 8 – Metrics & Dashboard
    ("8", "Metrics emitted"): exists_any(
        [
            os.path.join(ROOT, "outputs", "**", "*metrics*.json"),
            os.path.join(ROOT, "outputs", "**", "*metrics*.tsv"),
        ]
    ),
    # Week 9 – Nightly / Stress
    ("9", "Nightly all-phases logs"): exists_any(
        [os.path.join(ROOT, "outputs", "nightly_allphases_*.log")]
    ),
    ("9", "Backups exist"): os.path.isdir(os.path.join(ROOT, "backups")),
    # Week 10 – Scale & Failover
    ("10", "Parallel exec/config present"): exists_any(
        [
            os.path.join(ROOT, "tools", "*parallel*.py"),
            os.path.join(ROOT, "self_healing_runner_v5.py"),
        ]
    ),
    # Week 11 – Shield modules (A–C done)
    ("11", "Phase 11 A–C scripts exist"): exists_any(
        [os.path.join(SCRIPTS, "phase11", "module_*", "*_READY.py")]
    ),
    # Week 12+ – Remaining Shield + Cloud
    ("12", "Cloud/remote backup configs"): exists_any(
        [
            os.path.join(ROOT, "tools", "*backup*.py"),
            os.path.join(ROOT, "tools", "*backup*.ps1"),
        ]
    ),
}

# Build progress table (TSV)
prog_tsv = os.path.join(OUTDIR, "progress_report.tsv")
with open(prog_tsv, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["Week", "Checkpoint", "Status", "Evidence/Note"])
    for (wk, name), ok in sorted(
        indicators.items(), key=lambda x: (int(x[0][0]), x[0][1])
    ):
        ev_dt, ev_file = (
            newest_file([os.path.join(ROOT, "**", "*")]) if ok else ("", "")
        )
        w.writerow([wk, name, status(ok), ev_file])

# High-level summary markdown
summary_md = os.path.join(OUTDIR, "progress_summary.md")

# Compute useful counts
phase11_files = count_files([os.path.join(SCRIPTS, "phase11", "**", "*_READY.py")])
nightly_count = count_files([os.path.join(ROOT, "outputs", "nightly_allphases_*.log")])
scan_reports = count_files(
    [
        os.path.join(ROOT, "outputs", "scan_report*.txt"),
        os.path.join(ROOT, "outputs", "scan_report*.csv"),
    ]
)

with open(summary_md, "w", encoding="utf-8") as f:
    f.write(
        f"# MAGIC Progress Summary ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
    )
    f.write(f"- READY scripts total: **{ready_total}**\n")
    if manifest_items is not None:
        f.write(
            f"- Manifest entries: **{manifest_total}**  → delta: **{ready_total - manifest_total}**\n"
        )
    else:
        f.write("- Manifest: **not found** (phase_manifest.json)\n")
    f.write(f"- Phase 11 READY files: **{phase11_files}**\n")
    f.write(f"- Nightly all-phases logs: **{nightly_count}**\n")
    f.write(f"- Scan reports found: **{scan_reports}**\n\n")

    f.write("## Week-by-Week\n\n")
    # Rollup per week
    by_week = {}
    for (wk, name), ok in indicators.items():
        by_week.setdefault(wk, []).append((name, ok))
    for wk in sorted(by_week, key=lambda x: int(x)):
        entries = by_week[wk]
        total = len(entries)
        done = sum(1 for _, ok in entries if ok)
        part = 0
        st = "✅" if done == total and total > 0 else ("⚠" if done > 0 else "❌")
        f.write(f"**Week {wk}**: {st} ({done}/{total})\n\n")
        for name, ok in entries:
            f.write(f"- {status(ok)} {name}\n")
        f.write("\n")

print(f"Wrote {prog_tsv}")
print(f"Wrote {summary_md}")
print(f"Wrote {phase_counts_path}")
