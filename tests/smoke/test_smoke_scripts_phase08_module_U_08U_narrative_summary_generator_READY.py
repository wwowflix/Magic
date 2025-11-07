import importlib, types


def test_import_scripts_phase08_module_U_08U_narrative_summary_generator_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_U.08U_narrative_summary_generator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
