# tests/test_remediator_more.py
import tools.remediator as r


def test_fix_unicode_noop():
    s = "clean"
    assert r.fix_unicode(s) == "clean"


def test_apply_remediation_no_match():
    class Weird(Exception):
        pass

    assert r.apply_remediation(Weird("something")) is False
