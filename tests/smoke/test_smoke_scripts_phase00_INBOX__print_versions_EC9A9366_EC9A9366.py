import importlib, types

def test_import_scripts_phase00_INBOX__print_versions_EC9A9366_EC9A9366():
    mod = importlib.import_module("scripts.phase00.INBOX._print_versions_EC9A9366_EC9A9366")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
