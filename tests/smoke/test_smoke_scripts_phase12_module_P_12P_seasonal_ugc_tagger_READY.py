import importlib, types


def test_import_scripts_phase12_module_P_12P_seasonal_ugc_tagger_READY():
    mod = importlib.import_module(
        "scripts.phase12.module_P.12P_seasonal_ugc_tagger_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
