import importlib, types


def test_import_scripts_phase00_INBOX_charsetprober_8B58F863_8B58F863():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.charsetprober_8B58F863_8B58F863"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
