import json
import sys
import subprocess
from pathlib import Path


def test_emit_metrics_cli_runs_with_no_summaries_and_writes_empty(tmp_path: Path):
    r = subprocess.run(
        [sys.executable, "-m", "tools.emit_metrics_from_summaries"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    out = tmp_path / "outputs" / "metrics" / "agent_metrics.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data == {"totals": {}, "by_phase": {}}
