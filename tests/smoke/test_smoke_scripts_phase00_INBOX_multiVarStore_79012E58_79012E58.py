import importlib, types


def test_import_scripts_phase00_INBOX_multiVarStore_79012E58_79012E58():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.multiVarStore_79012E58_79012E58"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
