import json
import sys
import subprocess
from pathlib import Path


def test_emit_metrics_cli_missing_dir_creates_empty_metrics(tmp_path: Path):
    # DO NOT create outputs/summaries — exercise the missing-dir branch
    r = subprocess.run(
        [sys.executable, "-m", "tools.emit_metrics_from_summaries"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    out = tmp_path / "outputs" / "metrics" / "agent_metrics.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["totals"] == {} and data["by_phase"] == {}
