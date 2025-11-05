# MAGIC_CLEAN_V1
from pathlib import Path
import os, sys

# Robust project root
_ROOT = Path(__file__).resolve()
_tmp = _ROOT
for _ in range(6):
    if (_tmp / ".git").exists() or (_tmp / "outputs").exists():
        _ROOT = _tmp
        break
    _tmp = _tmp.parent
else:
    _ROOT = Path(__file__).resolve().parents[4]

LOG_DIR = _ROOT / "outputs" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "11A_script_health_verifier_report.txt"

def quick_health_scan():
    base = _ROOT / "scripts" / "phase11"
    checked, issues = 0, []
    for p in base.rglob("*.py"):
        try:
            _ = p.read_text(encoding="utf-8", errors="replace")
            checked += 1
        except Exception as e:
            issues.append((str(p), str(e)))
    return checked, issues

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    checked, issues = quick_health_scan()
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write(f"checked={checked}, issues={len(issues)}\n")
        for path, err in issues[:50]:
            log.write(f"ISSUE | {path} | {err}\n")
    print("OK")

if __name__ == "__main__":
    main()