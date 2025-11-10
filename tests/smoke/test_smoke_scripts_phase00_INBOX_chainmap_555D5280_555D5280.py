import importlib, types


def test_import_scripts_phase00_INBOX_chainmap_555D5280_555D5280():
    mod = importlib.import_module("scripts.phase00.INBOX.chainmap_555D5280_555D5280")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
