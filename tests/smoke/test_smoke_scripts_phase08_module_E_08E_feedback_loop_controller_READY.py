import importlib, types


def test_import_scripts_phase08_module_E_08E_feedback_loop_controller_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_E.08E_feedback_loop_controller_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
