#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
11D — API/Callchain Integrity (MONITOR)
- Reads recent lines from outputs/{logs,reports}
- Validates simple call order and domain hygiene
- Emits one TSV line: module<TAB>script<TAB>status<TAB>message<TAB>utc_iso
- Exit 0 for PASS/WARN, 1 for FAIL (strict only)
"""
from __future__ import annotations
import sys, json, re, os
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Tuple

MODULE = "phase11_module_D"
SCRIPT  = "11D_api_callchain_verifier_READY.py"

def utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_rules(p: Path) -> dict:
    if not p.exists():
        return {
            "scan_roots": ["outputs\\logs", "outputs\\reports"],
            "max_chain_len": 12,
            "warn_if_missing_roots": True,
            "enforce_order_pairs": [["request_prepared","request_sent"],["request_sent","response_received"]],
            "forbidden_apis": ["http://","ftp://"],
            "allowlist_domains": ["https://","wss://"],
            "strict": False,
            "summary_dir": "outputs\\reports",
            "module_name": MODULE
        }
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"scan_roots":["outputs\\logs","outputs\\reports"],"strict":False,"summary_dir":"outputs\\reports","module_name":MODULE}

def recent_files(roots: List[Path], limit=400) -> List[Path]:
    bag=[]
    for r in roots:
        if not r.exists(): continue
        for p in r.rglob("*"):
            if p.is_file():
                try: bag.append((p.stat().st_mtime,p))
                except Exception: pass
    bag.sort(reverse=True, key=lambda t:t[0])
    return [p for _,p in bag[:limit]]

def grep_lines(files: List[Path], limit_bytes=300_000) -> List[str]:
    lines=[]
    for p in files:
        try:
            blob=p.read_bytes()[:limit_bytes]
            text=blob.decode("utf-8","replace")
            lines.extend(text.splitlines()[-200:])  # last chunk
        except Exception:
            continue
    return lines[-2000:]

def has_forbidden(lines: List[str], needles: List[str]) -> Tuple[bool,str]:
    low="\n".join(lines).lower()
    for n in needles or []:
        if n.lower() in low:
            return True, n
    return False, ""

def allowed_scheme(lines: List[str], allow: List[str]) -> bool:
    joined="\n".join(lines)
    # at least one allowed scheme if URLs are present
    return ("http" not in joined.lower()) or any(a in joined for a in allow or [])

def check_order(lines: List[str], pairs: List[List[str]]) -> Tuple[bool,str]:
    joined="\n".join(lines)
    ok_all=True; bad_msg=""
    for a,b in pairs or []:
        ia=joined.find(a); ib=joined.find(b)
        if ia != -1 and ib != -1 and ib < ia:
            ok_all=False; bad_msg=f"order violation: {a} -> {b}"
            break
    return ok_all, bad_msg

def main() -> int:
    try: sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception: pass

    root=Path(".").resolve()
    rules=load_rules(root / "config" / "api_chain_rules.json")

    scan_roots=[Path(r) for r in rules.get("scan_roots",[])]
    missing=[str(r) for r in scan_roots if not r.exists()]
    strict=bool(rules.get("strict",False))

    if missing and rules.get("warn_if_missing_roots",True):
        print(f"{MODULE}\t{SCRIPT}\tWARN\tmissing scan roots: {', '.join(missing)}\t{utc()}")
        # continue; do not fail just because logs aren't there

    files=recent_files(scan_roots)
    lines=grep_lines(files)

    bad, needle = has_forbidden(lines, rules.get("forbidden_apis",[]))
    if bad:
        status = "FAIL" if strict else "WARN"
        print(f"{MODULE}\t{SCRIPT}\t{status}\tforbidden API scheme detected: {needle}\t{utc()}")
        return 1 if strict else 0

    if not allowed_scheme(lines, rules.get("allowlist_domains",[])):
        status = "FAIL" if strict else "WARN"
        print(f"{MODULE}\t{SCRIPT}\t{status}\tno allowlisted API scheme present\t{utc()}")
        return 1 if strict else 0

    ok_order, msg = check_order(lines, rules.get("enforce_order_pairs",[]))
    if not ok_order:
        status = "FAIL" if strict else "WARN"
        print(f"{MODULE}\t{SCRIPT}\t{status}\t{msg}\t{utc()}")
        return 1 if strict else 0

    print(f"{MODULE}\t{SCRIPT}\tPASS\tapi chain healthy; files={len(files)} lines={len(lines)}\t{utc()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())