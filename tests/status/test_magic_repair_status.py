from __future__ import annotations

import importlib
import io
import json
import os
import re
from pathlib import Path
from datetime import datetime
import pytest

# Env-driven filters:
# - MAGIC_PROGRESS_ONLY:  regex to INCLUDE (optional)
# - MAGIC_PROGRESS_SKIP:  regex to EXCLUDE (default below)
_INCLUDE = os.environ.get("MAGIC_PROGRESS_ONLY")
_EXCLUDE = os.environ.get(
    "MAGIC_PROGRESS_SKIP",
    r"(scrape|crawler|spider|snscrape|selenium|webdriver|twitter|x_|tiktok|youtube|"
    r"reddit|facebook|instagram|telegram|mastodon|weibo|vkontakte|api|client|mail|smtp|"
    r"notion|gspread|drive|s3|boto|bigquery|sheet|gmail|calendar|chrome|playwright|"
    r"firefox|requests_session|pipeline|ingest|producer|consumer|publish|fetch|scraper)",
)


def _discover_modules(root: Path) -> list[str]:
    scripts = root / "scripts"
    mods = []
    for p in scripts.glob("*.py"):
        if p.name == "__init__.py":
            continue
        mods.append(f"scripts.{p.stem}")

    # Apply include/exclude regex if provided
    if _INCLUDE:
        inc = re.compile(_INCLUDE, re.I)
        mods = [m for m in mods if inc.search(m)]
    if _EXCLUDE:
        exc = re.compile(_EXCLUDE, re.I)
        mods = [m for m in mods if not exc.search(m)]

    seen, out = set(), []
    for m in sorted(mods):
        if m not in seen:
            out.append(m)
            seen.add(m)
    return out


def _try_import(modname: str):
    importlib.invalidate_caches()
    try:
        importlib.import_module(modname)
        return "PASS", None
    except BaseException as e:
        et = type(e).__name__
        msg = str(e).splitlines()[0] if str(e) else ""
        return "FAIL", f"{et}: {msg}"


def _write_reports(rows: list[dict], outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tsv = outdir / f"smoke_progress_{ts}.tsv"
    jsn = outdir / f"smoke_progress_{ts}.json"
    latest_tsv = outdir / "smoke_progress_latest.tsv"
    latest_json = outdir / "smoke_progress_latest.json"

    buf = io.StringIO()
    buf.write("Module\tStatus\tError\n")
    for r in rows:
        buf.write("\t".join([r["module"], r["status"], r.get("error", "")]) + "\n")
    data = buf.getvalue()
    tsv.write_text(data, encoding="utf-8")
    latest_tsv.write_text(data, encoding="utf-8")

    js = {"generated_at": datetime.now().isoformat(), "rows": rows}
    jsn.write_text(json.dumps(js, indent=2), encoding="utf-8")
    latest_json.write_text(json.dumps(js, indent=2), encoding="utf-8")


@pytest.mark.order(0)
def test_magic_repair_progress():
    """
    Report-only test: imports a filtered set of scripts.* modules and writes a status table.
    Never fails unless MAGIC_PROGRESS_STRICT=1.
    Control the scope via MAGIC_PROGRESS_ONLY and MAGIC_PROGRESS_SKIP.
    """
    root = Path(__file__).resolve().parents[2]
    modules = _discover_modules(root)

    rows, fail_count = [], 0
    for mod in modules:
        status, err = _try_import(mod)
        rows.append({"module": mod, "status": status, "error": err or ""})
        if status == "FAIL":
            fail_count += 1

    outdir = root / "outputs" / "reports" / "readiness"
    _write_reports(rows, outdir)

    total = len(rows)
    passed = total - fail_count
    print(f"[magic-progress] {passed}/{total} imports PASS")

    if os.environ.get("MAGIC_PROGRESS_STRICT") == "1" and fail_count:
        pytest.fail(f"Strict progress gate: {fail_count} modules failing import")
