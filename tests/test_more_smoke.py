import importlib, pytest

CANDIDATES = [
    "scripts.utils",
    "scripts.__init__",
]

@pytest.mark.parametrize("name", CANDIDATES)
def test_smoke_import(name):
    importlib.import_module(name)
