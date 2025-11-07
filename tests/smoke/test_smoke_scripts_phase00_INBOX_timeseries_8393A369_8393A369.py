import importlib, types


def test_import_scripts_phase00_INBOX_timeseries_8393A369_8393A369():
    mod = importlib.import_module("scripts.phase00.INBOX.timeseries_8393A369_8393A369")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
