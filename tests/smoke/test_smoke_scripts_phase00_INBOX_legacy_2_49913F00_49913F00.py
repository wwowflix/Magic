import importlib, types


def test_import_scripts_phase00_INBOX_legacy_2_49913F00_49913F00():
    mod = importlib.import_module("scripts.phase00.INBOX.legacy_2_49913F00_49913F00")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
