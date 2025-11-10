import json
from pathlib import Path

BASELINE = Path("outputs/metrics/sli_baseline.json")
CURRENT = Path("outputs/metrics/sli.json")

def main() -> None:
    if not CURRENT.exists():
        raise SystemExit("Missing current SLI: outputs/metrics/sli.json")

    current = json.loads(CURRENT.read_text(encoding="utf-8"))

    if not BASELINE.exists():
        BASELINE.write_text(json.dumps(current, indent=2), encoding="utf-8")
        print("No baseline found. Saved current SLI as baseline.")
        return

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    cur_avail = float(current.get("availability", 0.0))
    base_avail = float(baseline.get("availability", 0.0))
    diff = cur_avail - base_avail

    print(f"Baseline availability: {base_avail}")
    print(f"Current  availability: {cur_avail}")
    print(f"Delta: {diff:+.4f}")

if __name__ == "__main__":
    main()
