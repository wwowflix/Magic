import importlib, types


def test_import_scripts_phase00_INBOX_grUtils_85C389E6_85C389E6():
    mod = importlib.import_module("scripts.phase00.INBOX.grUtils_85C389E6_85C389E6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
