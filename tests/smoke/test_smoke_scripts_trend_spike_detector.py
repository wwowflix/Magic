import importlib, types

def test_import_scripts_trend_spike_detector():
    mod = importlib.import_module("scripts.trend_spike_detector")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
