import importlib, types


def test_import_scripts_phase00_INBOX_put_EDA8A1D7_EDA8A1D7():
    mod = importlib.import_module("scripts.phase00.INBOX.put_EDA8A1D7_EDA8A1D7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
