import json
import sys
import subprocess
from pathlib import Path


def test_e2e_malformed_folder_uses_fallback_log_path(tmp_path: Path):
    summaries = tmp_path / "outputs" / "summaries"
    summaries.mkdir(parents=True)
    # bad Folder value → regex fails → fallback log placed directly under logs_root
    (summaries / "phase_master_summary.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n" "weird.py\tFAIL\t99\t<<bad folder>>\n",
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
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    # should mark ok False (no log found), and log_path should be logs_root/weird.log
    fail = [row for row in data["checked"] if row["status"] == "FAIL"][0]
    assert fail["log_path"].endswith("outputs\\logs\\weird.log") or fail["log_path"].endswith(
        "outputs/logs/weird.log"
    )
    assert fail["log_found"] is False
    assert data["ok"] is False


def test_e2e_blank_status_rows_are_skipped(tmp_path: Path):
    summaries = tmp_path / "outputs" / "summaries"
    summaries.mkdir(parents=True)
    (summaries / "phase_master_summary.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n"
        "a.py\tPASS\t1\tscripts/phase1/module_A/\n"
        "skip.py\t\t1\tscripts/phase1/module_A/\n",
        encoding="utf-8",
    )
    # make PASS ok (no logs needed)
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
            "1",
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(report.read_text(encoding="utf-8"))
    # only the PASS row should be counted
    assert data["totals"] == {"PASS": 1}
