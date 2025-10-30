import importlib, types


def test_import_scripts_phase00_INBOX_data_B7020F59_B7020F59():
    mod = importlib.import_module("scripts.phase00.INBOX.data_B7020F59_B7020F59")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
