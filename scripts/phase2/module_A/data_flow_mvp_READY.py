"""
MAGIC Data Flow MVP
Week 1 → Day 1
"""

import json
from typing import Any, Dict


def read_input(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def parse_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": data.get("id", None),
        "timestamp": data.get("timestamp", None),
        "source": data.get("source", "unknown"),
        "payload": data.get("payload", {}),
    }


def normalize_schema(parsed: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "event_id": parsed["id"],
        "event_ts": parsed["timestamp"],
        "event_source": parsed["source"],
        "event_payload": parsed["payload"],
    }


def emit_output(normalized: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "ok",
        "data": normalized,
    }


def run(path: str) -> Dict[str, Any]:
    raw = read_input(path)
    parsed = parse_fields(raw)
    normalized = normalize_schema(parsed)
    return emit_output(normalized)


if __name__ == "__main__":
    example = run("demo.json")
    print(example)
