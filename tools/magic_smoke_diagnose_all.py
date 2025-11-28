from __future__ import annotations

import importlib
import json
import os
import re
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
TESTS_SMOKE_DIR = ROOT / "tests" / "smoke"
OUT_DIR = ROOT / "outputs" / "diagnostics"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TXT_REPORT = OUT_DIR / "smoke_import_report.txt"
JSON_REPORT = OUT_DIR / "smoke_import_report.json"

IMPORT_MODULE_PATTERN = re.compile(
    r'import_module\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
)

# -------------------------------------------------------
# Result holder
# -------------------------------------------------------
@dataclass
class ImportResult:
    module: str
    ok: bool
    error_type: str | None = None
    error_message: str | None = None
    where: str | None = None    # which smoke test found it


# -------------------------------------------------------
# Step 1: Discover all import targets from smoke tests
# -------------------------------------------------------
def discover_import_targets() -> List[Tuple[str, str]]:
    targets = []

    if not TESTS_SMOKE_DIR.is_dir():
        print(f"[ERROR] Missing folder: {TESTS_SMOKE_DIR}")
        return targets

    for path in sorted(TESTS_SMOKE_DIR.glob("test_smoke_scripts_*.py")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for m in IMPORT_MODULE_PATTERN.finditer(text):
            modname = m.group(1).strip()
            targets.append((modname, path.name))

    return targets


def dedupe_targets(targets: List[Tuple[str, str]]) -> Dict[str, str]:
    result = {}
    for mod, src in targets:
        if mod not in result:
            result[mod] = src
    return result


# -------------------------------------------------------
# Step 2: Try importing each module
# -------------------------------------------------------
def try_import_module(modname: str) -> ImportResult:
    try:
        importlib.import_module(modname)
        return ImportResult(module=modname, ok=True)
    except BaseException as exc:
        etype = type(exc).__name__
        msg = str(exc)
        if len(msg) > 400:
            msg = msg[:397] + "..."
        return ImportResult(
            module=modname,
            ok=False,
            error_type=etype,
            error_message=msg,
        )


# -------------------------------------------------------
# Step 3: Save TXT and JSON reports
# -------------------------------------------------------
def write_txt_report(results: List[ImportResult]):
    with TXT_REPORT.open("w", encoding="utf-8") as f:
        f.write("=== MAGIC – Full Smoke Import Diagnostic ===\n")
        f.write(f"Repo root : {ROOT}\n\n")

        passed = [r for r in results if r.ok]
        failed = [r for r in results if not r.ok]

        f.write(f"Modules checked : {len(results)}\n")
        f.write(f"OK imports      : {len(passed)}\n")
        f.write(f"Failed imports  : {len(failed)}\n\n")

        if failed:
            f.write("---- FAILURES ----\n")
            for r in failed:
                f.write(f"\nModule : {r.module}\n")
                f.write(f"Source : {r.where}\n")
                f.write(f"Error  : {r.error_type}: {r.error_message}\n")


def write_json_report(results: List[ImportResult]):
    data = []

    for r in results:
        data.append({
            "module": r.module,
            "ok": r.ok,
            "where": r.where,
            "error_type": r.error_type,
            "error_message": r.error_message,
        })

    with JSON_REPORT.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# -------------------------------------------------------
# Main
# -------------------------------------------------------
def main():
    print("=== MAGIC – Full Smoke Import Diagnostic ===")
    print(f"Repo root       : {ROOT}")
    print(f"Smoke tests dir : {TESTS_SMOKE_DIR}\n")

    raw_targets = discover_import_targets()
    if not raw_targets:
        print("[WARN] No smoke import_module targets found.")
        sys.exit(0)

    unique = dedupe_targets(raw_targets)
    print(f"Discovered {len(raw_targets)} calls → {len(unique)} unique modules.\n")

    results = []
    for modname, src in sorted(unique.items()):
        print(f"[CHECK] {modname} (from {src})")
        res = try_import_module(modname)
        res.where = src
        results.append(res)

    # Save results
    write_txt_report(results)
    write_json_report(results)

    failed = [r for r in results if not r.ok]

    print("\nReports saved:")
    print(f"  TXT : {TXT_REPORT}")
    print(f"  JSON: {JSON_REPORT}\n")

    if failed:
        print("✗ Some imports failed. See reports for details.")
        sys.exit(1)
    else:
        print("🎉 All modules imported successfully!")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("\n[INTERNAL ERROR] Diagnostic crashed:")
        traceback.print_exc()
        sys.exit(2)
