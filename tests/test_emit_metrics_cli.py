import json
import sys
import subprocess
from pathlib import Path


def test_emit_metrics_cli_no_args(tmp_path: Path, monkeypatch):
    # create default inputs at expected locations
    sdir = tmp_path / "outputs" / "summaries"
    sdir.mkdir(parents=True)
    (sdir / "master.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n" "a.py\tPASS\t1\tx\n" "b.py\tFAIL\t1\ty\n",
        encoding="utf-8",
    )
    # run from tmp_path so defaults resolve inside tmp
    r = subprocess.run(
        [sys.executable, "-m", "tools.emit_metrics_from_summaries"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    out = tmp_path / "outputs" / "metrics" / "agent_metrics.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["totals"]["PASS"] == 1
    assert data["totals"]["FAIL"] == 1
