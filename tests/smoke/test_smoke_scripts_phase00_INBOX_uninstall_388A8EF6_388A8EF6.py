import importlib, types

def test_import_scripts_phase00_INBOX_uninstall_388A8EF6_388A8EF6():
    mod = importlib.import_module("scripts.phase00.INBOX.uninstall_388A8EF6_388A8EF6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
