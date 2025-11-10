import importlib, types


def test_import_scripts_phase09_module_J_09J_ai_self_check_summary_generator_READY():
    mod = importlib.import_module(
        "scripts.phase09.module_J.09J_ai_self_check_summary_generator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
