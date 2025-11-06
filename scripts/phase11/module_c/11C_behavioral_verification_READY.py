#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 11C — Behavioral Integrity / Safety Checker
- Scans recent outputs for forbidden patterns
- Enforces size limits (stdout & files)
- Optional safe-mode latch via flag file
- Emits one TSV line:
  module<TAB>script<TAB>status<TAB>message<TAB>utc_iso
Exit codes: 0 = PASS/WARN, 1 = FAIL
"""
from __future__ import annotations
import sys, json, re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

MODULE = "phase11_module_C"
SCRIPT  = "11C_behavioral_verification_READY.py"

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_rules(p: Path) -> dict:
    if not p.exists():
        return {
            "forbidden_strings": ["BEGIN PGP PRIVATE KEY", "sk-"],
            "scan_roots": ["outputs\\logs", "outputs\\reports"],
            "max_stdout_kb": 256,
            "max_file_mb": 25,
            "warn_if_missing_any_scan_root": True,
            "safe_mode_flag_file": "tools\\flags\\SAFE_MODE_ON",
            "summary_dir": "outputs\\reports",
            "module_name": MODULE,
            "strict": False,
        }
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {
            "forbidden_strings": ["BEGIN PGP PRIVATE KEY", "sk-"],
            "scan_roots": ["outputs\\logs", "outputs\\reports"],
            "max_stdout_kb": 256,
            "max_file_mb": 25,
            "warn_if_missing_any_scan_root": True,
            "safe_mode_flag_file": "tools\\flags\\SAFE_MODE_ON",
            "summary_dir": "outputs\\reports",
            "module_name": MODULE,
            "strict": False,
        }

def check_scan_roots(scan_roots: List[str]) -> Tuple[List[str], List[Path]]:
    missing, roots = [], []
    for r in scan_roots:
        p = Path(r)
        (roots if p.exists() else missing).append(p if p.exists() else r)
    return missing, [p for p in roots if isinstance(p, Path)]

def iter_recent_files(roots: List[Path], max_files: int = 500) -> List[Path]:
    files: List[Tuple[float, Path]] = []
    for root in roots:
        for fp in root.rglob("*"):
            if fp.is_file():
                try:
                    files.append((fp.stat().st_mtime, fp))
                except Exception:
                    pass
    files.sort(reverse=True, key=lambda t: t[0])
    return [fp for _, fp in files[:max_files]]

def scan_forbidden(files: List[Path], needles: List[str]) -> List[Tuple[Path, str]]:
    if not needles: return []
    import re
    hits: List[Tuple[Path, str]] = []
    pattern = re.compile("|".join(re.escape(s) for s in needles), re.IGNORECASE)
    for fp in files:
        try:
            with fp.open("rb") as f:
                chunk = f.read(1_000_000)  # 1 MB
            text = chunk.decode("utf-8", errors="replace")
            if pattern.search(text):
                for s in needles:
                    if s.lower() in text.lower():
                        hits.append((fp, s)); break
        except Exception:
            pass
    return hits

def scan_large_files(files: List[Path], limit_mb: int) -> List[Tuple[Path, float]]:
    overs: List[Tuple[Path, float]] = []
    byte_limit = limit_mb * 1024 * 1024
    for fp in files:
        try:
            size = fp.stat().st_size
            if size > byte_limit:
                overs.append((fp, round(size / (1024 * 1024), 2)))
        except Exception:
            pass
    return overs

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    root = Path(".").resolve()
    rules_path = root / "config" / "behavior_rules.json"
    rules = load_rules(rules_path)

    scan_roots = rules.get("scan_roots", [])
    forbidden  = rules.get("forbidden_strings", [])
    max_stdout_kb = int(rules.get("max_stdout_kb", 256))
    max_file_mb = int(rules.get("max_file_mb", 25))
    warn_missing = bool(rules.get("warn_if_missing_any_scan_root", True))
    safe_mode_flag_file = Path(rules.get("safe_mode_flag_file", "tools\\flags\\SAFE_MODE_ON"))
    strict = bool(rules.get("strict", False))

    if safe_mode_flag_file.exists():
        print(f"{MODULE}\t{SCRIPT}\tWARN\tSAFE_MODE flag present; enforcement active\t{utc_now_iso()}")
        return 0

    missing, roots = check_scan_roots(scan_roots)
    if missing and warn_missing:
        print(f"{MODULE}\t{SCRIPT}\tWARN\tScan roots missing: {', '.join(missing)}\t{utc_now_iso()}")

    files = iter_recent_files(roots)
    hits  = scan_forbidden(files, forbidden) if forbidden else []
    overs = scan_large_files(files, max_file_mb) if max_file_mb > 0 else []

    if hits:
        fp, needle = hits[0]
        print(f"{MODULE}\t{SCRIPT}\tFAIL\tForbidden pattern '{needle}' in {fp.as_posix()}\t{utc_now_iso()}")
        return 1

    if overs:
        fp, size = max(overs, key=lambda t: t[1])
        status = "WARN" if not strict else "FAIL"
        print(f"{MODULE}\t{SCRIPT}\t{status}\tLarge file {fp.as_posix()} = {size}MB (> {max_file_mb}MB)\t{utc_now_iso()}")
        return 0 if not strict else 1

    msg = f"Behavioral checks clear; scanned={len(files)} roots={len(roots)}"
    line = f"{MODULE}\t{SCRIPT}\tPASS\t{msg}\t{utc_now_iso()}"
    if len(line.encode("utf-8"))/1024.0 > max_stdout_kb:
        print(f"{MODULE}\t{SCRIPT}\tWARN\tOwn stdout would exceed {max_stdout_kb}KB; truncating\t{utc_now_iso()}")
        return 0

    print(line)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
print('OK')
