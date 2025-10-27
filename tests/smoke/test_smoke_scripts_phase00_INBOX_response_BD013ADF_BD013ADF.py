import importlib, types

def test_import_scripts_phase00_INBOX_response_BD013ADF_BD013ADF():
    mod = importlib.import_module("scripts.phase00.INBOX.response_BD013ADF_BD013ADF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
