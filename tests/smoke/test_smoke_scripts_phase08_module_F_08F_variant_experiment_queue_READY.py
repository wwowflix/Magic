import importlib, types


def test_import_scripts_phase08_module_F_08F_variant_experiment_queue_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_F.08F_variant_experiment_queue_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
