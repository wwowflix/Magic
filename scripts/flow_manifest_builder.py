from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import scripts.flow_registry as reg

# Where the Week-1 manifest will live
FLOW_MANIFEST_PATH = Path("config") / "flow_manifest_week1.json"

# Minimal required keys for each module entry
REQUIRED_KEYS = ("module_id", "name", "category", "phase", "enabled", "tags")


def build_manifest() -> List[Dict[str, Any]]:
    """
    Build an in-memory manifest from the flow registry.

    Returns a list of dicts, one per module.
    """
    items = reg.list_all_modules()
    manifest: List[Dict[str, Any]] = []

    for raw in items:
        data: Dict[str, Any] = dict(raw)

        # Ensure required keys exist
        for key in REQUIRED_KEYS:
            if key not in data:
                mid = data.get("module_id")
                raise KeyError(f"Missing {key!r} for module {mid!r}")

        # Normalise tags -> list
        tags = data.get("tags")
        if isinstance(tags, (set, tuple)):
            data["tags"] = list(tags)

        manifest.append(data)

    return manifest


def write_manifest(path: Path | None = None) -> tuple[Path, int]:
    """
    Write the manifest to disk as pretty JSON.

    Returns a tuple of (path_written, module_count).
    """
    target = Path(path) if path is not None else FLOW_MANIFEST_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest()
    text = json.dumps(manifest, indent=2, sort_keys=True)
    target.write_text(text, encoding="utf-8")

    return target, len(manifest)


def main() -> None:
    """
    CLI entrypoint for Week-1 tools/ops scripts.
    """
    path, count = write_manifest()
    print(f"[MAGIC] Flow manifest written to {path} with {count} modules.")


if __name__ == "__main__":
    main()
