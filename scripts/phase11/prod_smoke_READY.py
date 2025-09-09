"""
Production smoke entrypoint for MAGIC.

- Safe to run with no args.
- Performs light health checks.
- Defaults to non-strict: warns but does not fail the gate.
- Set STRICT=True to enforce failures once you are ready.

Exit codes:
  0 = healthy (or only warnings when STRICT=False)
  1 = failed critical checks (STRICT=True) or unexpected exception
"""
from __future__ import annotations
import sys, os, json, time, traceback, importlib
from typing import List

# ---- TUNABLES ----
STRICT: bool = False                    # Flip to True to make failures block the gate
MIN_PYTHON: tuple = (3, 10)             # Require at least this Python
CRITICAL_MODULES: List[str] = [
    # Add modules your system must be able to import:
    # "requests",
    # "numpy",
]
REQUIRED_PATHS: List[str] = [
    r"D:\MAGIC\outputs\reports",
]
CONFIG_FILE: str | None = None          # e.g., r"D:\MAGIC\config\prod.json"
REQUIRED_CONFIG_KEYS: List[str] = [
    # e.g., "api_base", "token"
]
HEARTBEAT_PATH: str = r"D:\MAGIC\outputs\reports\smoke_heartbeat.txt"
# -------------------

def warn(msg: str) -> None:
    print(f"[SMOKE][WARN] {msg}", file=sys.stderr)

def fail(msg: str) -> None:
    print(f"[SMOKE][FAIL] {msg}", file=sys.stderr)

def ok(msg: str) -> None:
    print(f"[SMOKE][OK] {msg}")

def is_venv() -> bool:
    # Common heuristic: venv has different base_prefix
    return hasattr(sys, "base_prefix") and sys.prefix != getattr(sys, "base_prefix", sys.prefix)

def check_python_version() -> bool:
    if sys.version_info < MIN_PYTHON:
        fail(f"Python {sys.version_info.major}.{sys.version_info.minor} < {MIN_PYTHON[0]}.{MIN_PYTHON[1]}")
        return False
    ok(f"Python {sys.version_info.major}.{sys.version_info.minor} >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}")
    return True

def check_venv() -> bool:
    if not is_venv():
        warn("Not running in a virtual environment")
        return False
    ok("Running inside virtual environment")
    return True

def try_imports(mods: List[str]) -> bool:
    success = True
    for m in mods:
        try:
            importlib.import_module(m)
            ok(f"import: {m}")
        except Exception as e:
            warn(f"import failed: {m}: {e}")
            success = False
    return success

def check_paths(paths: List[str]) -> bool:
    success = True
    for p in paths:
        if not os.path.exists(p):
            warn(f"missing path: {p}")
            success = False
        else:
            ok(f"path exists: {p}")
    return success

def check_config(file: str, keys: List[str]) -> bool:
    if not file:
        return True
    if not os.path.exists(file):
        warn(f"config missing: {file}")
        return False
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        missing = [k for k in keys if k not in data]
        if missing:
            warn(f"config missing keys: {missing}")
            return False
        ok(f"config ok: {file}")
        return True
    except Exception as e:
        warn(f"config load failed: {file}: {e}")
        return False

def write_heartbeat(path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S"))
        ok(f"heartbeat wrote: {path}")
        return True
    except Exception as e:
        warn(f"heartbeat write failed: {e}")
        return False

def main() -> int:
    hard_fail = False

    # Python version (critical)
    if not check_python_version():
        hard_fail = True

    # venv presence (warning if absent)
    _ = check_venv()

    # Imports (warning if missing in non-strict; fail if STRICT)
    if CRITICAL_MODULES:
        imports_ok = try_imports(CRITICAL_MODULES)
        if not imports_ok and STRICT:
            hard_fail = True

    # Required paths (warning if missing in non-strict; fail if STRICT)
    if REQUIRED_PATHS:
        paths_ok = check_paths(REQUIRED_PATHS)
        if not paths_ok and STRICT:
            hard_fail = True

    # Config sanity (optional)
    if CONFIG_FILE:
        cfg_ok = check_config(CONFIG_FILE, REQUIRED_CONFIG_KEYS)
        if not cfg_ok and STRICT:
            hard_fail = True

    # Heartbeat write (warning in non-strict; fail in strict)
    hb_ok = write_heartbeat(HEARTBEAT_PATH)
    if not hb_ok and STRICT:
        hard_fail = True

    if hard_fail:
        fail("strict mode: failures detected")
        return 1

    ok("SMOKE complete")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)
