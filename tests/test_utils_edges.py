from scripts import utils

def test_to_bool_edges():
    # hits fallback for unknown string -> bool("maybe") is True
    assert utils.to_bool(" maybe ") is True

    # explicit empty string path (in _FALSY)
    assert utils.to_bool("") is False

    # float path (numbers branch)
    assert utils.to_bool(0.0) is False
    assert utils.to_bool(2.5) is True

    # generic truthiness fallback (non-str, non-number)
    assert utils.to_bool([]) is False
    assert utils.to_bool([1]) is True
