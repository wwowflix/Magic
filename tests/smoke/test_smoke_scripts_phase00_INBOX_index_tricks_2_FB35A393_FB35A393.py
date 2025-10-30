import importlib, types


def test_import_scripts_phase00_INBOX_index_tricks_2_FB35A393_FB35A393():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.index_tricks_2_FB35A393_FB35A393"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
