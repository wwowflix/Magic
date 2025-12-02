from __future__ import annotations

"""
MAGIC Week 1 – Data Flow MVP (W1D1-1)

Goal:
- Ingest a demo JSON file.
- Parse and normalize records into a stable schema.
- Emit a normalized dict and (optionally) a JSON output file.

This MUST:
- Use only stdlib.
- Be safe to import (no side effects).
- Provide a single "run_pipeline" entrypoint for smokes & templates.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List
import json
import logging


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)
if not logger.handlers:
    # Safe default logger – does nothing noisy when imported.
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(levelname)s] data_flow_mvp: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class DataModule:
    """
    Normalized schema for one "data module" definition.

    All auto-generated modules should eventually respect this shape.
    """
    module_id: str
    name: str
    category: str
    phase: int
    enabled: bool = True
    tags: List[str] | None = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # Ensure tags is always a list (never None) for downstream code.
        data["tags"] = self.tags or []
        return data


# ---------------------------------------------------------------------------
# Core normalization helpers
# ---------------------------------------------------------------------------

def _load_raw_json(path: Path) -> Any:
    """Load raw JSON from disk."""
    logger.info("Loading demo JSON from %s", path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _normalize_record(raw: Dict[str, Any]) -> DataModule:
    """
    Normalize a single raw record into our DataModule schema.

    Handles multiple possible legacy field names so you can feed in
    slightly different demo.json shapes without breaking the MVP.
    """
    # Multiple aliases supported for robustness
    module_id = (
        raw.get("module_id")
        or raw.get("id")
        or raw.get("code")
        or "unknown"
    )

    name = (
        raw.get("name")
        or raw.get("title")
        or raw.get("label")
        or "Untitled"
    )

    category = (
        raw.get("category")
        or raw.get("type")
        or "generic"
    )

    # Phase may come as int or string; default to 0 if missing
    phase_raw = raw.get("phase", 0)
    try:
        phase = int(phase_raw)
    except Exception:
        phase = 0

    enabled = bool(raw.get("enabled", True))

    tags_raw = raw.get("tags") or raw.get("keywords") or []
    if isinstance(tags_raw, str):
        # Allow comma-separated tags in the demo file.
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    elif isinstance(tags_raw, Iterable):
        tags = [str(t) for t in tags_raw]
    else:
        tags = []

    return DataModule(
        module_id=str(module_id),
        name=str(name),
        category=str(category),
        phase=phase,
        enabled=enabled,
        tags=tags,
    )


def _normalize_dataset(raw_data: Any) -> Dict[str, Any]:
    """
    Normalize the entire raw JSON payload.

    Accepts either:
    - list[dict]
    - {"items": [...]}
    """
    if isinstance(raw_data, dict) and "items" in raw_data:
        items = raw_data["items"]
    else:
        items = raw_data

    if not isinstance(items, list):
        raise TypeError("Expected demo JSON to be a list or an {items: [...]} dict.")

    modules: List[Dict[str, Any]] = []
    for raw in items:
        if not isinstance(raw, dict):
            logger.warning("Skipping non-dict record: %r", raw)
            continue
        mod = _normalize_record(raw)
        modules.append(mod.to_dict())

    normalized: Dict[str, Any] = {
        "schema_version": "1.0",
        "module_count": len(modules),
        "modules": modules,
    }
    return normalized


def run_pipeline(
    input_path: Path,
    output_path: Path | None = None,
) -> Dict[str, Any]:
    """
    Main orchestration function (used by smokes and higher layers).

    - Loads demo JSON.
    - Normalizes it.
    - Optionally writes a normalized JSON file.

    Returns the normalized dataset as a dict.
    """
    raw = _load_raw_json(input_path)
    normalized = _normalize_dataset(raw)

    if output_path is not None:
        logger.info("Writing normalized output to %s", output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(normalized, f, indent=2, ensure_ascii=False)

    logger.info("Normalization complete – %d modules", normalized["module_count"])
    return normalized


# ---------------------------------------------------------------------------
# CLI entrypoint (safe to ignore in tests)
# ---------------------------------------------------------------------------

def _default_input() -> Path:
    """
    Default path used when running as a script.

    Matches the Week-1 table idea of 'demo.json' at project root or data/.
    """
    # Prefer ./data/demo.json, fall back to ./demo.json.
    candidates = [
        Path("data/demo.json"),
        Path("demo.json"),
    ]
    for c in candidates:
        if c.exists():
            return c
    # Just return first candidate; smokes will pass explicit path anyway.
    return candidates[0]


def main(argv: list[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="MAGIC Week-1 Data Flow MVP – normalize demo.json into canonical schema."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=str(_default_input()),
        help="Path to demo JSON file (default: data/demo.json or demo.json).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="outputs/data_flow_mvp_normalized.json",
        help="Where to write normalized JSON (default: outputs/data_flow_mvp_normalized.json).",
    )

    args = parser.parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output)

    run_pipeline(input_path, output_path)


if __name__ == "__main__":
    main()
