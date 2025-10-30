import importlib, types


def test_import_scripts_phase00_INBOX_sources_495C8F8A_495C8F8A():
    mod = importlib.import_module("scripts.phase00.INBOX.sources_495C8F8A_495C8F8A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
