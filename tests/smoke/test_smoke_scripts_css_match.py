import importlib, types


def test_import_scripts_css_match():
    mod = importlib.import_module("scripts.css_match")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
