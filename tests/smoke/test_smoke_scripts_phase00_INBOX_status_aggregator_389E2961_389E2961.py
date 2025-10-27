import importlib, types

def test_import_scripts_phase00_INBOX_status_aggregator_389E2961_389E2961():
    mod = importlib.import_module("scripts.phase00.INBOX.status_aggregator_389E2961_389E2961")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
