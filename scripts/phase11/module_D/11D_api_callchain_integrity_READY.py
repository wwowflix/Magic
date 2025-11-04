#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 11D — API / Callchain Integrity
- Loads config/api_targets.json
- Probes a small set of external/internal endpoints
- Emits ONE TSV line:
  module<TAB>script<TAB>status<TAB>message<TAB>utc_iso
Exit codes: 0 = PASS/WARN, 1 = FAIL
"""
from __future__ import annotations

import json, sys, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple
from urllib import request, error

MODULE = "phase11_module_D"
SCRIPT = "11D_api_callchain_integrity_READY.py"

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_config(p: Path) -> Dict[str, Any]:
    defaults = {
        "endpoints": [],
        "user_agent": "MAGIC-11D-Checker/1.0",
        "max_total_sec": 30,
        "soft_fail_on_network_errors": True,
        "summary_dir": "outputs\\reports",
        "strict": False,
    }
    if not p.exists():
        return defaults
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        defaults.update({k: data.get(k, defaults[k]) for k in defaults})
        defaults["endpoints"] = data.get("endpoints", [])
        return defaults
    except Exception:
        return defaults

def fetch(ep: Dict[str, Any], ua: str) -> Tuple[str, int, float, str]:
    """
    Returns: (name, status_code or -1, elapsed_sec, err_str_or_empty)
    """
    name = ep.get("name", "endpoint")
    url = ep.get("url", "")
    method = ep.get("method", "GET").upper()
    timeout = int(ep.get("timeout_sec", 5))
    req = request.Request(url=url, method=method, headers={"User-Agent": ua})
    t0 = time.monotonic()
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            elapsed = time.monotonic() - t0
            return (name, int(status), elapsed, "")
    except error.HTTPError as he:
        elapsed = time.monotonic() - t0
        return (name, int(getattr(he, "code", 500)), elapsed, f"HTTPError:{getattr(he, 'code', 'unknown')}")
    except Exception as e:
        elapsed = time.monotonic() - t0
        return (name, -1, elapsed, f"Error:{type(e).__name__}")

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    cfg = load_config(Path("config/api_targets.json"))
    endpoints: List[Dict[str, Any]] = cfg.get("endpoints", [])
    ua = cfg.get("user_agent", "MAGIC-11D-Checker/1.0")
    max_total = float(cfg.get("max_total_sec", 30))
    soft_fail = bool(cfg.get("soft_fail_on_network_errors", True))
    strict = bool(cfg.get("strict", False))

    if not endpoints:
        print(f"{MODULE}\t{SCRIPT}\tWARN\tNo endpoints configured\t{utc_now_iso()}")
        return 0

    results: List[Tuple[str, int, float, str]] = []
    t0 = time.monotonic()
    for ep in endpoints:
        results.append(fetch(ep, ua))
        if time.monotonic() - t0 > max_total:
            results.append(("budget", -1, 0.0, "TimeBudgetExceeded"))
            break

    failures, warns = [], []
    for ep, (name, status, elapsed, err) in zip(endpoints, results):
        min_ok = int(ep.get("expect_status_min", 200))
        max_ok = int(ep.get("expect_status_max", 299))
        if status == -1 and err:
            # network / TLS / DNS error — warn or fail based on soft_fail
            if soft_fail:
                warns.append(f"{name}: {err}")
            else:
                failures.append(f"{name}: {err}")
        elif status < min_ok or status > max_ok:
            failures.append(f"{name}: status={status}")
        # else PASS

    if failures:
        status = "FAIL"
        msg = "; ".join(failures[:4])
        print(f"{MODULE}\t{SCRIPT}\t{status}\t{msg}\t{utc_now_iso()}")
        return 1

    if warns and not strict:
        status = "WARN"
        msg = "; ".join(warns[:4])
        print(f"{MODULE}\t{SCRIPT}\t{status}\t{msg}\t{utc_now_iso()}")
        return 0

    print(f"{MODULE}\t{SCRIPT}\tPASS\t{len(endpoints)} endpoints healthy\t{utc_now_iso()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())