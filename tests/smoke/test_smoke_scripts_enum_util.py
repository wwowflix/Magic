import importlib, types


def test_import_scripts_enum_util():
    mod = importlib.import_module("scripts.enum_util")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
