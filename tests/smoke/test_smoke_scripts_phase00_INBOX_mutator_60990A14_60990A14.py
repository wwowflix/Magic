import importlib, types

def test_import_scripts_phase00_INBOX_mutator_60990A14_60990A14():
    mod = importlib.import_module("scripts.phase00.INBOX.mutator_60990A14_60990A14")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
