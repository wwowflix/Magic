import importlib, types


def test_import_scripts_phase18_module_U_18U_google_sheets_earnings_exporter_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_U.18U_google_sheets_earnings_exporter_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
