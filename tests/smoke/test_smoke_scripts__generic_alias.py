import importlib, types


def test_import_scripts__generic_alias():
    mod = importlib.import_module("scripts._generic_alias")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
