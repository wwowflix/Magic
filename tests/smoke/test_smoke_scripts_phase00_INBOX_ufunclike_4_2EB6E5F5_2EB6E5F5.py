import importlib, types


def test_import_scripts_phase00_INBOX_ufunclike_4_2EB6E5F5_2EB6E5F5():
    mod = importlib.import_module("scripts.phase00.INBOX.ufunclike_4_2EB6E5F5_2EB6E5F5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
