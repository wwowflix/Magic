import subprocess, sys, pathlib, glob

ROOT = pathlib.Path(__file__).resolve().parents[2]
MOD  = ROOT / "scripts" / "phase11" / "module_P"
targets = [pathlib.Path(p) for p in glob.glob(str(MOD / "*_READY.py"))]

def run_target(p: pathlib.Path):
    proc = subprocess.run(
        [sys.executable, "-X", "faulthandler", "-u", str(p)],
        capture_output=True, text=True, errors="replace", timeout=120
    )
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    assert proc.returncode == 0, f"{p} exit={proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    assert ("OK" in out) or ("PASS" in out), f"{p} did not print OK/PASS.\nCOMBINED OUTPUT:\n{out}"

def test_phase11_ok():
    assert targets, f"No READY scripts found under {MOD}"
    for t in targets:
        run_target(t)
