import importlib, types


def test_import_scripts_phase06_module_O_06O_zapier_make_integration_bridge_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_O.06O_zapier_make_integration_bridge_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
