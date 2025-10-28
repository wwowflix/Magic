import importlib, types

def test_import_scripts_phase00_INBOX_longevity_predictor_2_275CA56F_275CA56F():
    mod = importlib.import_module("scripts.phase00.INBOX.longevity_predictor_2_275CA56F_275CA56F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
