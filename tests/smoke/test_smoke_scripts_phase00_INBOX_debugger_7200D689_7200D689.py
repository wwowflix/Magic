import importlib, types


def test_import_scripts_phase00_INBOX_debugger_7200D689_7200D689():
    mod = importlib.import_module("scripts.phase00.INBOX.debugger_7200D689_7200D689")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
