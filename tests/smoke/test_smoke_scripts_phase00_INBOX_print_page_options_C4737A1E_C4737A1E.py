import importlib, types


def test_import_scripts_phase00_INBOX_print_page_options_C4737A1E_C4737A1E():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.print_page_options_C4737A1E_C4737A1E"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
