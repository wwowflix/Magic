import importlib, types

def test_import_scripts_phase00_INBOX_numerictypes_2_8EBC2BAE_8EBC2BAE():
    mod = importlib.import_module("scripts.phase00.INBOX.numerictypes_2_8EBC2BAE_8EBC2BAE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
