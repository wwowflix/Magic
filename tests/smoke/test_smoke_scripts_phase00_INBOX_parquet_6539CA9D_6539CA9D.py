import importlib, types


def test_import_scripts_phase00_INBOX_parquet_6539CA9D_6539CA9D():
    mod = importlib.import_module("scripts.phase00.INBOX.parquet_6539CA9D_6539CA9D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
