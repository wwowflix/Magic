import importlib, types


def test_import_scripts_magic_datetime():
    mod = importlib.import_module("scripts.magic_datetime")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
