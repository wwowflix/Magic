import importlib, types

def test_import_scripts_task_status():
    mod = importlib.import_module("scripts.task_status")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
