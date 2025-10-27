import importlib, types

def test_import_scripts_phase00_INBOX_langbulgarianmodel_BE66EF60_BE66EF60():
    mod = importlib.import_module("scripts.phase00.INBOX.langbulgarianmodel_BE66EF60_BE66EF60")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
