import json
import sys
import subprocess
from pathlib import Path


def test_e2e_cli_missing_summary(tmp_path: Path):
    # point to a summary file that does NOT exist
    missing_summary = tmp_path / "outputs" / "summaries" / "phase_master_summary.tsv"
    report = tmp_path / "e2e_report.json"
    cmd = [
        sys.executable,
        "-m",
        "tools.e2e_smoketest",
        "--summary",
        str(missing_summary),
        "--logs_root",
        str(tmp_path / "outputs" / "logs"),
        "--phase",
        "11",
        "--report",
        str(report),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    # some implementations return 0 with ok=False; others non-zero. Accept either.
    if r.returncode == 0 and report.exists():
        data = json.loads(report.read_text(encoding="utf-8"))
        assert data.get("ok") is False
    else:
        assert r.returncode != 0
