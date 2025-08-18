import tools.remediator as r


def test_unicode_path_returns_true(monkeypatch):
    monkeypatch.setattr(r, "fix_unicode", lambda s: s.replace("\u2028", "").replace("\u2029", ""))
    assert r.apply_remediation(UnicodeError("bad \u2028 line")) is True
