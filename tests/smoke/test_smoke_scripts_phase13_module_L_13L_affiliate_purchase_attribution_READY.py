import importlib, types


def test_import_scripts_phase13_module_L_13L_affiliate_purchase_attribution_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_L.13L_affiliate_purchase_attribution_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
