import sys, subprocess, pathlib

MOD = pathlib.Path('scripts/phase11/module_C')
targets = sorted(MOD.rglob('*_READY.py'))

def run_target(p: pathlib.Path):
    proc = subprocess.run([sys.executable, "-X","faulthandler","-u", str(p)],
                          capture_output=True, text=True)
    out = (proc.stdout or "") + (("\n"+proc.stderr) if proc.stderr else "")
    assert proc.returncode == 0, f"{p} exit={proc.returncode}\nSTDOUT:\n{out}"
    # Accept OK, PASS, WARN, or empty output
    assert ("OK" in out) or ("PASS" in out) or ("WARN" in out) or (out.strip() == ""), \
        f"{p} did not emit an accept signal. STDOUT:\n{out}"

def test_phase11_ok():
    assert targets, f"No READY scripts found under {MOD}"
    for t in targets:
        run_target(t)
