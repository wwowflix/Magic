import importlib, types

def test_import_scripts_phase00_INBOX_kerning_405E67ED_405E67ED():
    mod = importlib.import_module("scripts.phase00.INBOX.kerning_405E67ED_405E67ED")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
