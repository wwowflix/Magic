import importlib, types


def test_import_scripts_phase00_INBOX_timer_comparison_E8E5FF76_E8E5FF76():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.timer_comparison_E8E5FF76_E8E5FF76"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
