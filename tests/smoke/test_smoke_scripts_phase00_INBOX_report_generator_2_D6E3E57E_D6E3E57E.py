import importlib, types


def test_import_scripts_phase00_INBOX_report_generator_2_D6E3E57E_D6E3E57E():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.report_generator_2_D6E3E57E_D6E3E57E"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
