import importlib, types


def test_import_scripts_phase00_INBOX_basePen_236860D4_236860D4():
    mod = importlib.import_module("scripts.phase00.INBOX.basePen_236860D4_236860D4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
