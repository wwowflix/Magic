import json
import sys
import subprocess
from pathlib import Path


def test_manifest_cli_compact(tmp_path: Path):
    s = tmp_path / "scripts" / "phase9" / "module_z"
    s.mkdir(parents=True)
    (s / "Z_READY.py").write_text("# z", encoding="utf-8")
    out = tmp_path / "phase_manifest.json"
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.create_manifest",
            str(tmp_path),
            str(out),
            "--compact",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    # compact JSON (no pretty indent): single line or very tight
    txt = out.read_text(encoding="utf-8")
    assert "\n  " not in txt  # crude but effective: no pretty indentation
    data = json.loads(txt)
    assert data["count"] == 1
