import importlib, types


def test_import_scripts_phase00_INBOX_package_finder_9D8C3971_9D8C3971():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.package_finder_9D8C3971_9D8C3971"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
