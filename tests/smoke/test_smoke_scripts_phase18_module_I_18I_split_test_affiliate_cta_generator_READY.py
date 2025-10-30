import importlib, types


def test_import_scripts_phase18_module_I_18I_split_test_affiliate_cta_generator_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_I.18I_split_test_affiliate_cta_generator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
