import importlib, types


def test_import_scripts_phase00_INBOX_mastodon_CA3F8436_CA3F8436():
    mod = importlib.import_module("scripts.phase00.INBOX.mastodon_CA3F8436_CA3F8436")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
