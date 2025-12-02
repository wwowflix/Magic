"""
MAGIC Week 0 shim for diagnostic_test.

Original behaviour:
- Imported at module load.
- Read vault.json and crashed if the file contained a UTF-8 BOM.

MAGIC Week 0 goals:
- Import must NEVER crash.
- vault.json should be read in a BOM-safe way *only* when explicitly used.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


VAULT_PATH = Path(__file__).with_name("vault.json")


def load_vault() -> Dict[str, Any]:
    """
    Load credentials from vault.json in a BOM-safe way.

    - If the file is missing, return {}.
    - If decoding or JSON parsing fails, return {}.
    - We use encoding="utf-8-sig" to transparently handle a UTF-8 BOM.
    """
    if not VAULT_PATH.exists():
        return {}

    try:
        with VAULT_PATH.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except Exception:
        # MAGIC Week 0: diagnostics must never crash imports.
        return {}


def main() -> None:
    """
    Minimal diagnostic entrypoint.

    Safe to run manually; smoke tests only care that this module imports.
    """
    cfg = load_vault()
    print(f"[MAGIC] diagnostic_test loaded {len(cfg)} keys from {VAULT_PATH}")


if __name__ == "__main__":
    main()
