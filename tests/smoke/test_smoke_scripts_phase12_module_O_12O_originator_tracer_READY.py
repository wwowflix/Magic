import importlib, types


def test_import_scripts_phase12_module_O_12O_originator_tracer_READY():
    mod = importlib.import_module(
        "scripts.phase12.module_O.12O_originator_tracer_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
