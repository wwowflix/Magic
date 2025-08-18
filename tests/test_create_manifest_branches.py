import json
import tools.create_manifest as cm


def test_no_files_found(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scripts").mkdir(parents=True)
    cm.main()
    out = tmp_path / "phase_manifest.json"
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(data, list)


def test_bad_filename_is_skipped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    bad = tmp_path / "scripts" / "phase99" / "module_Z"
    bad.mkdir(parents=True)
    (bad / "phase99_weird_name.py").write_text("pass", encoding="utf-8")
    cm.main()
    out = tmp_path / "phase_manifest.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert all("weird" not in (row.get("FinalFilename", "")) for row in data)
