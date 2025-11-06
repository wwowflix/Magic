from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BAD = re.compile(r"""(?i)\b[A-Z]:\\MAGIC\\|/mnt/|/Users/.*/MAGIC""")

def test_repo_has_no_hardcoded_drives():
    skipped = {".git", "venv", ".pytest_cache", "__pycache__", ".github"}
    offenders = []
    for p in ROOT.rglob("*"):
        if any(part in skipped for part in p.parts):
            continue
        if p.is_file() and p.suffix in {".py", ".ps1", ".psm1"}:
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if BAD.search(txt):
                offenders.append(str(p))
    assert not offenders, "Hardcoded paths found:\\n" + "\\n".join(offenders)
