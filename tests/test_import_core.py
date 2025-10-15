import importlib, pytest
@pytest.mark.parametrize("mod", ["scripts", "tools", "scripts.utils"])
def test_imports(mod):
    try:
        importlib.import_module(mod)
    except ModuleNotFoundError:
        pytest.skip(f"{mod} not present")
