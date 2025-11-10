import json
from pathlib import Path
from datetime import datetime

def main() -> None:
    # Simple placeholder SLI metrics
    data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "availability": 1.0,
        "latency_ms_p50": 100,
        "latency_ms_p95": 200,
        "error_rate": 0.0,
    }

    out_path = Path("outputs/metrics/sli.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote SLI metrics to {out_path}")

if __name__ == "__main__":
    main()
