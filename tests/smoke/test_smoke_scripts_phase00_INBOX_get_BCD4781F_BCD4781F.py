import importlib, types


def test_import_scripts_phase00_INBOX_get_BCD4781F_BCD4781F():
    mod = importlib.import_module("scripts.phase00.INBOX.get_BCD4781F_BCD4781F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
