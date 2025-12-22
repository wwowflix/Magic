# ================================================
#  MAGIC Week-1 Data Flow Auto-Gen Template
#  Input  NormalizedRecord  Output JSON
# ================================================

from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any, Dict

OUTPUT = Path(__file__).resolve().parents[2] / "outputs" / "DF101_output.json"


@dataclass
class NormalizedRecord:
    id: str
    source: str
    status: str
    payload: Dict[str, Any]


def ingest() -> Dict[str, Any]:
    return {
        "id": "DF101",
        "source": "auto-generated-flow",
        "status": "ok",
        "payload": {"seed": "alpha"},
    }


def normalize(raw: Dict[str, Any]) -> NormalizedRecord:
    return NormalizedRecord(
        id=raw.get("id", "unknown"),
        source=raw.get("source", "gen"),
        status=raw.get("status", "ok"),
        payload=raw.get("payload", {}),
    )


def save(rec: NormalizedRecord) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(asdict(rec), indent=2), encoding="utf-8")


def main() -> None:
    rec = normalize(ingest())
    save(rec)
    print("[AUTO-DATA]", rec)


if __name__ == "__main__":
    main()
