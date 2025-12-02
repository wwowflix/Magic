from __future__ import annotations

import importlib
import pkgutil
import sys
import types
from pathlib import Path
from typing import List, Tuple

FAILED: List[Tuple[str, BaseException]] = []


def main() -> None:
    """
    Scan all modules under the local 'scripts' folder and try importing them
    as if they were in a 'scripts' package, similar to how tests do it.
    """
    root = Path(__file__).resolve().parent.parent
    scripts_path = root / "scripts"

    if not scripts_path.is_dir():
        print(f"[ERROR] scripts folder not found at {scripts_path}")
        return

    # Create a lightweight 'scripts' package dynamically
    pkg = types.ModuleType("scripts")
    pkg.__path__ = [str(scripts_path)]
    sys.modules.setdefault("scripts", pkg)

    print("=== MAGIC Import Scan ===")
    print(f"Scanning modules under: {scripts_path}")
    for mod in pkgutil.iter_modules(pkg.__path__, prefix="scripts."):
        name = mod.name
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            FAILED.append((name, exc))
            print(f"FAIL: {name} -> {type(exc).__name__}: {exc}")
        else:
            print(f"OK  : {name}")

    print("\\n=== SUMMARY ===")
    print(f"Total failing modules: {len(FAILED)}")
    for name, exc in FAILED:
        print(f"- {name}: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
