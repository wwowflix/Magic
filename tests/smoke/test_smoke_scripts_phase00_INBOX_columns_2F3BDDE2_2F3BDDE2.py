import importlib, types


def test_import_scripts_phase00_INBOX_columns_2F3BDDE2_2F3BDDE2():
    mod = importlib.import_module("scripts.phase00.INBOX.columns_2F3BDDE2_2F3BDDE2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
