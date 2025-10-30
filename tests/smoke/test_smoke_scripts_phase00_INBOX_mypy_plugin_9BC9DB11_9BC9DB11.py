import importlib, types


def test_import_scripts_phase00_INBOX_mypy_plugin_9BC9DB11_9BC9DB11():
    mod = importlib.import_module("scripts.phase00.INBOX.mypy_plugin_9BC9DB11_9BC9DB11")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
