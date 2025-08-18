import tools.remediator as r


def test_fix_unicode_returns_clean_string():
    s = "bad\u2028line\u2029break"
    out = r.fix_unicode(s)
    assert "\u2028" not in out and "\u2029" not in out


def test_apply_remediation_file_not_found(tmp_path, monkeypatch):
    # Simulate FileNotFoundError path
    calls = {"created": False}

    def _touch(p):
        calls["created"] = True

    monkeypatch.setattr(r, "create_missing_inputs", lambda *_: _touch("x"))
    rc = r.apply_remediation(RuntimeError("FileNotFoundError: foo.csv"))
    assert rc is True and calls["created"]


def test_apply_remediation_import_error(monkeypatch):
    monkeypatch.setattr(r, "pip_install", lambda *_: True)
    rc = r.apply_remediation(ImportError("no module named x"))
    assert rc is True
