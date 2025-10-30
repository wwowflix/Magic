import importlib, types


def test_import_scripts_phase09_module_I_09I_api_gateway_access_handler_READY():
    mod = importlib.import_module(
        "scripts.phase09.module_I.09I_api_gateway_access_handler_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
