import importlib, types


def test_import_scripts_phase00_INBOX_scheme_7AF727CB_7AF727CB():
    mod = importlib.import_module("scripts.phase00.INBOX.scheme_7AF727CB_7AF727CB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
