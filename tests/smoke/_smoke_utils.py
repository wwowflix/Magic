import sys, subprocess, pathlib

def run_target(p: pathlib.Path) -> None:
    proc = subprocess.run([sys.executable, "-X", "faulthandler", "-u", str(p)],
                          capture_output=True, text=True)
    out = (proc.stdout or "") + (("\n"+proc.stderr) if proc.stderr else "")
    assert proc.returncode == 0, f"{p} exit={proc.returncode}\nSTDOUT:\n{out}"
    # Accept OK, PASS, WARN, or empty output
    assert ("OK" in out) or ("PASS" in out) or ("WARN" in out) or (out.strip() == ""), \
        f"{p} did not emit an accept signal. STDOUT:\n{out}"
