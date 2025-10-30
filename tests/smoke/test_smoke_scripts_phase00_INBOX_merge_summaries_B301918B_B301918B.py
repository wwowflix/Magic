import importlib, types


def test_import_scripts_phase00_INBOX_merge_summaries_B301918B_B301918B():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.merge_summaries_B301918B_B301918B"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
