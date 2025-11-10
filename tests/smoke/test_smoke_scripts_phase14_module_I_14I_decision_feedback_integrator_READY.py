import importlib, types


def test_import_scripts_phase14_module_I_14I_decision_feedback_integrator_READY():
    mod = importlib.import_module(
        "scripts.phase14.module_I.14I_decision_feedback_integrator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
