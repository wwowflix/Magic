import importlib, types


def test_import_scripts_phase02_collector_02A_google_trends_collector_READY():
    mod = importlib.import_module(
        "scripts.phase02.collector.02A_google_trends_collector_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
