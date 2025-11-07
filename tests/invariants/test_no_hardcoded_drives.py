from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
PHASE_ROOT = ROOT / "scripts" / "phase11"   # current enforcement scope
PY_EXT = {".py"}
SKIP_DIRS = {"INBOX", "QUARANTINE", "__pycache__"}

def iter_safe_py(root: Path):
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            for e in d.iterdir():
                if e.is_dir():
                    if any(part in SKIP_DIRS for part in e.parts):
                        continue
                    stack.append(e)
                elif e.is_file() and e.suffix.lower() in PY_EXT:
                    yield e
        except (FileNotFoundError, PermissionError, OSError):
            continue

def test_no_hardcoded_drives_in_phase11_python():
    offenders = []
    if not PHASE_ROOT.exists():
        return  # nothing to check yet
    for p in iter_safe_py(PHASE_ROOT):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except (FileNotFoundError, PermissionError, OSError):
            continue
        # Flag Windows absolute drive roots like "C:\" or "E:\"
        if re.search(r"\b[A-Za-z]:\\", txt):
            offenders.append(str(p))
    assert not offenders, "Hardcoded drive paths found in phase11 .py files:\n" + "\n".join(offenders)
