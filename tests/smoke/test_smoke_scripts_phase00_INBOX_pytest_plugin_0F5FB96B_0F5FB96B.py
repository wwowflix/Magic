import importlib, types


def test_import_scripts_phase00_INBOX_pytest_plugin_0F5FB96B_0F5FB96B():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.pytest_plugin_0F5FB96B_0F5FB96B"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
