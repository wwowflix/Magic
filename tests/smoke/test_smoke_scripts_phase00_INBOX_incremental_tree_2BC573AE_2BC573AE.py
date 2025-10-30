import importlib, types


def test_import_scripts_phase00_INBOX_incremental_tree_2BC573AE_2BC573AE():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.incremental_tree_2BC573AE_2BC573AE"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
