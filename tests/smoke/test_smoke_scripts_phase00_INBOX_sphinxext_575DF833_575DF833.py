import importlib, types


def test_import_scripts_phase00_INBOX_sphinxext_575DF833_575DF833():
    mod = importlib.import_module("scripts.phase00.INBOX.sphinxext_575DF833_575DF833")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
