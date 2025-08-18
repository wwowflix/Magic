import json
import sys
import subprocess
from pathlib import Path


def test_e2e_phase_with_no_rows_is_ok_true(tmp_path: Path):
    summaries = tmp_path / "outputs" / "summaries"
    summaries.mkdir(parents=True)
    (summaries / "phase_master_summary.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n" "11A_x.py\tPASS\t11\tscripts/phase11/module_A/\n",
        encoding="utf-8",
    )
    report = tmp_path / "e2e_report.json"
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.e2e_smoketest",
            "--summary",
            str(summaries / "phase_master_summary.tsv"),
            "--logs_root",
            str(tmp_path / "outputs" / "logs"),
            "--phase",
            "12",  # no rows for phase 12
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["ok"] is True and data["totals"] == {}
