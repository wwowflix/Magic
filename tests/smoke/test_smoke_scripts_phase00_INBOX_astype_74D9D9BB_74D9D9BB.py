import importlib, types


def test_import_scripts_phase00_INBOX_astype_74D9D9BB_74D9D9BB():
    mod = importlib.import_module("scripts.phase00.INBOX.astype_74D9D9BB_74D9D9BB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
