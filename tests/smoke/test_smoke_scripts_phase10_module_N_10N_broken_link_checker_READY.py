import importlib, types


def test_import_scripts_phase10_module_N_10N_broken_link_checker_READY():
    mod = importlib.import_module(
        "scripts.phase10.module_N.10N_broken_link_checker_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
