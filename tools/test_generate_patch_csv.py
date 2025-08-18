from tools import generate_patch_csv


def test_generate_patch_csv_main(tmp_path):
    # Arrange: make a dummy READY script that matches the expected "11A_*.py" style
    sdir = tmp_path / "scripts" / "phase11" / "module_A"
    sdir.mkdir(parents=True)
    (sdir / "11A_dummy_READY.py").write_text("print('ok')", encoding="utf-8")

    out = tmp_path / "patch.csv"

    # Act
    rc = generate_patch_csv.main(["--root", str(tmp_path / "scripts"), "--out", str(out)])

    # Assert
    assert rc == 0
    assert out.exists()
    txt = out.read_text(encoding="utf-8")
    # It’s fine if your writer uses a different exact layout, just check that it contains the phase/module
    assert "11" in txt and "A" in txt
