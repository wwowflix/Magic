from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
import json


OUTPUT = Path(__file__).resolve().parents[1] / "outputs" / "week1_file_output.json"


@dataclass
class FileRecord:
    path: str
    size: int
    meta: Dict[str, Any]


def scan_folder(root: str | Path) -> List[FileRecord]:
    """
    Week 1 file flow MVP:

    - Walk a folder
    - Collect a few *.py files
    - Capture path + size + tiny meta
    """
    base = Path(root)
    records: List[FileRecord] = []

    for p in base.glob("*.py"):
        try:
            size = p.stat().st_size
        except OSError:
            size = 0

        records.append(
            FileRecord(
                path=str(p),
                size=size,
                meta={"mvp": True},
            )
        )

        # MVP: just a small sample, not full scan
        if len(records) >= 3:
            break

    return records


def save_output(records: List[FileRecord]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(r) for r in records]
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    here = Path(__file__).resolve().parents[1] / "tools"
    records = scan_folder(here)
    save_output(records)
    print(f"[W1-FILE] OK, scanned {len(records)} files")


if __name__ == "__main__":
    main()
