import importlib, types


def test_import_scripts_phase01_module_B_01B_auto_cleanup_script_READY():
    mod = importlib.import_module(
        "scripts.phase01.module_B.01B_auto_cleanup_script_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
