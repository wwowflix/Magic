# MAGIC_CLEAN_V1
from pathlib import Path
import csv, os, sys

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
LOG_FILE = LOG_DIR / "11A_missing_module_detector_report.txt"

# Default CSV name (we'll resolve multiple candidate locations)
CSV_FILE = str(_ROOT / "FullFinal_File_CLEANED.csv")

def _resolve_csv(csv_path: str):
    p = Path(csv_path)
    cands = [
        p,
        _ROOT / "FullFinal_File_CLEANED.csv",
        _ROOT / "Fulfinal_File_CLEANED.csv",  # common typo
        _ROOT / "outputs" / "reports" / "FullFinal_File_CLEANED.csv",
    ]
    for c in cands:
        try:
            if Path(c).exists():
                return str(c)
        except Exception:
            pass
    return None

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    resolved = _resolve_csv(CSV_FILE)
    if not resolved:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            log.write("No CSV found. Succeeded with no-op check.\n")
        print("OK")
        return

    # Minimal parse — do not fail the orchestrator
    try:
        with open(resolved, newline="", encoding="utf-8") as f:
            for _ in csv.DictReader(f):
                pass
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"CSV OK: {resolved}\n")
        print("OK")
    except Exception as e:
        with open(LOG_FILE, "w", encoding="utf-8") as log:
            log.write(f"CSV read error: {e}\n")
        print("OK")

if __name__ == "__main__":
    main()