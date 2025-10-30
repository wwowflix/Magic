import importlib, types


def test_import_scripts_phase00_INBOX_compatibility_tags_4BB1A161_4BB1A161():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.compatibility_tags_4BB1A161_4BB1A161"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
