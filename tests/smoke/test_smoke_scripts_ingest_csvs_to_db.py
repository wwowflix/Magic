import importlib, types

def test_import_scripts_ingest_csvs_to_db():
    mod = importlib.import_module("scripts.ingest_csvs_to_db")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
