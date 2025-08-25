from pathlib import Path
from datetime import datetime, timedelta
import os

def _mk_old(path: Path, rel: str, days_old=9):
    p = path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("x")
    ts = (datetime.utcnow() - timedelta(days=days_old)).timestamp()
    os.utime(p, (ts, ts))
    return p

def test_cleanup_chaos(tmp_path):
    names = ["a.log", "b.tmp", "nested/c.log", "nested/deeper/d.txt"]
    files = [_mk_old(tmp_path, n) for n in names]

    from tools.cleanup_agent import cleanup
    removed = cleanup(str(tmp_path), days=3)

    # All created files should be removed
    assert set(n.split("/")[-1] for n in names).issubset(set(removed))
    assert all(not f.exists() for f in files)
