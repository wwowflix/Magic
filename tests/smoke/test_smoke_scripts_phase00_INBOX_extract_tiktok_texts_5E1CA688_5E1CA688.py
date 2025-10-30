import importlib, types


def test_import_scripts_phase00_INBOX_extract_tiktok_texts_5E1CA688_5E1CA688():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.extract_tiktok_texts_5E1CA688_5E1CA688"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
