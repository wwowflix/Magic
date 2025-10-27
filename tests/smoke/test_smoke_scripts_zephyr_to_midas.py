import importlib, types

def test_import_scripts_zephyr_to_midas():
    mod = importlib.import_module("scripts.zephyr_to_midas")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
