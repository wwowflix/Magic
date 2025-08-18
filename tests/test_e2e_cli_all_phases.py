import json
import sys
import subprocess
from pathlib import Path


def test_e2e_cli_all_phases(tmp_path: Path):
    summaries = tmp_path / "outputs" / "summaries"
    summaries.mkdir(parents=True)
    (summaries / "phase_master_summary.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n"
        "11A_a.py\tPASS\t11\tscripts/phase11/module_A/\n"
        "12B_b.py\tFAIL\t12\tscripts/phase12/module_B/\n",
        encoding="utf-8",
    )
    # create FAIL log so ok=True
    logs_root = tmp_path / "outputs" / "logs" / "phase12_module_B"
    logs_root.mkdir(parents=True)
    (logs_root / "12B_b.log").write_text("x", encoding="utf-8")

    report = tmp_path / "e2e_report.json"
    # NOTE: no --phase argument → aggregate branch
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.e2e_smoketest",
            "--summary",
            str(summaries / "phase_master_summary.tsv"),
            "--logs_root",
            str(tmp_path / "outputs" / "logs"),
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["ok"] is True
    assert data["totals"]["PASS"] == 1 and data["totals"]["FAIL"] == 1
