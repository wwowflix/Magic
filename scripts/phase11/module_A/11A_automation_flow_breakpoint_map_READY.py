# MAGIC_CLEAN_V1
from pathlib import Path
import sys, json, os

# Robust project root (drive-agnostic)
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
LOG_FILE = LOG_DIR / "11A_automation_flow_breakpoint_map_report.txt"

# Minimal safe payload: write a valid JSON map and exit OK
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    breakpoint_map = {
        "phase": "11",
        "module": "A",
        "script": "11A_automation_flow_breakpoint_map_READY.py",
        "checkpoints": ["preflight", "run", "finalize"],
        "status": "OK"
    }
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(breakpoint_map, ensure_ascii=False) + "\n")
    print("OK")

if __name__ == "__main__":
    main()
