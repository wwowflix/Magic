import importlib, types


def test_import_scripts_phase00_INBOX_deduplicate_records_2_B139F347_B139F347():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.deduplicate_records_2_B139F347_B139F347"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
