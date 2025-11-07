import importlib, types


def test_import_scripts_phase00_INBOX_fix_prefixes_9E899E61_9E899E61():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.fix_prefixes_9E899E61_9E899E61"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
