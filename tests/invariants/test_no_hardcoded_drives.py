from pathlib import Path
import re, os

ROOT = Path(__file__).resolve().parents[2]

def iter_safe(root: Path):
    """Yield all files safely (skip deleted/inaccessible paths)."""
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            for e in d.iterdir():
                if e.is_dir():
                    # Skip typical noise folders
                    if any(x in e.parts for x in (".git", "venv", ".venv", "outputs", "build", "dist")):
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
        if any(part in p.parts for part in (".git", "venv", ".venv", "outputs", "build", "dist")):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except (FileNotFoundError, PermissionError, OSError):
            continue
        if re.search(r"\b[A-Za-z]:\\\\", txt):  # catches "C:\" etc
            offenders.append(str(p))
    assert not offenders, "Hardcoded drive paths found:\\n" + "\\n".join(offenders)
