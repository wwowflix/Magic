import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BAD = re.compile(r"[A-Za-z]:\\\\")  # any Windows drive root like C:\ or E:\

SKIP_PARTS = {".git", "venv", ".pytest_cache", "__pycache__", ".github"}

def test_repo_has_no_hardcoded_drives():
    offenders = []
    for p in ROOT.rglob("*"):
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        if p.is_file() and p.suffix in {".py", ".ps1", ".psm1"}:
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if BAD.search(txt):
                offenders.append(str(p))
    assert not offenders, "Hardcoded paths found:\\n" + "\\n".join(offenders)
