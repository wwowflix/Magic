from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set

from scripts.flow_manifest_builder import (
    FLOW_MANIFEST_PATH,
    build_manifest,
    write_manifest,
)

EXPECTED_DATA_IDS: Set[str] = {"DF101", "DF102", "DF103", "DF104", "DF105"}
EXPECTED_AI_IDS: Set[str] = {"AI101", "AI102", "AI103", "AI104", "AI105"}
EXPECTED_ALL_IDS: Set[str] = EXPECTED_DATA_IDS | EXPECTED_AI_IDS


def _assert_entry_shape(entry: Dict[str, Any]) -> None:
    assert isinstance(entry, dict)
    assert "module_id" in entry
    assert "name" in entry
    assert "category" in entry
    assert "phase" in entry
    assert "enabled" in entry
    assert isinstance(entry.get("tags"), list)


def test_build_manifest_in_memory() -> None:
    manifest: List[Dict[str, Any]] = build_manifest()

    assert isinstance(manifest, list)
    assert len(manifest) == len(EXPECTED_ALL_IDS)

    ids = {m["module_id"] for m in manifest}
    assert ids == EXPECTED_ALL_IDS

    for entry in manifest:
        _assert_entry_shape(entry)


def test_write_manifest_creates_json_file(tmp_path: Path) -> None:
    # Write into a temp directory so we do not depend on local config layout
    target = tmp_path / "flow_manifest_week1.json"

    written_path, count = write_manifest(target)

    assert written_path == target
    assert count == len(EXPECTED_ALL_IDS)
    assert target.exists()

    loaded = json.loads(target.read_text(encoding="utf-8"))
    assert isinstance(loaded, list)
    assert len(loaded) == len(EXPECTED_ALL_IDS)

    ids = {m["module_id"] for m in loaded}
    assert ids == EXPECTED_ALL_IDS

    for entry in loaded:
        _assert_entry_shape(entry)


def test_write_manifest_default_location_creates_file() -> None:
    # Clean up any old manifest
    FLOW_MANIFEST_PATH.unlink(missing_ok=True)

    written_path, count = write_manifest()

    assert written_path == FLOW_MANIFEST_PATH
    assert written_path.exists()
    assert count == len(EXPECTED_ALL_IDS)
