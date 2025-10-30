import importlib, types


def test_import_scripts_phase00_INBOX_macUtils_963DE878_963DE878():
    mod = importlib.import_module("scripts.phase00.INBOX.macUtils_963DE878_963DE878")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
