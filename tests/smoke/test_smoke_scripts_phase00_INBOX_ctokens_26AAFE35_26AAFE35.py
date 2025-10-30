import importlib, types


def test_import_scripts_phase00_INBOX_ctokens_26AAFE35_26AAFE35():
    mod = importlib.import_module("scripts.phase00.INBOX.ctokens_26AAFE35_26AAFE35")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
