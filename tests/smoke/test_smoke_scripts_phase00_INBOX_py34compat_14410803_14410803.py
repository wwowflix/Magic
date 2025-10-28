import importlib, types

def test_import_scripts_phase00_INBOX_py34compat_14410803_14410803():
    mod = importlib.import_module("scripts.phase00.INBOX.py34compat_14410803_14410803")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
