import importlib, types


def test_import_scripts_phase00_INBOX_tags_62B62180_62B62180():
    mod = importlib.import_module("scripts.phase00.INBOX.tags_62B62180_62B62180")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
