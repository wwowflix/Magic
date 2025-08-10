#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAGIC – Build Live Dashboard (Week 8 · Step 8.2)

Inputs (defaults; override with CLI flags):
  --summary       outputs/summaries/phase_master_summary.tsv
  --metrics_glob  "outputs/logs/agent_metrics/*.json"

Outputs (default outdir: outputs/dashboard):
  - status_breakdown.png
  - passing_per_module.png
  - trend_over_time.png        (only if date/metrics exist)
  - module_success_rate.tsv
  - top_failing_scripts.tsv
  - dashboard_summary.json
  - index.html

Usage:
  python tools/build_dashboard.py \
    --summary outputs/summaries/phase_master_summary.tsv \
    --metrics_glob "outputs/logs/agent_metrics/*.json" \
    --outdir outputs/dashboard --restrict_phase 11
"""

import argparse
import glob
import json
import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------- config & helpers ---------------------------

PASS_LABELS = {
    "PASS", "SUCCESS", "OK", "DONE", "PASSED",
    "EXECUTED SUCCESSFULLY", "COMPLETED", "GREEN"
}
FAIL_LABELS = {"FAIL", "FAILED", "ERROR", "ERR", "RED"}
MISSING_LABELS = {"MISSING", "NOT_FOUND", "ABSENT", "NOT FOUND"}
SKIPPED_LABELS = {"SKIP", "SKIPPED"}

TIME_COL_CANDIDATES = [
    "run_at", "run_date", "timestamp", "time", "date", "last_moved", "last_run"
]

def ci_name_lookup(columns: List[str]) -> Dict[str, str]:
    """Case-insensitive lookup map: lower_name -> actual column name."""
    return {c.lower(): c for c in columns}

def find_optional_col(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Find first matching column (case-insensitive). Return None if not found."""
    lut = ci_name_lookup(list(df.columns))
    for cand in candidates:
        if cand.lower() in lut:
            return lut[cand.lower()]
    return None

def normalize_status(s) -> str:
    if pd.isna(s):
        return "OTHER"
    v = str(s).strip().upper()
    if v in PASS_LABELS:
        return "PASS"
    if v in FAIL_LABELS:
        return "FAIL"
    if v in MISSING_LABELS:
        return "MISSING"
    if v in SKIPPED_LABELS:
        return "SKIPPED"
    # heuristics
    if "PASS" in v or "SUCCESS" in v or "GREEN" in v:
        return "PASS"
    if "FAIL" in v or "ERROR" in v:
        return "FAIL"
    if "MISSING" in v or "NOT FOUND" in v:
        return "MISSING"
    if "SKIP" in v:
        return "SKIPPED"
    return v or "OTHER"

def derive_module_from_row(row: pd.Series) -> str:
    """Derive Module letter from any available hints."""
    # 1) direct columns if exist
    for key in ["module", "Module", "mod", "Mod"]:
        if key in row and pd.notna(row[key]):
            val = str(row[key]).strip()
            if val:
                return val[0].upper()
    # 2) filename pattern like '11B_script.py' or '11B-...'
    for key in ["Filename", "FinalFilename", "Script", "Name", "File"]:
        if key in row and pd.notna(row[key]):
            s = str(row[key])
            m = re.search(r'\b(\d{1,2})([A-Z])[_\-]', s)
            if m:
                return m.group(2).upper()
    # 3) folder path like 'scripts/phase11/module_B'
    for key in ["Folder", "Path", "Location"]:
        if key in row and pd.notna(row[key]):
            s = str(row[key])
            m = re.search(r'module[_/\\\-\s]?([A-Z])', s, flags=re.I)
            if m:
                return m.group(1).upper()
    return "UNK"

def derive_phase_from_row(row: pd.Series) -> Optional[int]:
    """Derive Phase number from column, filename, or folder."""
    # direct column
    for key in ["phase", "Phase", "phase_number", "PhaseNumber"]:
        if key in row and pd.notna(row[key]):
            try:
                return int(str(row[key]).strip())
            except Exception:
                pass
    # filename pattern like '11B_script.py'
    for key in ["Filename", "FinalFilename", "Script", "Name", "File"]:
        if key in row and pd.notna(row[key]):
            s = str(row[key])
            m = re.search(r'\b(\d{1,2})[A-Z][_\-]', s)
            if m:
                return int(m.group(1))
    # folder path like 'scripts/phase11/module_B'
    for key in ["Folder", "Path", "Location"]:
        if key in row and pd.notna(row[key]):
            s = str(row[key])
            m = re.search(r'phase[_/\\\-\s]?(\d{1,2})', s, flags=re.I)
            if m:
                return int(m.group(1))
    return None

def safe_savefig(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()

def load_metrics_from_json(metrics_glob: str) -> pd.DataFrame:
    rows = []
    for fpath in glob.glob(metrics_glob or ""):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                d = json.load(f)
            # Accept a few common key variants
            date = d.get("date") or d.get("run_date") or d.get("day")
            p = d.get("pass", d.get("passes", 0))
            f_ = d.get("fail", d.get("fails", d.get("errors", 0)))
            m = d.get("missing", 0)
            s = d.get("skipped", 0)
            rows.append({
                "date": date,
                "pass": int(p or 0),
                "fail": int(f_ or 0),
                "missing": int(m or 0),
                "skipped": int(s or 0)
            })
        except Exception:
            continue
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["date"]).sort_values("date")

def load_trend_from_tsv(df: pd.DataFrame) -> pd.DataFrame:
    tcol = find_optional_col(df, TIME_COL_CANDIDATES)
    if not tcol:
        return pd.DataFrame()
    tmp = df.copy()
    tmp["__status_norm"] = tmp["__status_norm"].map(normalize_status)
    tmp["__dt"] = pd.to_datetime(tmp[tcol], errors="coerce").dt.date
    tmp = tmp.dropna(subset=["__dt"])
    if tmp.empty:
        return pd.DataFrame()
    grp = tmp.groupby("__dt")["__status_norm"].value_counts().unstack(fill_value=0)
    dfm = pd.DataFrame({
        "date": pd.to_datetime(grp.index),
        "pass": grp.get("PASS", pd.Series(0, index=grp.index)).astype(int),
        "fail": grp.get("FAIL", pd.Series(0, index=grp.index)).astype(int),
        "missing": grp.get("MISSING", pd.Series(0, index=grp.index)).astype(int),
        "skipped": grp.get("SKIPPED", pd.Series(0, index=grp.index)).astype(int),
    }).sort_values("date")
    return dfm

# --------------------------- main builder ---------------------------

def build_dashboard(
    summary_path: str,
    metrics_glob: Optional[str],
    outdir: str,
    title: str = "MAGIC – Runner Dashboard",
    restrict_phase: Optional[int] = None,
    no_html: bool = False
) -> dict:
    if not os.path.isfile(summary_path):
        raise FileNotFoundError(f"Summary TSV not found: {summary_path}")

    os.makedirs(outdir, exist_ok=True)

    # Load TSV (tab-separated)
    df = pd.read_csv(summary_path, sep="\t")

    # Status normalization (case-insensitive column name)
    col_status = find_optional_col(df, ["status", "result", "outcome"])
    if not col_status:
        df["__status_norm"] = "OTHER"
    else:
        df["__status_norm"] = df[col_status].map(normalize_status)

    # Derive module + phase
    df["__module"] = df.apply(derive_module_from_row, axis=1)
    df["__phase"] = df.apply(derive_phase_from_row, axis=1)

    # Optional: focus a specific phase (e.g., Phase 11)
    if restrict_phase is not None:
        df = df[df["__phase"] == restrict_phase]

    # ---------------- charts ----------------
    images = {}

    # Chart 1: Passing scripts per module
    pass_mask = df["__status_norm"] == "PASS"
    pass_per_module = (
        df[pass_mask]
        .groupby("__module")
        .size()
        .sort_values(ascending=False)
    )
    plt.figure()
    pass_per_module.plot(kind="bar")
    plt.title("Number of Passing Scripts per Module")
    plt.xlabel("Module")
    plt.ylabel("Count")
    p1 = os.path.join(outdir, "passing_per_module.png")
    safe_savefig(p1)
    images["passing_per_module"] = os.path.basename(p1)

    # Chart 2: Status breakdown
    status_counts = df["__status_norm"].value_counts().sort_values(ascending=False)
    plt.figure()
    status_counts.plot(kind="bar")
    plt.title("Status Breakdown")
    plt.xlabel("Status")
    plt.ylabel("Count")
    p2 = os.path.join(outdir, "status_breakdown.png")
    safe_savefig(p2)
    images["status_breakdown"] = os.path.basename(p2)

    # Chart 3: Trend over time (JSON metrics preferred, TSV fallback)
    df_trend = load_metrics_from_json(metrics_glob) if metrics_glob else pd.DataFrame()
    if df_trend.empty:
        df_trend = load_trend_from_tsv(df)

    trend_available = False
    if not df_trend.empty:
        plt.figure()
        plt.plot(df_trend["date"], df_trend["pass"], label="Pass")
        plt.plot(df_trend["date"], df_trend["fail"], label="Fail")
        if "missing" in df_trend.columns:
            plt.plot(df_trend["date"], df_trend["missing"], label="Missing")
        if "skipped" in df_trend.columns:
            plt.plot(df_trend["date"], df_trend["skipped"], label="Skipped")
        plt.title("Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.legend()
        p3 = os.path.join(outdir, "trend_over_time.png")
        safe_savefig(p3)
        images["trend_over_time"] = os.path.basename(p3)
        trend_available = True

    # ---------------- extra tables (TSV) ----------------
    totals_per_module = df.groupby("__module").size()
    passes_per_module = df[df["__status_norm"] == "PASS"].groupby("__module").size()
    rates = (passes_per_module / totals_per_module * 100).fillna(0).round(1)

    mod_rate = (
        pd.DataFrame({
            "module": totals_per_module.index,
            "total": totals_per_module.values.astype(int),
            "pass": passes_per_module.reindex(totals_per_module.index).fillna(0).astype(int).values,
            "success_rate_pct": rates.reindex(totals_per_module.index).fillna(0).values
        })
        .sort_values(["success_rate_pct", "pass"], ascending=[False, False])
    )
    mod_rate_path = os.path.join(outdir, "module_success_rate.tsv")
    mod_rate.to_csv(mod_rate_path, sep="\t", index=False)

    # Top failing scripts (first 50 rows)
    cols = [c for c in ["Filename", "Folder", "Status", "Phase"] if c in df.columns]
    fail_tbl = df[df["__status_norm"] == "FAIL"][["__module", "__phase"] + cols].head(50)
    fail_tbl_path = os.path.join(outdir, "top_failing_scripts.tsv")
    fail_tbl.to_csv(fail_tbl_path, sep="\t", index=False)

    # ---------------- summary JSON ----------------
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": title,
        "input_summary_tsv": os.path.abspath(summary_path),
        "restrict_phase": restrict_phase,
        "totals": {
            "PASS": int(status_counts.get("PASS", 0)),
            "FAIL": int(status_counts.get("FAIL", 0)),
            "MISSING": int(status_counts.get("MISSING", 0)),
            "SKIPPED": int(status_counts.get("SKIPPED", 0)),
            "OTHER": int(status_counts.sum()
                         - status_counts.get("PASS", 0)
                         - status_counts.get("FAIL", 0)
                         - status_counts.get("MISSING", 0)
                         - status_counts.get("SKIPPED", 0)),
        },
        "modules_with_pass": {k: int(v) for k, v in pass_per_module.to_dict().items()},
        "images": images,
        "trend_available": trend_available,
        "tables": {
            "module_success_rate_tsv": os.path.abspath(mod_rate_path),
            "top_failing_scripts_tsv": os.path.abspath(fail_tbl_path),
        }
    }
    with open(os.path.join(outdir, "dashboard_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # ---------------- HTML ----------------
    if not no_html:
        parts = [
            "<!doctype html>",
            "<meta charset='utf-8'>",
            f"<title>{title}</title>",
            "<style>",
            "body{font-family:system-ui,Segoe UI,Arial;margin:24px;max-width:1120px}",
            "h1{margin:0 0 8px} .meta{color:#666;margin:0 0 16px}",
            "img{max-width:100%;height:auto;border:1px solid #eee;padding:8px;border-radius:12px;box-shadow:0 1px 4px rgba(0,0,0,.06)}",
            "section{margin:28px 0}",
            "a.btn{display:inline-block;margin-top:8px;padding:8px 12px;border:1px solid #ddd;border-radius:10px;text-decoration:none;color:#222}",
            "</style>",
            f"<h1>{title}</h1>",
            f"<p class='meta'>Generated at: <b>{summary['generated_at']}</b>"
            + (f" · Phase filter: <b>{restrict_phase}</b>" if restrict_phase is not None else "")
            + "</p>",
            "<section><h2>Status Breakdown</h2>",
            f"<img src='{images['status_breakdown']}' alt='Status breakdown' />",
            "</section>",
            "<section><h2>Passing Scripts per Module</h2>",
            f"<img src='{images['passing_per_module']}' alt='Passing per module' />",
            "</section>",
        ]
        if trend_available and "trend_over_time" in images:
            parts += [
                "<section><h2>Trend Over Time</h2>",
                f"<img src='{images['trend_over_time']}' alt='Trend over time' />",
                "</section>"
            ]
        parts += [
            "<section><h2>Data Tables</h2>",
            "<p><a class='btn' href='module_success_rate.tsv'>module_success_rate.tsv</a></p>",
            "<p><a class='btn' href='top_failing_scripts.tsv'>top_failing_scripts.tsv</a></p>",
            "</section>",
            "<p class='meta'>Source: outputs/summaries/phase_master_summary.tsv</p>",
        ]
        with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
            f.write("\n".join(parts))

    print(f"✅ Dashboard built in: {outdir}")
    return summary

# --------------------------- CLI ---------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", default="outputs/summaries/phase_master_summary.tsv")
    ap.add_argument("--metrics_glob", default="outputs/logs/agent_metrics/*.json")
    ap.add_argument("--outdir", default="outputs/dashboard")
    ap.add_argument("--title", default="MAGIC – Runner Dashboard")
    ap.add_argument("--restrict_phase", type=int, default=None,
                    help="Only include rows that belong to this Phase number (e.g., 11).")
    ap.add_argument("--no-html", action="store_true", help="Do not emit index.html")
    args = ap.parse_args()

    build_dashboard(
        summary_path=args.summary,
        metrics_glob=args.metrics_glob,
        outdir=args.outdir,
        title=args.title,
        restrict_phase=args.restrict_phase,
        no_html=args.no_html
    )

if __name__ == "__main__":
    main()

