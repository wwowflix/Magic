import importlib, types


def test_import_scripts_phase01_module_D_01D_log_visualizer_cli_READY():
    mod = importlib.import_module(
        "scripts.phase01.module_D.01D_log_visualizer_cli_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
