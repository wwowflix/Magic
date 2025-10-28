import importlib, types

def test_import_scripts_phase00_INBOX_module_with_deprecations_F20EDD1C_F20EDD1C():
    mod = importlib.import_module("scripts.phase00.INBOX.module_with_deprecations_F20EDD1C_F20EDD1C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
