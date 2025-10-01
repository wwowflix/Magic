#!/usr/bin/env python
# rediscover_magic.py
import argparse
import csv
import json
import math
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_MARKERS = {
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "Pipfile",
    ".git",
    "README.md",
    "README.rst",
    "README.txt",
    "LICENSE",
    ".venv",
    "venv",
    "env",
    "tox.ini",
    "pytest.ini",
}
DEFAULT_EXCLUDES = {
    ".git",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    ".mypy_cache",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "site-packages",
    "env",
    "venv",
    ".venv",
}
MAGIC_HINTS = (
    "magic",
    "self_healing",
    "runner",
    "orchestrator",
    "_READY",
    "failover",
    "audit",
    "phase",
    "scribe",
)


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def analyze_py_file(path: Path):
    text = safe_read_text(path)
    loc = text.count("\n") + 1 if text else 0
    # cheap function/class/import counters (fast + tolerant)
    fn = len(re.findall(r"^\s*def\s+\w+\(", text, flags=re.M))
    cl = len(re.findall(r"^\s*class\s+\w+\(", text, flags=re.M))
    im = len(
        re.findall(
            r"^\s*(?:from\s+[\w\.]+\s+import|import\s+[\w\.]+)", text, flags=re.M
        )
    )
    # module docstring-ish line (first non-empty comment/string)
    doc = None
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith('"""') or s.startswith("'''"):
            doc = s.strip("\"'")[:160]
            break
        if s.startswith("#"):
            doc = s.lstrip("# ").strip()[:160]
            break
        break
    # collect top-level imports (names only, rough)
    imports = []
    for m in re.finditer(r"^\s*import\s+([A-Za-z0-9_\.]+)", text, flags=re.M):
        imports.extend([p.split(".")[0] for p in m.group(1).split(",")])
    for m in re.finditer(r"^\s*from\s+([A-Za-z0-9_\.]+)\s+import", text, flags=re.M):
        imports.append(m.group(1).split(".")[0])
    return {"loc": loc, "functions": fn, "classes": cl, "imports": imports, "doc": doc}


def find_project_root(start: Path, cache):
    # nearest ancestor that has a marker, else top folder under drive
    p = start if start.is_dir() else start.parent
    cur = p
    while True:
        if cur in cache:
            return cache[cur]
        has_marker = any((cur / m).exists() for m in PROJECT_MARKERS)
        if has_marker:
            cache[p] = cur
            return cur
        if cur.parent == cur:
            cache[p] = p
            return p
        cur = cur.parent


def magic_score(stats):
    # recency (0..1) via 180d half-life-ish
    days = stats.get("days_since_last", 365.0)
    recency = math.exp(-days / 180.0)
    size = min(10.0, stats.get("py_files", 0) / 5.0)
    loc = min(6.0, stats.get("total_loc", 0) / 1000.0)
    has_readme = 5.0 if stats.get("has_readme") else 0.0
    has_reqs = 8.0 if stats.get("has_reqs") else 0.0
    has_tests = 6.0 if stats.get("tests") else 0.0
    hint = 0.0
    for k in (
        "magic",
        "runner",
        "ready",
        "orchestrator",
        "failover",
        "audit",
        "phase",
        "self_healing",
    ):
        if stats.get(f"hint_{k}"):
            hint += 3.0
    hint = min(hint, 15.0)
    return round(
        40 * recency + size + loc + has_readme + has_reqs + has_tests + hint, 2
    )


def main():
    ap = argparse.ArgumentParser(
        description="Scan drive and rediscover Python projects."
    )
    ap.add_argument(
        "--root", nargs="+", default=[r"D:\MAGIC"], help="Root folder(s) to scan"
    )
    ap.add_argument(
        "--out", default=r"D:\MAGIC\outputs\rediscover", help="Output folder"
    )
    ap.add_argument(
        "--max-files", type=int, default=200000, help="Hard cap on scanned .py files"
    )
    ap.add_argument(
        "--since-days",
        type=int,
        default=None,
        help="Only consider files modified in last N days",
    )
    ap.add_argument(
        "--exclude", nargs="*", default=[], help="Extra folder names to ignore"
    )
    args = ap.parse_args()

    roots = [Path(p) for p in args.root]
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)
    since_cutoff = None
    if args.since_days:
        since_cutoff = datetime.now() - timedelta(days=args.since_days)

    file_count = 0
    project_cache = {}
    projects = {}  # root -> stats

    def bump_project(proot: Path):
        if proot not in projects:
            projects[proot] = {
                "project": proot.name,
                "root": str(proot),
                "py_files": 0,
                "total_loc": 0,
                "functions": 0,
                "classes": 0,
                "imports": {},
                "last_write": None,
                "created": None,
                "has_readme": any(
                    (proot / f).exists()
                    for f in ("README.md", "README.rst", "README.txt")
                ),
                "has_reqs": any(
                    (proot / f).exists()
                    for f in ("requirements.txt", "pyproject.toml", "setup.py")
                ),
                "tests": (proot / "tests").exists(),
                "notables": set(),
            }

    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            # filter excludes (by name match)
            dirnames[:] = [d for d in dirnames if d not in excludes]
            # guard: skip huge virtualenvs quickly
            if any(d in excludes for d in Path(dirpath).parts):
                continue
            for fn in filenames:
                if not fn.lower().endswith(".py"):
                    continue
                fpath = Path(dirpath) / fn
                try:
                    st = fpath.stat()
                except Exception:
                    continue
                if since_cutoff and datetime.fromtimestamp(st.st_mtime) < since_cutoff:
                    continue
                proot = find_project_root(fpath, project_cache)
                bump_project(proot)
                P = projects[proot]

                metrics = analyze_py_file(fpath)
                P["py_files"] += 1
                P["total_loc"] += metrics["loc"]
                P["functions"] += metrics["functions"]
                P["classes"] += metrics["classes"]
                for imp in metrics["imports"]:
                    if imp:
                        P["imports"][imp] = P["imports"].get(imp, 0) + 1

                lw = datetime.fromtimestamp(st.st_mtime)
                cr = datetime.fromtimestamp(st.st_ctime)
                P["last_write"] = (
                    lw
                    if (P["last_write"] is None or lw > P["last_write"])
                    else P["last_write"]
                )
                P["created"] = (
                    cr if (P["created"] is None or cr < P["created"]) else P["created"]
                )

                name_low = fn.lower()
                text_low = ""
                if any(h in name_low for h in MAGIC_HINTS):
                    P["notables"].add(fn)
                    text_low = ""  # avoid extra IO unless needed

                file_count += 1
                if file_count >= args.max_files:
                    print(f"Hit max files limit: {args.max_files}", file=sys.stderr)
                    break
            if file_count >= args.max_files:
                break
        if file_count >= args.max_files:
            break

    rows = []
    for proot, P in projects.items():
        days_since = 9999.0
        if P["last_write"]:
            days_since = (datetime.now() - P["last_write"]).days + (
                (datetime.now() - P["last_write"]).seconds / 86400.0
            )

        # magic hints flags
        flags = {
            f"hint_{k}": False
            for k in (
                "magic",
                "runner",
                "ready",
                "orchestrator",
                "failover",
                "audit",
                "phase",
                "self_healing",
            )
        }
        for n in P["notables"]:
            ln = n.lower()
            flags["hint_magic"] |= "magic" in ln
            flags["hint_runner"] |= "runner" in ln
            flags["hint_ready"] |= "_ready" in ln
            flags["hint_orchestrator"] |= "orchestrator" in ln
            flags["hint_failover"] |= "failover" in ln
            flags["hint_audit"] |= "audit" in ln
            flags["hint_phase"] |= "phase" in ln
            flags["hint_self_healing"] |= "self_healing" in ln

        statline = {**P, "days_since_last": days_since, **flags}
        score = magic_score(statline)
        top_imports = ", ".join(
            sorted(P["imports"], key=P["imports"].get, reverse=True)[:6]
        )
        rows.append(
            {
                "Project": P["project"],
                "Root": P["root"],
                "PyFiles": P["py_files"],
                "LOC": P["total_loc"],
                "Funcs": P["functions"],
                "Classes": P["classes"],
                "TopImports": top_imports,
                "HasREADME": P["has_readme"],
                "HasReqs": P["has_reqs"],
                "HasTests": P["tests"],
                "LastWrite": P["last_write"].isoformat() if P["last_write"] else "",
                "DaysSinceLast": round(days_since, 2),
                "Notables": ", ".join(sorted(P["notables"])) if P["notables"] else "",
                "MagicScore": score,
            }
        )

    rows.sort(key=lambda r: (-r["MagicScore"], r["DaysSinceLast"]))
    csv_path = outdir / "project_index.csv"
    md_path = outdir / "project_index.md"
    json_path = outdir / "project_index.json"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            w.writeheader()
        w.writerows(rows)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Project Rediscovery Index ({len(rows)} projects)\n\n")
        top = rows[:20]
        for i, r in enumerate(top, 1):
            f.write(f"## {i}. {r['Project']}  \n")
            f.write(
                f"**Score:** {r['MagicScore']} â€" **Files:** {r['PyFiles']} â€" **LOC:** {r['LOC']} â€" **Updated:** {r['LastWrite']}\n\n"
            )
            if r["Notables"]:
                f.write(f"- Notables: {r['Notables']}\n")
            if r["TopImports"]:
                f.write(f"- Top imports: {r['TopImports']}\n")
            f.write(f"- Path: `{r['Root']}`\n\n")

    print(
        f"[rediscover] scanned_projects={len(rows)} py_files_capped_at={args.max_files}"
    )
    print(f"[rediscover] wrote:\n  {csv_path}\n  {json_path}\n  {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
