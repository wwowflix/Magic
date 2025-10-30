import importlib, types


def test_import_scripts_phase14_module_K_14K_multi_channel_profit_projection_READY():
    mod = importlib.import_module(
        "scripts.phase14.module_K.14K_multi_channel_profit_projection_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
