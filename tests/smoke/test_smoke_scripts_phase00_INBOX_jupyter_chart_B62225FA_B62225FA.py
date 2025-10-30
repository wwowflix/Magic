import importlib, types


def test_import_scripts_phase00_INBOX_jupyter_chart_B62225FA_B62225FA():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.jupyter_chart_B62225FA_B62225FA"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
