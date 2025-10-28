import importlib, types

def test_import_scripts_phase00_INBOX__datasource_8F324CA7_8F324CA7():
    mod = importlib.import_module("scripts.phase00.INBOX._datasource_8F324CA7_8F324CA7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
