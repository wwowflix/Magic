import importlib, types


def test_import_scripts_phase00_INBOX_ufunclike_1B54189F_1B54189F():
    mod = importlib.import_module("scripts.phase00.INBOX.ufunclike_1B54189F_1B54189F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
