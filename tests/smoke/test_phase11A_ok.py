import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]  # tests/smoke -> tests -> ROOT
targets = [
    ROOT / "scripts" / "phase11" / "module_A" / "11A_anomaly_log_writer_READY.py",
    ROOT / "scripts" / "phase11" / "module_A" / "11A_missing_module_detector_READY.py",
    ROOT / "scripts" / "phase11" / "module_A" / "11A_script_health_verifier_READY.py",
]

def run_target(p: pathlib.Path):
    proc = subprocess.run([sys.executable, "-X", "faulthandler", "-u", str(p)], capture_output=True, text=True)
    assert proc.returncode == 0, f"{p} exit={proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    # Optional: each prints "OK"
    assert "OK" in proc.stdout, f"{p} did not print OK. STDOUT:\n{proc.stdout}"

def test_phase11A_trio_ok():
    for t in targets:
        assert t.exists(), f"Missing file: {t}"
        run_target(t)
