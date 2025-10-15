import pytest
from scripts.utils import to_bool

@pytest.mark.parametrize("inp,exp", [
    (True, True), (False, False),
    ("true", True), ("FALSE", False),
    ("yes", True), ("no", False),
    ("y", True), ("n", False),
    ("1", True), ("0", False),
    (1, True), (0, False),
    (" on ", True), ("off", False),
])
def test_to_bool_ok(inp, exp):
    assert to_bool(inp) is exp

@pytest.mark.parametrize("bad", ["", "maybe", 2, -1, None, [], {}])
def test_to_bool_bad(bad):
    with pytest.raises(ValueError):
        to_bool(bad)
