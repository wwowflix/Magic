import json
import sys
import subprocess
from pathlib import Path


def test_e2e_cli_shape(tmp_path: Path):
    summaries = tmp_path / "outputs" / "summaries"
    summaries.mkdir(parents=True)
    (summaries / "phase_master_summary.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n"
        "11A_x.py\tPASS\t11\tscripts/phase11/module_A/\n"
        "11B_y.py\tFAIL\t11\tscripts/phase11/module_B/\n",
        encoding="utf-8",
    )
    logs = tmp_path / "outputs" / "logs" / "phase11_module_B"
    logs.mkdir(parents=True)
    (logs / "11B_y.log").write_text("ok", encoding="utf-8")

    report = tmp_path / "e2e_report.json"
    cmd = [
        sys.executable,
        "-m",
        "tools.e2e_smoketest",
        "--summary",
        str(summaries / "phase_master_summary.tsv"),
        "--logs_root",
        str(tmp_path / "outputs" / "logs"),
        "--phase",
        "11",
        "--report",
        str(report),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["ok"] is True
    assert data["totals"]["PASS"] == 1 and data["totals"]["FAIL"] == 1
