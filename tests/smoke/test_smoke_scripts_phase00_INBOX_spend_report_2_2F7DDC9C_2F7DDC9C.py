import importlib, types


def test_import_scripts_phase00_INBOX_spend_report_2_2F7DDC9C_2F7DDC9C():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.spend_report_2_2F7DDC9C_2F7DDC9C"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
