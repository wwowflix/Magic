import importlib, types


def test_import_scripts_phase00_INBOX_subversion_BE166CF0_BE166CF0():
    mod = importlib.import_module("scripts.phase00.INBOX.subversion_BE166CF0_BE166CF0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
