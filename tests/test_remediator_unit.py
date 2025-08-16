import json, os, sys, pathlib
import types
import tools.remediator as r

def test_fix_unicode_returns_clean_string():
    s = "bad\u2028line\u2029break"
    out = r.fix_unicode(s)
    assert "\u2028" not in out and "\u2029" not in out
    assert "bad" in out and "line" in out and "break" in out

def test_create_missing_inputs_creates_file(tmp_path):
    f = tmp_path / "inputs" / "needme.txt"
    assert not f.exists()
    r.create_missing_inputs(str(f))
    assert f.exists() and f.read_text(encoding="utf-8") == ""

def test_pip_install_mock(monkeypatch):
    calls = {"ran": False}
    def fake_run(cmd, **kwargs):
        calls["ran"] = True
        class P: returncode = 0
        return P()
    monkeypatch.setattr(r, "_run", fake_run, raising=True)
    assert r.pip_install("pack==0.0") is True
    assert calls["ran"] is True

def test_apply_remediation_file_not_found(monkeypatch):
    called = {"touch": False}
    monkeypatch.setattr(r, "create_missing_inputs", lambda *_: called.__setitem__("touch", True))
    rc = r.apply_remediation(RuntimeError("FileNotFoundError: foo.csv"))
    assert rc is True and called["touch"] is True

def test_apply_remediation_import_error(monkeypatch):
    monkeypatch.setattr(r, "pip_install", lambda *_: True)
    rc = r.apply_remediation(ImportError("No module named pandas"))
    assert rc is True

def test_apply_remediation_unicode(monkeypatch):
    # If fix_unicode is called, it should return True
    monkeypatch.setattr(r, "fix_unicode", lambda s: s.replace("\u2028", "").replace("\u2029", ""))
    rc = r.apply_remediation(UnicodeError("bad \u2028 line"))
    assert rc is True

def test_apply_remediation_other_error():
    rc = r.apply_remediation(ValueError("nope"))
    assert rc is False
