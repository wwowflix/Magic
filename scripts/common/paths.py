from pathlib import Path
import os

def discover_root(start: Path | None = None) -> Path:
    p = (start or Path(__file__).resolve())
    tmp = p
    for _ in range(6):
        if (tmp / ".git").exists() or (tmp / "outputs").exists():
            return tmp
        tmp = tmp.parent
    return p.parents[4]

ROOT = discover_root()
LOG_DIR = ROOT / "outputs" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
