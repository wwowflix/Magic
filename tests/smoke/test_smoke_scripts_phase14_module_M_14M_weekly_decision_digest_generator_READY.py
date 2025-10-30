import importlib, types


def test_import_scripts_phase14_module_M_14M_weekly_decision_digest_generator_READY():
    mod = importlib.import_module(
        "scripts.phase14.module_M.14M_weekly_decision_digest_generator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
