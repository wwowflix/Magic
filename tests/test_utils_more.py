from scripts import utils

def test_to_bool_more():
    assert utils.to_bool(1) is True
    assert utils.to_bool(0) is False
    assert utils.to_bool("TRUE") is True
    assert utils.to_bool("False") is False
