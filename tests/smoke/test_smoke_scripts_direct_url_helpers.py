import importlib, types


def test_import_scripts_direct_url_helpers():
    mod = importlib.import_module("scripts.direct_url_helpers")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
