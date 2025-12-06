from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
import json


OUTPUT = Path(__file__).resolve().parents[1] / "outputs" / "week1_error_output.json"


@dataclass
class ErrorRecord:
    code: str
    message: str
    meta: Dict[str, Any]


def collect_errors() -> List[ErrorRecord]:
    """
    Week1 error flow MVP:
    - Return a tiny, static list of errors.
    """
    return [
        ErrorRecord(code="E001", message="sample error", meta={"severity": "low"}),
        ErrorRecord(code="E002", message="another error", meta={"severity": "high"}),
    ]


def summarize(errors: List[ErrorRecord]) -> Dict[str, Any]:
    total = len(errors)
    high = sum(1 for e in errors if e.meta.get("severity") == "high")
    return {"total": total, "high": high}


def save_output(errors: List[ErrorRecord]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "errors": [asdict(e) for e in errors],
        "summary": summarize(errors),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    errors = collect_errors()
    save_output(errors)
    print(f"[W1-ERROR] OK, total={len(errors)}")


if __name__ == "__main__":
    main()
