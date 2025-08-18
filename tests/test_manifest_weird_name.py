from pathlib import Path
from tools import create_manifest as cm


def test_manifest_includes_nonstandard_filename(tmp_path: Path):
    m = tmp_path / "scripts" / "phase7" / "module_x"
    m.mkdir(parents=True)
    # Not matching the strict prefix pattern, but still *_READY.py
    (m / "totally_weird_name_READY.py").write_text("# x", encoding="utf-8")
    files = cm.discover(tmp_path)
    rels = [p.relative_to(tmp_path).as_posix() for p in files]
    assert any("totally_weird_name_READY.py" in r for r in rels)
