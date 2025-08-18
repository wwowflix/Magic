import sys
import json
import subprocess
import pathlib


def test_e2e_ok_with_existing_logs(tmp_path):
    summaries_dir = tmp_path / "outputs" / "summaries"
    logs_root = tmp_path / "outputs" / "logs"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    logs_root.mkdir(parents=True, exist_ok=True)

    tsv = summaries_dir / "phase_master_summary.tsv"
    tsv.write_text(
        "Filename\tStatus\tPhase\tFolder\n"
        "11A_foo.py\tPASS\t11\tscripts/phase11/module_A/\n"
        "11B_bar.py\tFAIL\t11\tscripts/phase11/module_B/\n",
        encoding="utf-8",
    )

    fail_log_dir = logs_root / "phase11_module_B"
    fail_log_dir.mkdir(parents=True, exist_ok=True)
    (fail_log_dir / "11B_bar.log").write_text("placeholder log", encoding="utf-8")

    report = tmp_path / "e2e_report.json"
    cmd = [
        sys.executable,
        str(pathlib.Path("tools") / "e2e_smoketest.py"),
        "--summary",
        str(tsv),
        "--logs_root",
        str(logs_root),
        "--phase",
        "11",
        "--report",
        str(report),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, f"stderr:\n{proc.stderr}\nstdout:\n{proc.stdout}"
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["ok"] is True and data["phase"] == 11
    assert data["totals"].get("PASS", 0) == 1
    assert data["totals"].get("FAIL", 0) == 1
