import json
from pathlib import Path
import tools.create_manifest as cm


def test_manifest_empty_and_cli_defaults(tmp_path, monkeypatch, capsys):
    # Empty case (covers default argv=None path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scripts").mkdir()
    rc = cm.main(None)  # default: scripts=./scripts, out=./phase_manifest.json
    assert rc == 0
    data = json.loads(Path("phase_manifest.json").read_text(encoding="utf-8"))
    assert data == []
    out = capsys.readouterr().out
    assert "Wrote 0 entries" in out


def test_manifest_nonempty_and_explicit_args(tmp_path, monkeypatch, capsys):
    # Non-empty discovery with expected layout
    root = tmp_path / "scripts" / "phase11" / "module_B"
    root.mkdir(parents=True)
    f = root / "11B_example_READY.py"
    f.write_text("# stub", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    # Pass extra unknown arg to ensure parse_known_args ignores it
    rc = cm.main(
        [
            "--scripts-root",
            str(tmp_path / "scripts"),
            "--out",
            "phase_manifest.json",
            "--extra-pytest-arg",  # ignored
        ]
    )
    assert rc == 0

    manifest = json.loads(Path("phase_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest) == 1
    item = manifest[0]
    assert item["phase"] == "phase11"
    assert item["module"] == "module_B"
    assert item["filename"] == "11B_example_READY.py"
    # Should print count 1
    out = capsys.readouterr().out
    assert "Wrote 1 entries" in out


def test_scripts_root_constant_is_pathlike():
    # Make sure SCRIPTS_ROOT exists and is usable
    assert hasattr(cm, "SCRIPTS_ROOT")
    assert cm.SCRIPTS_ROOT.name == "scripts"
