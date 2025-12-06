"""
MAGIC Week 1 – Data Flow MVP (W1D1-1)
Tests expect:

 load_raw()            -> returns a dict
 normalize(record)     -> returns NormalizedRecord
 output writes json
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "week1_demo_input.json"
OUTPUT = ROOT / "outputs" / "week1_demo_output.json"


@dataclass
class NormalizedRecord:
    id: str
    source: str
    status: str
    payload: Dict[str, Any]


def load_raw() -> Dict[str, Any]:
    """Return raw dict data (no args — required by test)."""
    if CONFIG.exists():
        return json.loads(CONFIG.read_text(encoding="utf-8"))

    return {
        "id": "demo-1",
        "source": "week1-demo",
        "status": "ok",
        "extra": {"note": "sample-fallback", "version": 1},
    }


def normalize(record: Dict[str, Any]) -> NormalizedRecord:
    """Convert ONE dict  ONE NormalizedRecord (required by tests)."""
    return NormalizedRecord(
        id=str(record.get("id", "unknown")),
        source=str(record.get("source", "unknown")),
        status=str(record.get("status", "unknown")),
        payload={
            k: v
            for k, v in record.items()
            if k not in {"id", "source", "status"}
        },
    )


def save_output(rec: NormalizedRecord) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(asdict(rec), indent=2), encoding="utf-8")


def main() -> None:
    raw = load_raw()
    rec = normalize(raw)
    save_output(rec)

    print("[W1D1]  MVP ran ok")
    print(f"id={rec.id}, source={rec.source}, status={rec.status}")


if __name__ == "__main__":
    main()
