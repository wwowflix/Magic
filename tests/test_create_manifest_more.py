import json
import sys
import subprocess
from pathlib import Path
from tools import create_manifest as cm


def test_discover_and_build(tmp_path: Path):
    a = tmp_path / "scripts" / "phase0" / "module_a"
    a.mkdir(parents=True)
    b = tmp_path / "scripts" / "phase1" / "module_b"
    b.mkdir(parents=True)
    (a / "A_READY.py").write_text("# a", encoding="utf-8")
    (b / "B_READY.py").write_text("# b", encoding="utf-8")

    files = cm.discover(tmp_path)
    assert len(files) == 2

    m = cm.build_manifest(tmp_path, files)
    assert m["count"] == 2
    phases = {e["phase"] for e in m["entries"]}
    assert phases == {0, 1}


def test_manifest_cli(tmp_path: Path):
    s = tmp_path / "scripts" / "phase2" / "module_c"
    s.mkdir(parents=True)
    (s / "C_READY.py").write_text("# c", encoding="utf-8")
    out = tmp_path / "phase_manifest.json"
    r = subprocess.run(
        [sys.executable, "-m", "tools.create_manifest", str(tmp_path), str(out)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["count"] == 1
    assert data["entries"][0]["path"].endswith("C_READY.py")
