from pathlib import Path
from datetime import datetime, timedelta
import os

def test_cleanup_removes_old_files(tmp_path):
    # Create a fake old file
    f = tmp_path / "old.log"
    f.write_text("junk")

    # Backdate the file to 7 days ago
    old_ts = (datetime.utcnow() - timedelta(days=7)).timestamp()
    os.utime(f, (old_ts, old_ts))

    # Import your cleanup function (adjust path if needed)
    from tools.cleanup_agent import cleanup
    removed = cleanup(str(tmp_path), days=3)

    assert "old.log" in removed
    assert not f.exists()
