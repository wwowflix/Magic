from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

SCAN_DIRS  = {"scripts", "agents", "tools", "tests", ".github"}  # code-centric roots
EXCLUDE_DIRS = {".git", "venv", ".venv", "outputs", "build", "dist", ".pytest_cache", ".mypy_cache", "INBOX", "QUARANTINE", "__pycache__"}
SCAN_EXTS = {".py", ".ps1", ".psm1", ".sh", ".bat", ".cmd", ".ini", ".cfg", ".toml", ".yaml", ".yml"}  # skip .md/.json/etc

def iter_safe(root: Path):
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            for e in d.iterdir():
                if e.is_dir():
                    # must be under a scan root and not excluded
                    rel_parts = e.relative_to(ROOT).parts
                    if not rel_parts:
                        stack.append(e)  # root
                        continue
                    head = rel_parts[0]
                    if head not in SCAN_DIRS or any(x in e.parts for x in EXCLUDE_DIRS):
                        continue
                    stack.append(e)
                else:
                    yield e
        except (FileNotFoundError, PermissionError, OSError):
            continue

def test_repo_has_no_hardcoded_drives():
    offenders = []
    for p in iter_safe(ROOT):
        if not p.is_file():
            continue
        # must be under SCAN_DIRS and with a scannable extension
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            continue
        if not rel.parts or rel.parts[0] not in SCAN_DIRS:
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except (FileNotFoundError, PermissionError, OSError):
            continue
        # Flag hardcoded Windows drive roots like "C:\" or "E:\"
        if re.search(r"\b[A-Za-z]:\\", txt):
            offenders.append(str(p))
    assert not offenders, "Hardcoded drive paths found in code/config files:\\n" + "\\n".join(offenders)
