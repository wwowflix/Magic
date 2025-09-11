from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def load_manifest(manifest_path: str) -> List[Dict[str, Any]]:
    """Load manifest JSON into a list of dicts."""
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Manifest JSON is not a list")
        return data
    except FileNotFoundError:
        print(f"Manifest file not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)


def filter_manifest(
    entries: List[Dict[str, Any]], wanted_phases: List[int], wanted_modules: List[str]
) -> List[Dict[str, Any]]:
    """Filter manifest entries by phase and module."""
    filtered = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        phase = entry.get("Phase")
        module = entry.get("Module")
        if phase in wanted_phases and module in wanted_modules:
            filtered.append(entry)
    return filtered


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter manifest entries by phase/module.")
    parser.add_argument("--manifest", required=True, help="Path to manifest JSON file")
    parser.add_argument(
        "--phases", nargs="+", type=int, required=True, help="Phase numbers to include"
    )
    parser.add_argument("--modules", nargs="+", required=True, help="Module letters to include")
    parser.add_argument("--list", action="store_true", help="List matching entries")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    entries = load_manifest(str(manifest_path))
    selected = filter_manifest(entries, args.phases, args.modules)

    if not selected:
        print("No matching scripts found.")
        return 0

    if args.list:
        for entry in selected:
            print(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
