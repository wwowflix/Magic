import json
from pathlib import Path
import tools.create_manifest as cm

def test_cov_fill_edge_cases(tmp_path: Path):
    # (A) Base path without a "scripts" subdir -> discover() else-branch
    root = tmp_path / "noscripts"
    root.mkdir()
    assert cm.discover(root) == []

    # (B) build() with a path that does NOT include "scripts" in parts -> unknown branch
    orphan = tmp_path / "weird_READY.py"
    orphan.write_text("# weird", encoding="utf-8")
    built = cm.build([orphan])
    assert built
    phase = built[0].get("phase")
    assert phase in ("unknown", -1)
    assert built[0].get("module") == "unknown"

    # (C) CLI positionals + --compact -> dict payload; allow extra files
    s = tmp_path / "scripts" / "phase7" / "mod_k"
    s.mkdir(parents=True)
    (s / "K_READY.py").write_text("# k", encoding="utf-8")
    out = tmp_path / "phase_manifest.json"
    rc = cm.main([str(tmp_path), str(out), "--compact"])
    assert rc == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert data["count"] >= 1
    assert any(
        e.get("filename") == "K_READY.py" and e.get("module") == "mod_k"
        for e in data.get("entries", [])
    )