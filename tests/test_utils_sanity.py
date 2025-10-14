from scripts import utils

def test_utils_sanity():
    assert utils.to_bool(True) is True
    assert utils.to_bool("yes") is True
    assert utils.to_bool("no") is False
