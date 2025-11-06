import pathlib, pytest, sys, subprocess

MODULES = [p.name for p in (pathlib.Path("scripts/phase11")).glob("module_*") if p.is_dir()]

def run_target(p: pathlib.Path) -> None:
    proc = subprocess.run([sys.executable, "-X","faulthandler","-u", str(p)],
                          capture_output=True, text=True)
    out = (proc.stdout or "") + (("\n"+proc.stderr) if proc.stderr else "")
    assert proc.returncode == 0, f"{p} exit={proc.returncode}\nSTDOUT:\n{out}"
    assert ("OK" in out) or ("PASS" in out) or ("WARN" in out) or (out.strip() == ""), \
        f"{p} did not emit an accept signal. STDOUT:\n{out}"

@pytest.mark.parametrize("mod", MODULES)
def test_phase11_ok(mod):
    base = pathlib.Path("scripts/phase11")/mod
    targets = sorted(base.rglob("*_READY.py"))
    assert targets, f"No READY scripts found under {base}"
    for t in targets:
        run_target(t)
