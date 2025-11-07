import importlib, types


def test_import_scripts_phase00_INBOX_polynomial_AB1DE7CF_AB1DE7CF():
    mod = importlib.import_module("scripts.phase00.INBOX.polynomial_AB1DE7CF_AB1DE7CF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
