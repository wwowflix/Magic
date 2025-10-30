import importlib, types


def test_import_scripts_zephyr_feedback():
    mod = importlib.import_module("scripts.zephyr_feedback")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
