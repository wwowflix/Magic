import importlib, types


def test_import_scripts_phase00_INBOX_polynomial_2_2E823C51_2E823C51():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.polynomial_2_2E823C51_2E823C51"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
