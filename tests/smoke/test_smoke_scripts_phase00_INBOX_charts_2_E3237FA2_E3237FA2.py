import importlib, types


def test_import_scripts_phase00_INBOX_charts_2_E3237FA2_E3237FA2():
    mod = importlib.import_module("scripts.phase00.INBOX.charts_2_E3237FA2_E3237FA2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
