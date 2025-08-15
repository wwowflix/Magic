import os, subprocess, sys, textwrap, tempfile, shutil

def test_integrity_checker_runs_ok(tmp_path):
    # Make a minimal READY file
    scripts_dir = tmp_path / "scripts" / "phase11" / "module_c"
    scripts_dir.mkdir(parents=True)
    good = scripts_dir / "dummy_READY.py"
    good.write_text("x=1\n", encoding="utf-8")

    # Copy the checker into tmp and run it
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    checker_src = os.path.join(repo_root, "scripts", "phase11", "module_C", "11C_script_integrity_checker_READY.py")
    checker_dst = scripts_dir / "11C_script_integrity_checker_READY.py"
    checker_dst.write_text(open(checker_src, "r", encoding="utf-8").read(), encoding="utf-8")

    # Patch SCRIPTS_DIR in the checker by running from tmp root (relative walk)
    env = os.environ.copy()
    cwd = tmp_path

    # Run checker
    result = subprocess.run([sys.executable, str(checker_dst)], cwd=cwd, capture_output=True, text=True)
    assert result.returncode == 0, f"stdout={result.stdout} stderr={result.stderr}"
