import importlib, types


def test_import_scripts_phase05_module_E_05E_output_quality_checker_READY():
    mod = importlib.import_module(
        "scripts.phase05.module_E.05E_output_quality_checker_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
